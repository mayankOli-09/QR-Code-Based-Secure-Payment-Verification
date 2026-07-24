🔐 QR Pay Verifier — Secure QR Payment Verification System
<div align="center">

Scan. Analyze. Trust. — Before you pay.

QR Verification • Screenshot Analysis • OCR • Fraud Detection • URL Safety • Scan History • Real-Time Verification

Show Image Show Image Show Image Show Image Show Image Show Image Show Image

</div>
🎯 What is QR Pay Verifier?

QR Pay Verifier is a browser-based security tool that analyzes QR codes and payment screenshots before you complete a payment. Upload a QR code or payment receipt — the system decodes, analyzes, and gives you a clear verdict before you tap "Pay" or hand over goods.

⚠️ Don't scan first and regret later. Verify before you pay.

For QR Codes it:
Decodes the QR using multi-pass OpenCV processing
Identifies whether it is UPI / URL / Plain Text
Validates UPI ID, payee name, and known VPA suffixes
Checks embedded URLs against threat databases
Generates a Trust Score with SAFE / WARNING / DANGEROUS rating
For Payment Screenshots it:
Extracts all text using EasyOCR with multiple preprocessing passes
Detects payment app (Google Pay, PhonePe, Paytm, BHIM, etc.)
Extracts merchant name, UPI ID, transaction ID, amount, date & time
Checks image authenticity and quality
Produces a LIKELY REAL / SUSPICIOUS / LIKELY FAKE verdict
✨ Key Features
Feature	Description
🔍 QR Decoding	Decodes QR codes using OpenCV — no ZBar or pyzbar required
🧾 Screenshot Verification	Verifies Google Pay, PhonePe, Paytm, BHIM, and more
👁️ OCR Extraction	EasyOCR with grayscale, threshold, adaptive, and sharpen passes
🛡️ Fraud Detection	Multiple weighted security checks per scan
📊 Trust Score	0–100 confidence score with SAFE / WARNING / DANGEROUS rating
🌐 URL Safety Check	Offline heuristics + VirusTotal + Google Safe Browsing
✅ UPI Verification	Validates UPI format, payee name, VPA suffix, and amount
💰 Amount Detection	Extracts and validates payment amount from screenshots
🏪 Merchant Detection	Detects recipient / merchant name from receipts
🆔 Transaction Verification	Detects UPI reference numbers and app transaction IDs
📅 Date & Time Detection	Extracts payment date and time from screenshots
🕐 Scan History	Saves last 50 scans locally with verdict, score, and details
❓ FAQ	Built-in guide covering QR fraud, quishing, and safe payment practices
ℹ️ About	Explains how the tool works with real-world fraud examples
🏗️ Project Structure
QR Code-Based Secure Payment Verification/
│
├── v2/                          ← Active project
│   ├── main.py                  # FastAPI application & API endpoints
│   ├── qr_decoder.py            # OpenCV-based QR decoding (multi-pass)
│   ├── upi_parser.py            # UPI intent string parser
│   ├── url_checker.py           # URL safety checker
│   ├── fraud_detector.py        # QR fraud detection & trust scoring
│   ├── ss_checker.py            # Screenshot verification using EasyOCR
│   ├── app.js                   # Frontend logic (all tabs)
│   ├── style.css                # Styling
│   ├── index.html               # UI (QR, Screenshot, History, FAQ, About)
│   ├── reqt.txt                 # Python dependencies
│   └── venv/                    # Virtual environment
│
└── (Older Flask version — deprecated, not used)
⚙️ Installation
Prerequisites
Python 3.12+
VS Code with Live Server extension
Step 1 — Navigate to project folder
cmd
D:
cd "D:\College\Projects\QR Code-Based Secure Payment Verification\v2"
Step 2 — Activate virtual environment
cmd
..\venv\Scripts\activate

You should see (venv) appear in your prompt.

Step 3 — Install dependencies
cmd
pip install -r reqt.txt

Or manually:

cmd
pip install fastapi uvicorn opencv-python pillow numpy python-multipart python-dotenv easyocr torch torchvision
🚀 Running the Project
Start the backend
cmd
python main.py

You should see:

INFO:     Uvicorn running on http://0.0.0.0:8000

Keep this terminal open — the backend must stay running.

Open the frontend

Open index.html using Live Server in VS Code:

http://127.0.0.1:5500/v2/index.html
📸 How It Works
                      USER
                        │
            ┌───────────┴───────────┐
            │                       │
            ▼                       ▼
     Upload QR Code        Upload Payment Screenshot
            │                       │
            ▼                       ▼
   OpenCV QR Decoder      EasyOCR + Image Processing
            │                       │
            ▼                       ▼
   QR Classification       OCR Text Extraction
            │                       │
            ▼                       ▼
  UPI Parse / URL Check   Merchant, Amount & UPI Detection
            │                       │
            ▼                       ▼
   Fraud Detection        Screenshot Authenticity Checks
            └───────────┬───────────┘
                        ▼
               Security Analysis
                        │
                        ▼
            Trust Score / Verdict Generated
                        │
                        ▼
         SAFE ✅     WARNING ⚠️     DANGEROUS ❌
                        │
                        ▼
              Saved to Scan History 🕐
