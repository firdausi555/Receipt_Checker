from fastapi import FastAPI, UploadFile, File, HTTPException, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.database import init_db, SessionLocal, ReceiptFile, Receipt
from app.ocr import extract_receipt_data
import os
import shutil
from datetime import datetime

app = FastAPI(title="Receipt Checker")

UPLOAD_DIR = "uploaded_receipts"
os.makedirs(UPLOAD_DIR, exist_ok=True)

init_db()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/upload")
async def upload_receipt(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")


    receipt_file = db.query(ReceiptFile).filter(ReceiptFile.file_name == file.filename).first()
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    if receipt_file:
        receipt_file.file_path = file_path
        receipt_file.is_valid = False
        receipt_file.invalid_reason = None
        receipt_file.is_processed = False
        receipt_file.updated_at = datetime.utcnow()
    else:
        receipt_file = ReceiptFile(
            file_name=file.filename,
            file_path=file_path,
            is_valid=False,
            is_processed=False,
        )
        db.add(receipt_file)
    db.commit()
    db.refresh(receipt_file)
    return {"message": "File uploaded successfully", "id": receipt_file.id}


@app.post("/validate")
def validate_file(id: int, db: Session = Depends(get_db)):
    receipt_file = db.query(ReceiptFile).filter(ReceiptFile.id == id).first()
    if not receipt_file:
        raise HTTPException(status_code=404, detail="Receipt file not found")


    try:
        with open(receipt_file.file_path, "rb") as f:
            header = f.read(4)
        if header != b"%PDF":
            receipt_file.is_valid = False
            receipt_file.invalid_reason = "Invalid PDF header"
        else:
            receipt_file.is_valid = True
            receipt_file.invalid_reason = None
    except Exception as e:
        receipt_file.is_valid = False
        receipt_file.invalid_reason = f"Error reading file: {str(e)}"

    receipt_file.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(receipt_file)

    return {
        "id": receipt_file.id,
        "file_name": receipt_file.file_name,
        "is_valid": receipt_file.is_valid,
        "invalid_reason": receipt_file.invalid_reason,
    }


@app.post("/process")
def process_receipt(id: int, db: Session = Depends(get_db)):
    receipt_file = db.query(ReceiptFile).filter(ReceiptFile.id == id).first()
    if not receipt_file:
        raise HTTPException(status_code=404, detail="Receipt file not found")

    if not receipt_file.is_valid:
        raise HTTPException(status_code=400, detail="Cannot process invalid file")

    if receipt_file.is_processed:
        return {"message": "File already processed"}


    try:
        data = extract_receipt_data(receipt_file.file_path)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"OCR processing failed: {str(e)}")

    receipt = db.query(Receipt).filter(Receipt.file_path == receipt_file.file_path).first()
    if receipt:
        receipt.purchased_at = data.get("purchased_at")
        receipt.merchant_name = data.get("merchant_name")
        receipt.total_amount = data.get("total_amount")
        receipt.updated_at = datetime.utcnow()
    else:
        receipt = Receipt(
            purchased_at=data.get("purchased_at"),
            merchant_name=data.get("merchant_name"),
            total_amount=data.get("total_amount"),
            file_path=receipt_file.file_path,
        )
        db.add(receipt)

    receipt_file.is_processed = True
    receipt_file.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(receipt_file)
    db.refresh(receipt)

    return {"message": "Receipt processed successfully", "receipt_id": receipt.id}


@app.get("/receipts")
def list_receipts(db: Session = Depends(get_db)):
    receipts = db.query(Receipt).all()
    return receipts


@app.get("/receipts/{receipt_id}")
def get_receipt(receipt_id: int, db: Session = Depends(get_db)):
    receipt = db.query(Receipt).filter(Receipt.id == receipt_id).first()
    if not receipt:
        raise HTTPException(status_code=404, detail="Receipt not found")
    return receipt
