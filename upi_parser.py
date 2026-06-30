import re
from urllib.parse import urlparse, parse_qs


# Known legitimate UPI VPA suffixes
VALID_UPI_SUFFIXES = [
    "@okaxis", "@okhdfcbank", "@okicici", "@oksbi",
    "@ybl", "@ibl", "@axl", "@paytm", "@apl",
    "@upi", "@gpay", "@paytmbank", "@kotak",
    "@fbl", "@hsbc", "@indus", "@federal",
    "@mahb", "@barodampay", "@centralbank",
    "@cmsidfc", "@dbs", "@idfcbank", "@rbl",
    "@sc", "@scbl", "@ucob", "@unionbank", "@vijb",
    "@abfspay", "@airtel", "@airtelpaymentsbank",
    "@aubank", "@bandhan", "@bob", "@boi",
    "@canara", "@citi", "@dlb", "@idbi",
    "@ikwik", "@imobile", "@indusind", "@jkb",
    "@kvb", "@lvb", "@myicici", "@nsdl",
    "@pnb", "@psb", "@sib", "@syndicate",
    "@tjsp", "@uco", "@utbi", "@vijayabank",
]


def parse_upi(upi_string: str) -> dict:
    """
    Parse a UPI QR string and extract key fields.
    Format: upi://pay?pa=...&pn=...&am=...&cu=...&tn=...
    """
    result = {
        "raw": upi_string,
        "payment_address": None,
        "payee_name": None,
        "amount": None,
        "currency": None,
        "transaction_note": None,
        "merchant_code": None,
        "is_valid_format": False,
        "vpa_suffix_known": False,
        "warnings": [],
    }

    try:
        parsed = urlparse(upi_string)
        if parsed.scheme.lower() != "upi" or parsed.netloc.lower() != "pay":
            result["warnings"].append("UPI string has unexpected scheme or host.")
            return result

        params = parse_qs(parsed.query)

        def get_param(key):
            val = params.get(key, [None])[0]
            return val.strip() if val else None

        pa = get_param("pa")
        pn = get_param("pn")
        am = get_param("am")
        cu = get_param("cu")
        tn = get_param("tn")
        mc = get_param("mc")

        result["payment_address"] = pa
        result["payee_name"] = pn
        result["amount"] = am
        result["currency"] = cu or "INR"
        result["transaction_note"] = tn
        result["merchant_code"] = mc

        # Validate UPI ID format
        if pa and _is_valid_vpa(pa):
            result["is_valid_format"] = True
            # Check if suffix is a known bank/wallet
            result["vpa_suffix_known"] = any(
                pa.lower().endswith(suffix) for suffix in VALID_UPI_SUFFIXES
            )
        else:
            result["warnings"].append("Invalid or missing UPI payment address (pa).")

        # Warn if payee name is missing
        if not pn:
            result["warnings"].append("Payee name (pn) is missing — this is suspicious.")

        # Warn on suspicious amounts
        if am:
            try:
                amt_float = float(am)
                if amt_float <= 0:
                    result["warnings"].append("Amount is zero or negative.")
                elif amt_float > 10000:
                    result["warnings"].append(f"High amount detected: ₹{amt_float:,.2f}")
            except ValueError:
                result["warnings"].append("Amount field is not a valid number.")

    except Exception as e:
        result["warnings"].append(f"Failed to parse UPI string: {str(e)}")

    return result


def _is_valid_vpa(vpa: str) -> bool:
    """Validate UPI VPA format: localpart@provider"""
    pattern = r"^[a-zA-Z0-9.\-_]+@[a-zA-Z0-9]+$"
    return bool(re.match(pattern, vpa))