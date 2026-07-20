from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
from urllib.parse import urlparse, parse_qs
import uvicorn
from qr_decoder import decode_qr
from upi_parser import parse_upi
from url_checker import check_url_safety
from fraud_detector import assess_risk
from ss_checker import check_screenshot

load_dotenv()

app = FastAPI(title="QR Payment Verifier", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"status": "QR Payment Verifier API is running"}


@app.post("/verify")
async def verify_qr(file: UploadFile = File(...)):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Only image files are accepted.")

    image_bytes = await file.read()

    decoded_data = decode_qr(image_bytes)
    if not decoded_data:
        raise HTTPException(status_code=422, detail="No QR code found in the image.")

    upi_info = None
    url_safety = None

    if decoded_data.lower().startswith("upi://"):
        upi_info = parse_upi(decoded_data)
        params = parse_qs(urlparse(decoded_data).query)
        redirect_url = params.get("url", [None])[0]
        if redirect_url:
            url_safety = await check_url_safety(redirect_url)
    elif decoded_data.startswith("http://") or decoded_data.startswith("https://"):
        url_safety = await check_url_safety(decoded_data)

    result = assess_risk(decoded_data, upi_info, url_safety)

    return JSONResponse(content={
        "raw_data": decoded_data,
        "type": "upi" if upi_info else ("url" if url_safety else "text"),
        "upi_info": upi_info,
        "url_safety": url_safety,
        "trust_score": result["trust_score"],
        "rating": result["rating"],
        "checks": result["checks"],
        "recommendation": result["recommendation"],
    })


@app.post("/verify-screenshot")
async def verify_screenshot(file: UploadFile = File(...)):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Only image files are accepted.")

    image_bytes = await file.read()
    result = check_screenshot(image_bytes)

    return JSONResponse(content=result)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)