📊 Trust Score System
QR Verification
Factor	Effect on Score
✅ Valid UPI format	➕ Positive
✅ Payee name present	➕ Positive
✅ Known VPA suffix (bank/wallet)	➕ Positive
✅ Safe URL	➕ Positive
❌ Suspicious or phishing URL	➖ Negative
❌ Invalid UPI format	➖ Negative
❌ Missing payee name	➖ Negative
❌ Unusually large amount (>₹10,000)	➖ Negative
Screenshot Verification
Factor	Effect on Score
✅ Payment success keywords found	➕ Positive
✅ Valid transaction ID detected	➕ Positive
✅ Known payment app detected	➕ Positive
✅ Merchant name detected	➕ Positive
✅ UPI ID detected	➕ Positive
✅ Amount detected	➕ Positive
✅ Date & time detected	➕ Positive
✅ Good image quality	➕ Positive
❌ No transaction ID found	➖ Negative
❌ Low image sharpness	➖ Negative
❌ Failure / pending keywords	➖ Negative
Ratings
🟢  80 – 100   →   SAFE / LIKELY REAL
🟡  50 – 79    →   WARNING / SUSPICIOUS
🔴   0 – 49    →   DANGEROUS / LIKELY FAKE
🔌 API Reference

Base URL: http://127.0.0.1:8000

POST /verify

Accepts a QR code image and returns a full verification report.

Request: multipart/form-data — field: file

Response:

json
{
  "raw_data": "upi://pay?pa=merchant@axl&pn=Merchant&am=199&cu=INR",
  "type": "upi",
  "upi_info": {
    "payment_address": "merchant@axl",
    "payee_name": "Merchant",
    "amount": "199",
    "currency": "INR"
  },
  "url_safety": null,
  "trust_score": 95,
  "rating": "SAFE",
  "checks": [
    { "label": "Valid UPI format", "passed": true }
  ],
  "recommendation": "Looks good. You may proceed with this payment."
}
POST /verify-screenshot

Accepts a payment screenshot and returns an authenticity verdict.

Request: multipart/form-data — field: file

Response:

json
{
  "verdict": "LIKELY REAL",
  "confidence": 87,
  "merchant": "Airtel",
  "amount": "199",
  "transaction_id": "CICAg...",
  "upi_id": "airtelpay@axl",
  "app_detected": "Google Pay",
  "date": "19 Jul 2026",
  "time": "1:11 PM",
  "checks": [
    { "label": "Transaction ID found: CICAg...", "passed": true }
  ],
  "recommendation": "This screenshot appears to be a genuine payment receipt."
}
🧪 Test Cases
Input	Expected Result
Merchant UPI QR	Full UPI parsing + trust score
PhonePe / GPay / Paytm QR	Trust score with VPA verification
URL QR	URL safety analysis triggered
Plain Text QR	Classified as text, neutral score
Rotated QR (90°/180°/270°)	Successfully decoded via rotation passes
Blurry QR	Decoded via sharpening + upscaling
Google Pay Screenshot	OCR + full verification
PhonePe Screenshot	Merchant, amount & UPI detection
Paytm Screenshot	Transaction ID + date/time extraction
Edited / Fake Screenshot	Flagged as SUSPICIOUS or LIKELY FAKE
Screenshot without Transaction ID	Lower confidence score
🖥️ UI Tabs
Tab	Description
🔍 QR Verifier	Upload and verify QR code images
🧾 Screenshot Checker	Upload and verify payment screenshots
🕐 History	View last 50 scans with verdicts and details
❓ FAQ	Common questions about QR fraud, quishing, and safe payments
ℹ️ About	How the tool works, why it exists, and real fraud examples
🛠️ Tech Stack
Layer	Technology
Backend	Python 3.12, FastAPI, Uvicorn
QR Decoding	OpenCV QRCodeDetector (multi-pass)
OCR Engine	EasyOCR
Deep Learning	PyTorch (EasyOCR backend)
Image Processing	OpenCV, NumPy, Pillow
URL Safety	VirusTotal API, Google Safe Browsing API
Frontend	HTML5, CSS3, Vanilla JavaScript
Scan History	Browser localStorage (last 50 scans)
API Style	REST (multipart/form-data)
📝 Notes
QR decoding uses OpenCV's built-in QRCodeDetector — no ZBar or pyzbar required.
Screenshot verification uses EasyOCR with four preprocessing techniques: grayscale, Otsu thresholding, adaptive thresholding, and sharpening.
Supports receipts from Google Pay, PhonePe, Paytm, BHIM, Amazon Pay, Mobikwik, and Razorpay.
Scan history is stored entirely in the browser's localStorage — no data is sent to any external server.
URL safety optionally integrates with VirusTotal and Google Safe Browsing when API keys are configured in .env.
The older Flask version is deprecated and no longer maintained.
🤝 Contributing
bash
git checkout -b feature/your-feature-name
git commit -m "Add: your feature description"
git push origin feature/your-feature-name
# Open a Pull Request 🎉
<div align="center">

⭐ Star this repository if it helped you stay safe from QR payment fraud!

Scan Smart • Verify First • Pay Securely

Made with ❤️ using FastAPI • OpenCV • EasyOCR • Python

</div>
