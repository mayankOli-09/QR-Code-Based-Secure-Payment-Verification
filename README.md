# QR Pay Verifier

A browser-based QR code payment verification system with a Python/FastAPI backend and a vanilla JS/HTML/CSS frontend.

---

## Project Structure

```
qr-verifier/
├── backend/
│   ├── main.py                  # FastAPI app entry point
│   ├── requirements.txt
│   ├── .env.example             # Copy to .env and add API keys
│   └── services/
│       ├── qr_decoder.py        # QR image → decoded string
│       ├── upi_parser.py        # UPI string parser
│       ├── url_checker.py       # VirusTotal + Google Safe Browsing
│       └── fraud_detector.py    # Trust score + risk assessment
└── frontend/
    ├── index.html
    ├── style.css
    └── app.js
```

---

## Setup

### 1. Backend

```bash
cd backend

# Install system dependency for pyzbar (Linux/Mac)
# Ubuntu/Debian:
sudo apt-get install libzbar0
# macOS:
brew install zbar

# Install Python dependencies
pip install -r requirements.txt

# Configure API keys
cp .env.example .env
# Edit .env and paste your keys:
#   VIRUSTOTAL_API_KEY=...
#   GOOGLE_SAFE_BROWSING_API_KEY=...
```

**Get API keys:**
- VirusTotal (free): https://www.virustotal.com/gui/join-us
- Google Safe Browsing: https://console.cloud.google.com → Enable "Safe Browsing API" → Create API Key

> If you leave the keys blank, the system still works using offline heuristic checks.

### 2. Run the backend

```bash
cd backend
uvicorn main:app --reload
```

The API will be live at `http://localhost:8000`  
Interactive docs: `http://localhost:8000/docs`

### 3. Frontend

Simply open `frontend/index.html` in your browser.

> For a proper dev server (avoids CORS issues on some browsers):
> ```bash
> cd frontend
> npx serve .
> # or: python -m http.server 3000
> ```

---

## How It Works

| Step | What Happens |
|------|-------------|
| 1 | User uploads a QR code image |
| 2 | Backend decodes the QR using pyzbar + OpenCV (tries multiple strategies for robustness) |
| 3 | System detects type: UPI, URL, or plain text |
| 4 | UPI strings are parsed for payee name, amount, VPA validity |
| 5 | URLs are checked via VirusTotal + Google Safe Browsing (with offline fallback) |
| 6 | A trust score (0–100) is computed and a SAFE / WARNING / DANGEROUS rating is shown |

---

## Trust Score Breakdown

| Factor | Impact |
|--------|--------|
| Valid UPI format | +20 |
| Payee name present | +15 |
| Known bank/wallet VPA suffix | +10 |
| Normal amount | +5 |
| URL passes safety checks | +25 |
| Invalid UPI format | -30 |
| Missing payee name | -20 |
| High amount (>₹10,000) | -15 |
| Malicious URL detected | -40 |
| Suspicious URL pattern | -8 per flag |

**Ratings:** 80–100 = SAFE · 50–79 = WARNING · 0–49 = DANGEROUS

---

## API Reference

### `POST /verify`

Upload a QR code image and receive a full verification report.

**Request:** `multipart/form-data` with a field `file` (image)

**Response:**
```json
{
  "raw_data": "upi://pay?pa=merchant@upi&pn=MerchantName&am=100&cu=INR",
  "type": "upi",
  "upi_info": {
    "payment_address": "merchant@upi",
    "payee_name": "MerchantName",
    "amount": "100",
    "currency": "INR",
    "is_valid_format": true,
    "vpa_suffix_known": false,
    "warnings": []
  },
  "url_safety": null,
  "trust_score": 95,
  "rating": "SAFE",
  "checks": [
    { "label": "Valid UPI format", "passed": true },
    { "label": "Payee name present: MerchantName", "passed": true }
  ],
  "recommendation": "Looks good. You may proceed with this payment."
}
```

---

## Testing

Generate test QR codes using any UPI app (GPay, PhonePe, Paytm) or an online QR generator.

Test cases to cover:
- Valid GPay merchant QR → should be SAFE
- UPI QR without payee name → should be WARNING
- URL QR with a known phishing link → should be DANGEROUS
- Plain text QR → neutral result
- Blurry / rotated image → decoder tries multiple strategies
