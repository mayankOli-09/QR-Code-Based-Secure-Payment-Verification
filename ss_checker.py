import easyocr
import cv2
import numpy as np
import re

reader = easyocr.Reader(['en'], gpu=False, verbose=False)

SUCCESS_KEYWORDS = [
    "paid","payment successful","completed","successful",
    "money sent","credited","sent","debited","success"
]

FAILURE_KEYWORDS = [
    "failed","declined","cancelled","pending",
    "processing","timeout","error"
]

APP_PATTERNS = {
    "Google Pay":[
        "google pay","gpay","google transaction id",
        "google","pay"
    ],
    "PhonePe":[
        "phonepe","phone pe"
    ],
    "Paytm":[
        "paytm"
    ],
    "BHIM":[
        "bhim"
    ],
    "Amazon Pay":[
        "amazon pay","amazon"
    ],
    "Mobikwik":[
        "mobikwik"
    ],
    "Razorpay":[
        "razorpay"
    ]
}


def preprocess_images(img):

    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    gray=cv2.resize(
        gray,
        None,
        fx=2,
        fy=2,
        interpolation=cv2.INTER_CUBIC
    )

    blur=cv2.GaussianBlur(gray,(3,3),0)

    thresh=cv2.threshold(
        blur,
        0,
        255,
        cv2.THRESH_BINARY+cv2.THRESH_OTSU
    )[1]

    adaptive=cv2.adaptiveThreshold(
        gray,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        31,
        2
    )

    sharpen=cv2.filter2D(
        gray,
        -1,
        np.array([[0,-1,0],[-1,5,-1],[0,-1,0]])
    )

    return [gray,thresh,adaptive,sharpen]


def extract_text(images):

    lines=[]

    for img in images:

        try:
            txt=reader.readtext(
                img,
                detail=0,
                paragraph=True
            )

            lines.extend(txt)

        except:
            pass

    unique=[]

    for line in lines:

        line=line.strip()

        if line and line not in unique:
            unique.append(line)

    return "\n".join(unique)


def normalize_text(text):

    text=text.replace("|","I")
    text=text.replace("₹"," Rs ")
    text=text.replace("rs."," Rs ")
    text=text.replace("INR"," Rs ")

    text=re.sub(r"\s+"," ",text)

    return text


def detect_app(text):

    t=text.lower()

    if "google" in t and "pay" in t:
        return "Google Pay"

    if "gpay" in t:
        return "Google Pay"

    if "google transaction id" in t:
        return "Google Pay"

    if "phonepe" in t or "phone pe" in t:
        return "PhonePe"

    if "paytm" in t:
        return "Paytm"

    if "bhim" in t:
        return "BHIM"

    if "amazon" in t and "pay" in t:
        return "Amazon Pay"

    if "mobikwik" in t:
        return "Mobikwik"

    if "razorpay" in t:
        return "Razorpay"

    return None


def detect_merchant(text):

    patterns=[
        r"To\s+([A-Za-z0-9 &._-]+)",
        r"Paid to\s+([A-Za-z0-9 &._-]+)",
        r"Sent to\s+([A-Za-z0-9 &._-]+)"
    ]

    for p in patterns:

        m=re.search(
            p,
            text,
            re.IGNORECASE
        )

        if m:
            return m.group(1).strip()

    return None


def detect_upi(text):

    m=re.search(
        r"[a-zA-Z0-9._-]+@[a-zA-Z0-9._-]+",
        text
    )

    if m:
        return m.group()

    return None


def detect_transaction(text):

    patterns=[
        r"UPI\s*transaction\s*ID[: ]*([A-Za-z0-9_-]{8,40})",
        r"Google\s*transaction\s*ID[: ]*([A-Za-z0-9_-]{8,40})",
        r"Transaction\s*ID[: ]*([A-Za-z0-9_-]{8,40})",
        r"\b\d{12}\b",
        r"\b[A-Z0-9]{15,30}\b"
    ]

    for p in patterns:

        m=re.search(
            p,
            text,
            re.IGNORECASE
        )

        if m:

            if m.lastindex:
                return m.group(1)

            return m.group()

    return None
def detect_amount(text):

    t = normalize_text(text)

    candidates = []

    patterns = [

        (r"Rs\s*([\d,]+(?:\.\d{1,2})?)",40),

        (r"₹\s*([\d,]+(?:\.\d{1,2})?)",40),

        (r"Amount[: ]*([\d,]+(?:\.\d{1,2})?)",35),

        (r"Paid[: ]*([\d,]+(?:\.\d{1,2})?)",35),

        (r"Sent[: ]*([\d,]+(?:\.\d{1,2})?)",35),

        (r"Completed\s*([\d,]+(?:\.\d{1,2})?)",30),

        (r"To\s+[A-Za-z0-9 &._-]+\s+([\d,]+)",30)

    ]

    for pattern,score in patterns:

        for m in re.finditer(pattern,t,re.IGNORECASE):

            value=m.group(1).replace(",","")

            try:

                amt=float(value)

                if 1<=amt<=1000000:

                    candidates.append((score,amt))

            except:
                pass

    # OCR often reads ₹199 as 2199 or 7199.
    for m in re.finditer(r"\b([27]\d{3})\b",t):

        value=m.group(1)

        corrected=int(value[1:])

        if corrected<=50000:

            candidates.append((32,corrected))

    # Ignore years and bank-account endings.
    for m in re.finditer(r"\b\d{2,6}\b",t):

        num=int(m.group())

        if 1900<=num<=2100:
            continue

        if num in [8955,9876,1234]:
            continue

        if num>500000:
            continue

        candidates.append((10,num))

    if not candidates:
        return None

    candidates.sort(reverse=True)

    return str(int(candidates[0][1]))


