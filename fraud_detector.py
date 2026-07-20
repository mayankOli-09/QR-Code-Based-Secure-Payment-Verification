from typing import Optional


def assess_risk(
    raw_data: str,
    upi_info: Optional[dict],
    url_safety: Optional[dict],
) -> dict:
    """
    Compute a trust score (0–100), rating, and list of checks.
    """
    score = 50  # Neutral starting point
    checks = []

    # ── UPI Assessment ────────────────────────────────────────────────────────
    if upi_info:
        if upi_info.get("is_valid_format"):
            score += 20
            checks.append({"label": "Valid UPI format", "passed": True})
        else:
            score -= 30
            checks.append({"label": "Invalid UPI format", "passed": False})

        if upi_info.get("payee_name"):
            score += 15
            checks.append({"label": f"Payee name present: {upi_info['payee_name']}", "passed": True})
        else:
            score -= 20
            checks.append({"label": "Payee name missing (suspicious)", "passed": False})

        if upi_info.get("vpa_suffix_known"):
            score += 10
            checks.append({"label": "VPA suffix is a known bank/wallet", "passed": True})
        else:
            checks.append({"label": "VPA suffix is unrecognized", "passed": False})

        amount = upi_info.get("amount")
        if amount:
            try:
                amt = float(amount)
                if amt > 10000:
                    score -= 15
                    checks.append({"label": f"High amount flagged: ₹{amt:,.2f}", "passed": False})
                elif amt > 0:
                    score += 5
                    checks.append({"label": f"Amount looks normal: ₹{amt:,.2f}", "passed": True})
            except ValueError:
                score -= 10
                checks.append({"label": "Invalid amount value", "passed": False})
        else:
            checks.append({"label": "No amount specified", "passed": None})

        for warning in upi_info.get("warnings", []):
            checks.append({"label": f"Warning: {warning}", "passed": False})
            score -= 5

    # ── URL Assessment ────────────────────────────────────────────────────────
    if url_safety:
        threats = url_safety.get("threats", [])
        offline_flags = url_safety.get("offline_flags", [])

        if url_safety.get("is_safe") is True and not threats:
            score += 25
            checks.append({"label": "URL passed safety checks", "passed": True})
        elif url_safety.get("is_safe") is False or threats:
            score -= 40
            for t in threats:
                checks.append({"label": f"Threat detected: {t}", "passed": False})
        else:
            checks.append({"label": "URL safety could not be determined", "passed": None})

        for flag in offline_flags:
            score -= 8
            checks.append({"label": f"Suspicious pattern: {flag}", "passed": False})

        sources = url_safety.get("sources_checked", [])
        checks.append({
            "label": f"Checked via: {', '.join(sources)}",
            "passed": True,
        })

    # ── Plain text / unknown type ─────────────────────────────────────────────
    if not upi_info and not url_safety:
        checks.append({"label": "QR contains plain text (not UPI or URL)", "passed": None})
        score = 50  # Neutral — no payment risk

    # ── Clamp score ───────────────────────────────────────────────────────────
    score = max(0, min(100, score))

    if score >= 80:
        rating = "SAFE"
        recommendation = "Looks good. You may proceed with this payment."
    elif score >= 50:
        rating = "WARNING"
        recommendation = "Proceed with caution. Verify payee details before paying."
    else:
        rating = "DANGEROUS"
        recommendation = "Do NOT proceed. This QR code shows signs of fraud."

    return {
        "trust_score": score,
        "rating": rating,
        "checks": checks,
        "recommendation": recommendation,
    }