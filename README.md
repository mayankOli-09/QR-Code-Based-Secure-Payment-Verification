# 🔐 QR Pay Verifier — Secure QR Payment Verification System

<div align="center">

**Scan. Analyze. Trust. — Before you pay.**

*UPI Detection • Fraud Scoring • URL Safety • Real-Time Verification*

[![Python](https://img.shields.io/badge/Python-3.12+-blue?logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-teal?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![OpenCV](https://img.shields.io/badge/OpenCV-4.9+-red?logo=opencv&logoColor=white)](https://opencv.org)
[![JavaScript](https://img.shields.io/badge/Frontend-Vanilla%20JS-yellow?logo=javascript)](https://developer.mozilla.org/en-US/docs/Web/JavaScript)
[![License](https://img.shields.io/badge/License-MIT-lightgrey)](LICENSE)

</div>

---

## 🎯 What is QR Pay Verifier?

**QR Pay Verifier** is a browser-based security tool that analyzes QR codes before you complete a payment. Upload any QR code image — the system decodes it, classifies it (UPI, URL, or plain text), runs multiple fraud checks, and gives you a **trust score** so you know whether it's safe to pay.

> ⚠️ **Don't scan first and regret later. Verify before you pay.**

---

## ✨ Key Features

| Feature | Description |
|---|---|
| 🔍 **QR Decoding** | Decodes QR codes using OpenCV — no ZBar or pyzbar needed |
| 🧠 **Smart Classification** | Identifies UPI payment QRs, URLs, and plain text automatically |
| 🛡️ **Fraud Detection** | Runs multiple security checks and flags suspicious patterns |
| 📊 **Trust Score** | Calculates a 0–100 score with SAFE / WARNING / DANGEROUS rating |
| 🌐 **URL Safety Check** | Scans embedded URLs for phishing or malicious patterns |
| ✅ **UPI Verification** | Extracts and validates payee name, UPI ID, amount, and currency |

---

## 🏗️ Project Structure

```
QR Code-Based Secure Payment Verification/
│
├── v2/                        ← Active project
│   ├── main.py                # FastAPI app entry point
│   ├── qr_decoder.py          # OpenCV-based QR decoding
│   ├── upi_parser.py          # UPI intent string parser
│   ├── url_checker.py         # URL safety checker
│   ├── fraud_detector.py      # Fraud detection & trust scoring
│   ├── app.js                 # Frontend logic
│   ├── style.css              # Styling
│   ├── index.html             # Main UI
│   ├── req.txt                # Python dependencies
│   └── venv/                  # Virtual environment
│
└── (Older Flask version — deprecated, not used)
```

---

## ⚙️ Installation

### Prerequisites
- Python 3.12+
- VS Code with Live Server extension

---

### Step 1 — Open Command Prompt

```cmd
D:
cd "D:\College\Projects\QR Code-Based Secure Payment Verification\v2"
```

---

### Step 2 — Activate Virtual Environment

```cmd
..\venv\Scripts\activate
```

You should see `(venv)` appear before your prompt — this means it's active.

---

### Step 3 — Install Dependencies

```cmd
pip install -r req.txt
```

Or manually:

```cmd
pip install fastapi uvicorn opencv-python pillow numpy python-multipart requests python-dotenv
```

---

## 🚀 Running the Project

### Start the Backend

```cmd
python main.py
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
```

> Keep this terminal open — the backend must stay running.

---

### Open the Frontend

Open `v2/index.html` using **Live Server** in VS Code.

Your browser URL should look like:
```
http://127.0.0.1:5500/v2/index.html
```

---

## 📸 How It Works

```
 📷  User uploads a QR code image
        │
        ▼
 🧩  OpenCV decodes the QR code → extracts raw text
        │
        ▼
 🔎  Classifier identifies type: UPI | URL | Plain Text
        │
        ▼
 📋  UPI parser extracts → pa, pn, am, cu fields
 🌐  URL checker scans for phishing / suspicious patterns
        │
        ▼
 🕵️  Fraud detector runs all security checks
        │
        ▼
 📊  Trust score calculated (0–100)
        │
        ▼
 🚦  Frontend displays verdict: SAFE ✅ | WARNING ⚠️ | DANGEROUS ❌
```

---

## 📊 Trust Score System

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

### Ratings

```
🟢  80 – 100   →   SAFE
🟡  50 – 79    →   WARNING
🔴   0 – 49    →   DANGEROUS
```

---

## 🔌 API Reference

**Base URL:** `http://127.0.0.1:8000`

### `POST /verify`

Accepts a QR code image and returns a full verification report.

**Request:** `multipart/form-data` with field `file` (image upload)

**Response Example:**

```json
{
  "raw_data": "upi://pay?pa=merchant@upi&pn=Merchant&am=100&cu=INR",
  "type": "upi",
  "upi_info": {
    "payment_address": "merchant@upi",
    "payee_name": "Merchant",
    "amount": "100",
    "currency": "INR"
  },
  "url_safety": null,
  "trust_score": 95,
  "rating": "SAFE",
  "checks": [
    { "label": "Valid UPI Format", "passed": true }
  ],
  "recommendation": "Looks safe. You may proceed."
}
```

---

## 🧪 Test Cases

Try the verifier with these QR types to explore all scenarios:

| QR Type | Expected Behaviour |
|---|---|
| PhonePe / GPay / Paytm QR | Full UPI parse + trust score |
| Merchant UPI QR | Payee name + address verification |
| Plain Text QR | Classified as text, basic checks |
| URL QR | URL safety scan triggered |
| Rotated QR image | OpenCV handles rotation automatically |
| Blurry QR image | Tests decoder robustness |

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **Backend** | Python 3.12, FastAPI, Uvicorn |
| **QR Decoding** | OpenCV `QRCodeDetector` |
| **Image Processing** | NumPy, Pillow |
| **Frontend** | HTML5, CSS3, Vanilla JavaScript |
| **API Style** | REST (multipart/form-data) |

---

## 📝 Notes

- QR decoding uses OpenCV's built-in `QRCodeDetector` — no ZBar or `pyzbar` installation required.
- The older Flask version in the root folder is deprecated and no longer maintained.
- Frontend communicates with the FastAPI backend through REST API calls.
- `.env` file is used for any configurable environment variables.

---

## 🤝 Contributing

```bash
git checkout -b feature/your-feature-name
git commit -m "Add: your feature description"
git push origin feature/your-feature-name
# Open a Pull Request 🎉
```

---

<div align="center">

⭐ **Star this repo if it helped you stay safe from QR payment fraud!**

*Scan smart. Pay secure. Stay safe.*

</div>
