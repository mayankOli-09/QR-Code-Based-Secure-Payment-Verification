import httpx
import hashlib
import base64
import os
import re
from urllib.parse import urlparse


# Load API keys from environment variables
VIRUSTOTAL_API_KEY = os.getenv("VIRUSTOTAL_API_KEY", "")
GOOGLE_SAFE_BROWSING_API_KEY = os.getenv("GOOGLE_SAFE_BROWSING_API_KEY", "")

# Offline blacklist of known malicious/phishing domain patterns
BLACKLISTED_PATTERNS = [
    r"paypal.*\.com(?!$)",           # Fake PayPal
    r"googl[e3].*login",             # Fake Google
    r"support.*microsoft.*\.com(?!$)",
    r"amazon.*-secure",
    r"secure.*amazon",
    r"phishing",
    r"free.*prize",
    r"click.*here.*win",
    r"bankofind[il]a",              # Typosquat
    r"\.tk$", r"\.ml$", r"\.ga$",  # Free TLDs commonly used for phishing
    r"bit\.ly", r"tinyurl\.com",    # Shorteners (flag for review)
    r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}",  # Raw IP address URLs
]

SUSPICIOUS_KEYWORDS = [
    "login", "signin", "verify", "secure", "update",
    "confirm", "account", "banking", "payment", "wallet",
    "prize", "winner", "free", "click", "urgent",
]


async def check_url_safety(url: str) -> dict:
    """
    Check a URL against VirusTotal, Google Safe Browsing, and offline heuristics.
    Returns a dict with is_safe, source, threats, and details.
    """
    result = {
        "url": url,
        "is_safe": None,       # True / False / None (unknown)
        "threats": [],
        "sources_checked": [],
        "offline_flags": [],
    }

    # 1. Offline heuristic checks (always run)
    offline_flags = _offline_check(url)
    result["offline_flags"] = offline_flags
    result["sources_checked"].append("offline_heuristics")

    # 2. VirusTotal (online)
    if VIRUSTOTAL_API_KEY:
        vt_result = await _check_virustotal(url)
        result["sources_checked"].append("virustotal")
        if vt_result.get("error"):
            result["threats"].append(f"VirusTotal error: {vt_result['error']}")
        elif vt_result.get("malicious", 0) > 0:
            result["threats"].append(
                f"VirusTotal: {vt_result['malicious']} engine(s) flagged this URL as malicious."
            )
            result["is_safe"] = False
        else:
            if result["is_safe"] is None:
                result["is_safe"] = True

    # 3. Google Safe Browsing (online)
    if GOOGLE_SAFE_BROWSING_API_KEY:
        gsb_result = await _check_google_safe_browsing(url)
        result["sources_checked"].append("google_safe_browsing")
        if gsb_result.get("error"):
            result["threats"].append(f"Google Safe Browsing error: {gsb_result['error']}")
        elif gsb_result.get("threats"):
            for t in gsb_result["threats"]:
                result["threats"].append(f"Google Safe Browsing: {t}")
            result["is_safe"] = False
        else:
            if result["is_safe"] is None:
                result["is_safe"] = True

    # Fallback: if no online checks ran, use offline result
    if not VIRUSTOTAL_API_KEY and not GOOGLE_SAFE_BROWSING_API_KEY:
        result["is_safe"] = len(offline_flags) == 0

    return result


def _offline_check(url: str) -> list[str]:
    flags = []
    url_lower = url.lower()

    for pattern in BLACKLISTED_PATTERNS:
        if re.search(pattern, url_lower):
            flags.append(f"Matched suspicious pattern: {pattern}")

    parsed = urlparse(url)
    domain = parsed.netloc.lower()

    # Check for excessive subdomains (e.g. secure.bank.login.evil.com)
    parts = domain.split(".")
    if len(parts) > 4:
        flags.append("Excessive subdomain depth — possible spoofing.")

    # Check for suspicious keywords in path or domain
    for kw in SUSPICIOUS_KEYWORDS:
        if kw in url_lower:
            flags.append(f"Suspicious keyword in URL: '{kw}'")
            break

    # Check for HTTP (not HTTPS) on a payment-related URL
    if url.startswith("http://"):
        flags.append("URL uses insecure HTTP (not HTTPS).")

    return flags


async def _check_virustotal(url: str) -> dict:
    try:
        url_id = base64.urlsafe_b64encode(url.encode()).decode().rstrip("=")
        headers = {"x-apikey": VIRUSTOTAL_API_KEY}

        async with httpx.AsyncClient(timeout=10) as client:
            # First, submit URL for analysis
            submit_resp = await client.post(
                "https://www.virustotal.com/api/v3/urls",
                headers=headers,
                data={"url": url},
            )
            if submit_resp.status_code not in (200, 409):
                return {"error": f"VirusTotal submit failed: {submit_resp.status_code}"}

            # Then fetch the report
            report_resp = await client.get(
                f"https://www.virustotal.com/api/v3/urls/{url_id}",
                headers=headers,
            )
            if report_resp.status_code != 200:
                return {"error": f"VirusTotal report failed: {report_resp.status_code}"}

            data = report_resp.json()
            stats = data.get("data", {}).get("attributes", {}).get("last_analysis_stats", {})
            return {
                "malicious": stats.get("malicious", 0),
                "suspicious": stats.get("suspicious", 0),
                "harmless": stats.get("harmless", 0),
                "undetected": stats.get("undetected", 0),
            }
    except Exception as e:
        return {"error": str(e)}


async def _check_google_safe_browsing(url: str) -> dict:
    try:
        payload = {
            "client": {"clientId": "qr-verifier", "clientVersion": "1.0"},
            "threatInfo": {
                "threatTypes": ["MALWARE", "SOCIAL_ENGINEERING", "UNWANTED_SOFTWARE", "POTENTIALLY_HARMFUL_APPLICATION"],
                "platformTypes": ["ANY_PLATFORM"],
                "threatEntryTypes": ["URL"],
                "threatEntries": [{"url": url}],
            },
        }
        api_url = f"https://safebrowsing.googleapis.com/v4/threatMatches:find?key={GOOGLE_SAFE_BROWSING_API_KEY}"

        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.post(api_url, json=payload)
            if resp.status_code != 200:
                return {"error": f"GSB API error: {resp.status_code}"}

            data = resp.json()
            matches = data.get("matches", [])
            threats = [m.get("threatType", "UNKNOWN") for m in matches]
            return {"threats": threats}
    except Exception as e:
        return {"error": str(e)}