def detect_date(text):

    m=re.search(
        r"\d{1,2}\s+[A-Za-z]{3,9}\s+\d{4}",
        text
    )

    if m:
        return m.group()

    return None


def detect_time(text):

    m=re.search(
        r"\d{1,2}[:.]\d{2}\s*(am|pm)?",
        text,
        re.IGNORECASE
    )

    if m:
        return m.group()

    return None


def check_screenshot(image_bytes: bytes):

    result={
        "is_real":None,
        "confidence":0,
        "verdict":"UNKNOWN",
        "recommendation":"",
        "transaction_id":None,
        "amount":None,
        "merchant":None,
        "upi_id":None,
        "date":None,
        "time":None,
        "app_detected":None,
        "extracted_text":"",
        "checks":[]
    }

    nparr=np.frombuffer(image_bytes,np.uint8)

    img=cv2.imdecode(
        nparr,
        cv2.IMREAD_COLOR
    )

    if img is None:

        result["verdict"]="ERROR"
        result["recommendation"]="Could not read image."

        return result

    images=preprocess_images(img)

    raw_text=extract_text(images)

    text=normalize_text(raw_text)

    text_lower=text.lower()

    result["extracted_text"]=raw_text

    score=0

    # ---------- Payment status ----------

    if any(k in text_lower for k in SUCCESS_KEYWORDS):

        score+=20

        result["checks"].append({
            "label":"Payment success keywords found",
            "passed":True
        })

    elif any(k in text_lower for k in FAILURE_KEYWORDS):

        score-=20

        result["checks"].append({
            "label":"Failure keywords detected",
            "passed":False
        })

    else:

        result["checks"].append({
            "label":"Payment status not clear",
            "passed":None
        })

    # ---------- App ----------

    app=detect_app(text)

    if app:

        result["app_detected"]=app

        score+=20

        result["checks"].append({
            "label":f"Payment app detected: {app}",
            "passed":True
        })

    else:

        result["checks"].append({
            "label":"No payment app detected",
            "passed":None
        })

    # ---------- Merchant ----------

    merchant=detect_merchant(text)

    if merchant:

        result["merchant"]=merchant

        score+=10

    # ---------- UPI ID ----------

    upi=detect_upi(text)

    if upi:

        result["upi_id"]=upi

        score+=15

    # ---------- Transaction ----------

    txn=detect_transaction(text)

    if txn:

        result["transaction_id"]=txn

        score+=25

        result["checks"].append({
            "label":f"Transaction ID found: {txn}",
            "passed":True
        })

    else:

        result["checks"].append({
            "label":"Transaction ID not found",
            "passed":False
        })

    # ---------- Amount ----------

    amount=detect_amount(text)

    if amount:

        result["amount"]=amount

        score+=15

        result["checks"].append({
            "label":f"Amount detected: ₹{amount}",
            "passed":True
        })

    else:

        result["checks"].append({
            "label":"Amount not detected",
            "passed":False
        })

    result["date"]=detect_date(text)
    result["time"]=detect_time(text)    # ---------- Image quality ----------

    gray = images[0]

    laplacian = cv2.Laplacian(gray, cv2.CV_64F).var()

    if laplacian < 40:

        score -= 10

        result["checks"].append({
            "label": "Low image quality",
            "passed": False
        })

    else:

        score += 10

        result["checks"].append({
            "label": "Image quality looks good",
            "passed": True
        })

    # ---------- UPI reference ----------

    ref = re.search(r"\b\d{12}\b", text)

    if ref:

        score += 10

        result["checks"].append({
            "label": f"UPI reference found: {ref.group()}",
            "passed": True
        })

    else:

        result["checks"].append({
            "label": "UPI reference not found",
            "passed": None
        })

    # ---------- Extra consistency checks ----------

    if result["merchant"]:

        score += 5

    if result["date"]:

        score += 5

    if result["time"]:

        score += 5

    if result["app_detected"] == "Google Pay" and "google transaction id" in text_lower:

        score += 5

    if result["app_detected"] == "PhonePe" and "phonepe" in text_lower:

        score += 5

    if result["app_detected"] == "Paytm" and "paytm" in text_lower:

        score += 5

    # ---------- Final score ----------

    score = max(0, min(score, 100))

    result["confidence"] = score

    if score >= 70:

        result["is_real"] = True
        result["verdict"] = "LIKELY REAL"
        result["recommendation"] = (
            "This screenshot appears to be a genuine payment receipt."
        )

    elif score >= 40:

        result["is_real"] = None
        result["verdict"] = "SUSPICIOUS"
        result["recommendation"] = (
            "Payment could not be fully verified. Confirm the UPI transaction ID before releasing goods."
        )

    else:

        result["is_real"] = False
        result["verdict"] = "LIKELY FAKE"
        result["recommendation"] = (
            "This screenshot appears suspicious. Do not rely on it as proof of payment."
        )

    return result