import cv2
import numpy as np
from pyzbar.pyzbar import decode
from PIL import Image
import io


def decode_qr(image_bytes: bytes) -> str | None:
    """
    Decode a QR code from image bytes.
    Returns the decoded string, or None if no QR code found.
    Tries multiple preprocessing strategies for robustness.
    """
    # Convert bytes to numpy array
    nparr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    if img is None:
        # Fallback to PIL
        try:
            pil_img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
            img = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)
        except Exception:
            return None

    strategies = [
        lambda i: i,                                        # Original
        lambda i: cv2.cvtColor(i, cv2.COLOR_BGR2GRAY),    # Grayscale
        lambda i: _sharpen(i),                              # Sharpened
        lambda i: cv2.resize(i, None, fx=2, fy=2),        # Upscaled 2x
        lambda i: _adaptive_threshold(i),                   # Adaptive threshold
    ]

    for strategy in strategies:
        try:
            processed = strategy(img)
            codes = decode(processed)
            if codes:
                return codes[0].data.decode("utf-8").strip()
        except Exception:
            continue

    return None


def _sharpen(img):
    kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
    return cv2.filter2D(img, -1, kernel)


def _adaptive_threshold(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                  cv2.THRESH_BINARY, 11, 2)