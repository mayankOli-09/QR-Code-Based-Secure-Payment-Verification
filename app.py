from flask import Flask, render_template, request, jsonify, send_file, session, redirect, url_for
from datetime import datetime
from io import BytesIO
import re
import json
import os

app = Flask(__name__)
app.secret_key = "qr_secure_payment_verification_secret"

SCAN_HISTORY = []

def get_settings():
    return session.get("settings", {
        "verification_mode": "local",
        "theme": "professional",
        "language": "en",
        "risk_threshold": 70,
        "dark_mode": True,
        "url_api_enabled": False,
        "fraud_api_enabled": False
    })

def set_settings(data):
    session["settings"] = data

def is_payment_qr(text):
    if not text:
        return False
    t = text.strip().lower()
    return t.startswith("upi://pay") or "upi://" in t or "pay?" in t or "vpa=" in t

def parse_upi(text):
    result = {
        "is_upi": False,
        "pa": "",
        "pn": "",
        "am": "",
        "cu": "",
        "tn": "",
        "tr": "",
        "mid": "",
        "tid": "",
        "raw": text
    }
    if not text or not text.lower().startswith("upi://pay"):
        return result

    result["is_upi"] = True
    query = text.split("?", 1)[1] if "?" in text else ""
    params = {}
    for part in query.split("&"):
        if "=" in part:
            k, v = part.split("=", 1)
            params[k.lower()] = v

    result["pa"] = params.get("pa", "")
    result["pn"] = params.get("pn", "")
    result["am"] = params.get("am", "")
    result["cu"] = params.get("cu", "INR")
    result["tn"] = params.get("tn", "")
    result["tr"] = params.get("tr", "")
    result["mid"] = params.get("mid", "")
    result["tid"] = params.get("tid", "")
    return result

def check_local_url_safety(text):
    suspicious = [
        "bit.ly", "tinyurl", "t.co", "fake-bank", "login-update", "secure-pay", "verify-now"
    ]
    lowered = text.lower()
    issues = []
    if "http://" in lowered:
        issues.append("URL uses HTTP instead of HTTPS")
    if any(x in lowered for x in suspicious):
        issues.append("Suspicious domain pattern detected")
    if re.search(r"[0-9]", lowered) and re.search(r"bank|pay|upi|login|secure", lowered):
        issues.append("Possible typosquatting detected")
    return {
        "enabled": True,
        "is_safe": len(issues) == 0,
        "risk": "low" if len(issues) == 0 else "high" if len(issues) >= 2 else "medium",
        "issues": issues
    }

def detect_tampering(raw_text, parsed):
    issues = []
    if raw_text != raw_text.strip():
        issues.append("Leading or trailing whitespace detected")
    if parsed["is_upi"] and not parsed["pa"]:
        issues.append("UPI ID missing")
    if parsed["is_upi"] and parsed["pa"] and "@" not in parsed["pa"]:
        issues.append("Invalid UPI ID format")
    if parsed["is_upi"] and not parsed["pn"]:
        issues.append("Payee name missing")
    if parsed["is_upi"] and parsed["am"] and not re.match(r"^\d+(\.\d{1,2})?$", parsed["am"]):
        issues.append("Invalid amount format")
    if "upi://" in raw_text.lower() and "pa=" not in raw_text.lower():
        issues.append("Malformed UPI parameters")
    return {
        "is_tampered": len(issues) > 0,
        "issues": issues
    }

def get_risk_and_action(score):
    if score >= 85:
        return "Low", "Proceed with caution, but the QR appears safe."
    if score >= 60:
        return "Medium", "Review the QR carefully before proceeding."
    return "High", "Do not proceed unless the QR is independently verified."

