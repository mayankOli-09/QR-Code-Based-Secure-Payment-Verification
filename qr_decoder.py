import cv2
import numpy as np
from PIL import Image
import io


def decode_qr(image_bytes: bytes) -> str | None:
    nparr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    if img is None:
        try:
            pil_img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
            img = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)
        except Exception:
            return None

    detector = cv2.QRCodeDetector()

    # 1. Original color
    data, _, _ = detector.detectAndDecode(img)
    if data:
        return data.strip()

    # 2. Grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    data, _, _ = detector.detectAndDecode(gray)
    if data:
        return data.strip()

    # 3. Sharpened (helps blurry QRs)
    kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
    sharpened = cv2.filter2D(gray, -1, kernel)
    data, _, _ = detector.detectAndDecode(sharpened)
    if data:
        return data.strip()

    # 4. Enlarged 2x
    enlarged = cv2.resize(img, None, fx=2, fy=2)
    data, _, _ = detector.detectAndDecode(enlarged)
    if data:
        return data.strip()

    # 5. Rotations (90, 180, 270)
    rotation_map = {
        90:  cv2.ROTATE_90_CLOCKWISE,
        180: cv2.ROTATE_180,
        270: cv2.ROTATE_90_COUNTERCLOCKWISE,
    }
    for angle, flag in rotation_map.items():
        rotated = cv2.rotate(img, flag)
        data, _, _ = detector.detectAndDecode(rotated)
        if data:
            return data.strip()

    return None