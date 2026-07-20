# 🔐 QR Pay Verifier — Secure QR Payment Verification System

<div align="center">

**Scan. Analyze. Trust. — Before you pay.**

*QR Verification • Payment Screenshot Analysis • OCR • Fraud Detection • URL Safety • Real-Time Verification*

[![Python](https://img.shields.io/badge/Python-3.12+-blue?logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-teal?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![OpenCV](https://img.shields.io/badge/OpenCV-4.9+-red?logo=opencv&logoColor=white)](https://opencv.org)
[![EasyOCR](https://img.shields.io/badge/EasyOCR-Latest-green)](https://github.com/JaidedAI/EasyOCR)
[![PyTorch](https://img.shields.io/badge/PyTorch-Deep%20Learning-orange?logo=pytorch)](https://pytorch.org)
[![JavaScript](https://img.shields.io/badge/Frontend-Vanilla%20JS-yellow?logo=javascript)](https://developer.mozilla.org/en-US/docs/Web/JavaScript)
[![License](https://img.shields.io/badge/License-MIT-lightgrey)](LICENSE)

</div>

---

# 🎯 What is QR Pay Verifier?

**QR Pay Verifier** is a browser-based security tool that analyzes **QR codes and payment screenshots** before you complete a payment.

Upload either:

- 📷 A QR Code
- 🧾 A Payment Screenshot

The system automatically determines which type has been uploaded and performs the appropriate verification.

For QR codes it:

- Decodes the QR
- Identifies whether it is UPI / URL / Text
- Performs fraud analysis
- Generates a trust score

For payment screenshots it:

- Extracts text using OCR
- Detects payment app
- Detects merchant
- Detects UPI ID
- Detects transaction ID
- Detects payment amount
- Detects date & time
- Checks screenshot authenticity
- Produces a verification verdict

> ⚠️ **Don't scan first and regret later. Verify before you pay.**

---

# ✨ Key Features

| Feature | Description |
|---|---|
| 🔍 **QR Decoding** | Decodes QR codes using OpenCV without requiring ZBar or pyzbar |
| 🧾 **Payment Screenshot Verification** | Verify Google Pay, PhonePe, Paytm and other payment screenshots |
| 👁️ **OCR Extraction** | Uses EasyOCR with multiple preprocessing techniques |
| 🧠 **Automatic Detection** | Detects whether uploaded image is a QR code or payment screenshot |
| 🛡️ **Fraud Detection** | Performs multiple security checks |
| 📊 **Trust Score** | Generates confidence score and rating |
| 🌐 **URL Safety Check** | Detects suspicious or phishing URLs |
| ✅ **UPI Verification** | Validates UPI details from QR codes |
| 💰 **Amount Detection** | Extracts payment amount from screenshots |
| 🏪 **Merchant Detection** | Detects recipient/merchant name |
| 🆔 **Transaction Verification** | Detects UPI and Google transaction IDs |
| 📅 **Date & Time Detection** | Extracts payment date and time |
| 🖼️ **Image Quality Check** | Detects poor-quality or suspicious screenshots |

---

# 🏗️ Project Structure

```
QR Code-Based Secure Payment Verification/
│
├── v2/
│   ├── main.py                # FastAPI application
│   ├── qr_decoder.py          # QR Decoder
│   ├── upi_parser.py          # UPI Parser
│   ├── url_checker.py         # URL Safety Checker
│   ├── fraud_detector.py      # QR Fraud Detection
│   ├── ss_checker.py          # Screenshot Verification using EasyOCR
│   ├── app.js                 # Frontend Logic
│   ├── style.css              # Styling
│   ├── index.html             # UI
│   ├── req.txt                # Dependencies
│   └── venv/
│
└── Older Flask version (Deprecated)
```

---

# ⚙️ Installation

## Prerequisites

- Python 3.12+
- VS Code
- Live Server Extension

---

## Step 1

```cmd
D:
cd "D:\College\Projects\QR Code-Based Secure Payment Verification\v2"
```

---

## Step 2

Activate the virtual environment.

```cmd
..\venv\Scripts\activate
```

You should now see

```
(venv)
```

---

## Step 3

Install dependencies.

```cmd
pip install -r req.txt
```

or

```cmd
pip install fastapi uvicorn opencv-python pillow numpy python-multipart python-dotenv easyocr torch torchvision
```

---

## Running the Project

Start the backend.

```cmd
python main.py
```

You should see

```
INFO: Uvicorn running on http://0.0.0.0:8000
```

Keep this terminal running.

Open **index.html** using Live Server.

Example:

```
http://127.0.0.1:5500/v2/index.html
```

---
# 📸 How It Works

```
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
 QR Classification      OCR Text Extraction
          │                       │
          ▼                       ▼
UPI Parsing / URL Check Merchant, Amount & UPI Detection
          │                       │
          ▼                       ▼
 Fraud Detection      Screenshot Authenticity Checks
          └───────────┬───────────┘
                      ▼
             Security Analysis
                      │
                      ▼
          Trust Score / Verdict Generated
                      │
                      ▼
      SAFE ✅   WARNING ⚠️   DANGEROUS ❌
```

---

# 📊 Trust Score System

## QR Verification

| Factor | Effect on Score |
|---|---|
| ✅ Valid UPI format | ➕ Positive |
| ✅ Payee name present | ➕ Positive |
| ✅ Valid UPI ID | ➕ Positive |
| ✅ Safe URL | ➕ Positive |
| ❌ Suspicious URL | ➖ Negative |
| ❌ Invalid UPI format | ➖ Negative |
| ❌ Missing payee name | ➖ Negative |
| ❌ Unusually large amount | ➖ Negative |

---

## Screenshot Verification

| Factor | Effect |
|---|---|
| ✅ Payment success keywords | ➕ Positive |
| ✅ Valid transaction ID | ➕ Positive |
| ✅ Payment app detected | ➕ Positive |
| ✅ Merchant detected | ➕ Positive |
| ✅ UPI ID detected | ➕ Positive |
| ✅ Amount detected | ➕ Positive |
| ✅ Date & Time detected | ➕ Positive |
| ✅ Good image quality | ➕ Positive |
| ❌ Missing transaction ID | ➖ Negative |
| ❌ Low image quality | ➖ Negative |
| ❌ Failure / Pending keywords | ➖ Negative |

---

## Ratings

```
🟢 80 – 100 → SAFE
🟡 50 – 79  → WARNING
🔴 0 – 49   → DANGEROUS
```

---

# 🔌 API Reference

Base URL

```
http://127.0.0.1:8000
```

---

## POST /verify

Accepts a QR Code image.

### Request

```
multipart/form-data
field : file
```

### Response

```json
{
  "raw_data":"upi://pay?...",
  "type":"upi",
  "upi_info":{},
  "trust_score":95,
  "rating":"SAFE",
  "checks":[],
  "recommendation":"Looks safe."
}
```

---

## POST /verify-screenshot

Accepts a payment screenshot.

### Request

```
multipart/form-data
field : file
```

### Response

```json
{
    "verdict":"LIKELY REAL",
    "confidence":87,
    "merchant":"Airtel",
    "amount":"199",
    "transaction_id":"CICAg...",
    "upi_id":"airtelpay@...",
    "app_detected":"Google Pay",
    "date":"19 Jul 2026",
    "time":"1:11 PM",
    "checks":[]
}
```

---

# 🧪 Test Cases

| Input | Expected Result |
|---|---|
| Merchant UPI QR | Successful UPI parsing |
| PhonePe QR | Trust score generated |
| Google Pay QR | Trust score generated |
| Paytm QR | Trust score generated |
| URL QR | URL safety analysis |
| Plain Text QR | Classified as text |
| Rotated QR | Successfully decoded |
| Blurry QR | Decoder robustness test |
| Google Pay Screenshot | OCR + verification |
| PhonePe Screenshot | Merchant, amount & UPI detection |
| Paytm Screenshot | Transaction verification |
| Edited Screenshot | Flagged as suspicious |
| Screenshot without Transaction ID | Lower confidence |

---

# 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python 3.12, FastAPI, Uvicorn |
| QR Detection | OpenCV QRCodeDetector |
| OCR Engine | EasyOCR |
| Deep Learning | PyTorch |
| Image Processing | OpenCV, NumPy, Pillow |
| Frontend | HTML5, CSS3, Vanilla JavaScript |
| API Style | REST API |

---

# 📝 Notes

- QR decoding uses OpenCV's built-in `QRCodeDetector`; no ZBar or `pyzbar` installation is required.
- Payment screenshots are analyzed using **EasyOCR** with multiple image preprocessing techniques.
- OCR extracts merchant name, payment amount, UPI ID, transaction ID, payment date and payment time.
- Multiple preprocessing methods (grayscale conversion, thresholding, adaptive thresholding and sharpening) improve OCR accuracy.
- Screenshot verification supports receipts from Google Pay, PhonePe, Paytm, BHIM, Amazon Pay and Razorpay.
- Frontend communicates with the FastAPI backend using REST APIs.
- The older Flask version is deprecated and no longer maintained.
- Environment-specific configuration can be managed using the `.env` file.

---

# 🤝 Contributing

```bash
git checkout -b feature/your-feature-name
git commit -m "Add: your feature description"
git push origin feature/your-feature-name
```

Open a Pull Request 🎉

---

<div align="center">

⭐ **Star this repository if it helped you stay safe from QR payment fraud!**

**Scan Smart • Verify First • Pay Securely**

Made with ❤️ using **FastAPI**, **OpenCV**, **EasyOCR**, and **Python**.

</div>