def score_payment_qr(parsed, safety, tamper, raw_text):
    score = 100
    reasons = []

    if not is_payment_qr(raw_text):
        score -= 50
        reasons.append("QR does not clearly look like a payment QR.")

    if not parsed["is_upi"]:
        score -= 30
        reasons.append("UPI format not detected.")

    if parsed["is_upi"]:
        if not parsed["pa"]:
            score -= 20
            reasons.append("UPI ID is missing.")
        elif "@" not in parsed["pa"]:
            score -= 25
            reasons.append("UPI ID format is invalid.")

        if not parsed["pn"]:
            score -= 15
            reasons.append("Payee name is missing.")

        if not parsed["am"]:
            score -= 5
            reasons.append("Amount is missing.")
        else:
            try:
                amt = float(parsed["am"])
                if amt <= 0:
                    score -= 20
                    reasons.append("Amount must be greater than zero.")
                if amt > 10000:
                    score -= 10
                    reasons.append("Amount is unusually high.")
            except:
                score -= 20
                reasons.append("Amount is not a valid number.")

        if parsed["cu"] and parsed["cu"] != "INR":
            score -= 10
            reasons.append("Currency is not INR.")

    if safety["is_safe"] is False:
        score -= 25
        reasons.extend(safety["issues"])

    if tamper["is_tampered"]:
        score -= 25
        reasons.extend(tamper["issues"])

    if "merchant" in raw_text.lower() and not parsed["pn"]:
        score -= 10
        reasons.append("Merchant reference without payee name.")

    score = max(0, min(100, score))
    risk, action = get_risk_and_action(score)
    return score, reasons, risk, action

@app.route("/")
def index():
    return render_template("index.html", settings=get_settings())

@app.route("/scan")
def scan_page():
    return render_template("scan.html", settings=get_settings())

@app.route("/report")
def report_page():
    return render_template("report.html", settings=get_settings(), history=SCAN_HISTORY)

@app.route("/settings")
def settings_page():
    return render_template("settings.html", settings=get_settings())

@app.route("/api/verify", methods=["POST"])
def api_verify():
    data = request.get_json(force=True)
    raw_text = data.get("text", "")
    mode = data.get("mode", get_settings().get("verification_mode", "local"))

    parsed = parse_upi(raw_text)
    local_safety = check_local_url_safety(raw_text)
    tamper = detect_tampering(raw_text, parsed)
    is_payment = is_payment_qr(raw_text)

    score, reasons, risk, action = score_payment_qr(parsed, local_safety, tamper, raw_text)

    external_notes = []
    if mode == "external":
        external_notes.append("External API mode selected. Connect real API keys in production.")
        if len(raw_text) < 5:
            score = max(0, score - 10)
            reasons.append("External mode: QR text too short to trust.")
    else:
        external_notes.append("Local strict rules applied.")

    result = {
        "is_payment_qr": is_payment,
        "verification_mode": mode,
        "trust_score": score,
        "risk_category": risk,
        "action_recommendation": action,
        "reasons": reasons + external_notes,
        "payee_name": parsed["pn"] if parsed["is_upi"] else "",
        "upi_id": parsed["pa"] if parsed["is_upi"] else "",
        "amount": parsed["am"] if parsed["is_upi"] else "",
        "merchant_info": parsed["mid"] or parsed["tid"] or parsed["pn"] or "",
        "url_safety": local_safety,
        "tampering": tamper,
        "parsed": parsed,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    SCAN_HISTORY.insert(0, result)
    SCAN_HISTORY[:] = SCAN_HISTORY[:50]
    return jsonify(result)

@app.route("/api/settings", methods=["GET", "POST"])
def api_settings():
    if request.method == "GET":
        return jsonify(get_settings())
    data = request.get_json(force=True)
    current = get_settings()
    current.update({
        "verification_mode": data.get("verification_mode", current["verification_mode"]),
        "theme": data.get("theme", current["theme"]),
        "language": data.get("language", current["language"]),
        "risk_threshold": int(data.get("risk_threshold", current["risk_threshold"])),
        "dark_mode": bool(data.get("dark_mode", current["dark_mode"])),
        "url_api_enabled": bool(data.get("url_api_enabled", current["url_api_enabled"])),
        "fraud_api_enabled": bool(data.get("fraud_api_enabled", current["fraud_api_enabled"]))
    })
    set_settings(current)
    return jsonify({"status": "saved", "settings": current})

@app.route("/api/history")
def api_history():
    return jsonify(SCAN_HISTORY)

@app.route("/api/report/pdf", methods=["POST"])
def api_report_pdf():
    data = request.get_json(force=True)
    report_text = json.dumps(data, indent=2)
    pdf_bytes = BytesIO()
    pdf_bytes.write(report_text.encode("utf-8"))
    pdf_bytes.seek(0)
    return send_file(pdf_bytes, as_attachment=True, download_name="qr_report.txt", mimetype="text/plain")

if __name__ == "__main__":
    app.run(debug=True)