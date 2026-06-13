🔐 QR Payment Verification — Secure QR-Based Payment Verifier

<div align="center">
Detect fraudulent QR codes and verify payments before you pay

UPI Verification • Fraud Detection • URL Safety • Tamper-Proof QR

</div>

🎯 What is QR Payment Verification?

QR Payment Verification is a lightweight web-based tool that helps users scan and validate payment QR codes before completing a transaction. It checks UPI details, detects tampered or fraudulent QR codes, verifies the recipient's identity, and supports tamper-proof, digitally signed QR codes for safer merchant verification.

No more falling for fake payment screenshots or malicious QR codes — verify first, pay second.


✨ Key Features

FunctionHow It Works🔍 Scans & Validates QR CodesExtracts data (URL or UPI details) from the QR code and analyzes it for security issues🛡️ Prevents FraudDetects fraudulent or tampered QR codes before you complete the transaction✅ Verifies RecipientConfirms the UPI payee name matches the intended recipient🔏 Tamper-Proof ProofSupports digitally signed QR codes added to payment screenshots so merchants can verify authenticity


🚀 Quick Start

Prerequisites


A modern web browser (Chrome, Firefox, Edge)
No backend or server setup required — runs entirely client-side


Setup & Run

bash# 1. Clone the repository
git clone https://github.com/your-username/qr-payment-verification.git
cd qr-payment-verification

# 2. Open in browser
open index.html

That's it — no build step, no dependencies to install!


🏗️ Project Structure

qr-payment-verification/
├── index.html          # Main UI
├── style.css           # Styling
├── app.js              # Main logic
├── upi-parser.js        # UPI QR parsing logic
├── url-safety.js        # URL safety checker
├── fraud-detection.js   # Fraud detection logic
├── test-qr-codes/       # Test QR images folder
└── README.md            # Documentation


🛠️ Tech Stack

LayerTechnologyFrontendHTML, CSS, JavaScriptQR ParsingUPI Deep Link Parser (custom JS)Security ChecksURL Safety Checker, Fraud Detection EngineVerificationDigital Signature Validation (for tamper-proof QR)


📸 How It Works

User uploads/scans a QR code
        ↓
App extracts QR data (UPI ID, amount, payee name, or URL)
        ↓
URL Safety Checker scans for suspicious/malicious links
        ↓
Fraud Detection module checks for tampering & known scam patterns
        ↓
Recipient name is verified against UPI payee details
        ↓
User sees a clear safe/unsafe verdict before paying


🤝 Contributing

Contributions are welcome! Here's how:

bash# Fork the repo, then:
git checkout -b feature/your-feature-name
git commit -m "Add: your feature description"
git push origin feature/your-feature-name
# Open a Pull Request 🎉


<div align="center">
⭐ Star this repo if it helped you stay safe from QR payment fraud!

</div>
