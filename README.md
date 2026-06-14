# 🔐 QR Payment Verification — Secure QR-Based Payment Verifier

<div align="center">

**Detect fraudulent QR codes & verify payments before you tap "Pay"**

*UPI Verification • Fraud Detection • URL Safety • Tamper-Proof QR*

[![Made with HTML](https://img.shields.io/badge/Made%20with-HTML5-orange?logo=html5)](https://developer.mozilla.org/en-US/docs/Web/HTML)
[![Made with CSS](https://img.shields.io/badge/Styled%20with-CSS3-blue?logo=css3)](https://developer.mozilla.org/en-US/docs/Web/CSS)
[![Made with JS](https://img.shields.io/badge/Logic-JavaScript-yellow?logo=javascript)](https://developer.mozilla.org/en-US/docs/Web/JavaScript)
[![UPI](https://img.shields.io/badge/Supports-UPI%20QR-green?logo=googlepay)](https://www.npci.org.in/what-we-do/upi/product-overview)

</div>

---

## 🎯 What is QR Payment Verification?

**QR Payment Verification** is a lightweight, fully client-side web tool built to fight one of the fastest-growing scams in digital payments — **fake or tampered QR codes**.

Scammers swap genuine merchant QR codes with malicious ones, redirect payments to the wrong UPI ID, or send fake "payment successful" screenshots to dupe sellers. This tool lets you **scan, verify, and trust** a QR code *before* you complete a transaction — and helps merchants verify tamper-proof payment proofs *after*.

> ⚠️ **No more "Sorry, I sent it, check again" scams. Verify first, pay second.**

---

## ✨ Key Features

| Function | How It Works |
|---|---|
| 🔍 **Scan & Validate QR Codes** | Extracts embedded data (UPI intent string or URL) from any QR code and parses it for analysis |
| 🛡️ **Fraud Detection** | Flags fraudulent, tampered, or known-scam QR patterns before you proceed with payment |
| ✅ **Recipient Verification** | Cross-checks the UPI payee name (`pn`) against the UPI ID (`pa`) to confirm who you're *really* paying |
| 🌐 **URL Safety Check** | Scans embedded URLs against suspicious-pattern heuristics to catch phishing redirects |
| 🔏 **Tamper-Proof Receipts** | Validates digitally signed QR codes attached to payment screenshots, so merchants can confirm a transaction is genuine — not photoshopped |

---

## 🏗️ Project Structure

qr-payment-verification
index.html           # Main UI

style.css            # Styling & layout

app.js               # Core application logic & UI controller

upi-parser.js        # Parses UPI intent strings (pa, pn, am, etc.)

url-safety.js         # Checks embedded URLs for phishing/red flags

fraud-detection.js    # Cross-checks data against fraud heuristics

test-qr-codes/        # Sample QR images for testing

README.md             # Documentation


---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **Frontend** | HTML5, CSS3, Vanilla JavaScript |
| **QR Decoding** | Client-side QR image scanning |
| **UPI Parsing** | Custom UPI deep-link parser (`upi://pay?...`) |
| **Security Engine** | URL Safety Checker + Fraud Detection heuristics |
| **Proof of Authenticity** | Digital signature validation for tamper-proof receipts |

---

## 📸 How It Works

 📷  User uploads or scans a QR code
 
        │
        ▼
 🧩  QR data is decoded → UPI intent string or raw URL
 
        │
        ▼
 🌐  url-safety.js checks for phishing / malicious link patterns
        
        │
        ▼
 🕵️  fraud-detection.js checks for tampering & known scam signatures
        
        │
        ▼
 ✅  upi-parser.js verifies payee name (pn) matches UPI ID (pa)
        
        │
        ▼
 🚦  User sees a clear verdict:  SAFE ✅ | SUSPICIOUS ⚠️ | FRAUD ❌

---

## 🔮 Roadmap

- [ ] Live camera-based QR scanning
- [ ] Database of known scam UPI IDs (community-reported)
- [ ] Browser extension version
- [ ] Multi-language support

---
\`\`\`


<div align="center">

⭐ **If this project helped you spot a scam, star the repo and share it!** ⭐

*Stay safe. Scan smart. Pay secure.*

</div>
