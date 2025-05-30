🧾 Receipt OCR & Processing API

A FastAPI-based web service that allows users to upload scanned receipt PDFs, validates them, performs OCR to extract details (merchant name, date, and total amount), and stores them in an SQLite database. You can also retrieve and manage stored receipts via a RESTful API.

🔧 Features
Upload and validate receipt PDFs
OCR processing using pytesseract + pdf2image
Extract merchant name, purchase date, and total amount
Store metadata in SQLite
RESTful endpoints for managing receipts
📁 Directory Structure
receipt_checker/
├── app/
│   ├── main.py
│   ├── database.py
│   ├── ocr.py
├── uploaded_receipts/
├── main.py
├── create_sample_reciept.py
├── requirements.txt
└── README.md
⚙️ Requirements
Install dependencies:

pip install -r requirements.txt
requirements.txt

fastapi
uvicorn
sqlalchemy
pydantic
pytesseract
pdf2image
python-multipart
Pillow
PyMuPDF
PyPDF2
Also install:

poppler (for pdf2image)
Tesseract OCR (for pytesseract)
🚀 Run the API
Start the FastAPI server:

uvicorn app.main:app --reload
Visit the interactive Swagger docs at:
http://127.0.0.1:8000/docs

📬 API Endpoints
🔹 Upload Receipt

curl -X POST "http://127.0.0.1:8000/upload" -F "file=@/path/to/receipt.pdf"
curl -X POST "http://127.0.0.1:8000/upload" -F "file=@sample_receipt.pdf"

Response:

{
  "message": "File uploaded successfully",
  "id": 1
}
🔹 Validate Receipt

curl -X POST "http://127.0.0.1:8000/validate?id=1"
Response:

{
  "id": 1,
  "file_name": "receipt.pdf",
  "is_valid": true,
  "invalid_reason": null
}
🔹 Process Receipt (OCR)

curl -X POST "http://127.0.0.1:8000/process?id=1"
Response:

{
  "message": "Receipt processed successfully",
  "receipt_id": 1
}
🔹 Get All Receipts

curl -X GET "http://127.0.0.1:8000/receipts"
Response:

[
  {
    "id": 1,
    "file_path": "uploaded_receipts/receipt.pdf",
    "merchant_name": "Sample Store",
    "purchased_at": "2025-05-15T00:00:00",
    "total_amount": 30.00,
    "created_at": "...",
    "updated_at": "..."
  }
]
🧪 Test Scripts
Run validation test:
python3 create_sample_reciept.py
Run OCR test:
python3 create_sample_reciept.py





Output for cheeseCakeFactory Reciept:05:14:10 sabilfirdausi@Sabils-Mac-mini receipt_checker ±|main ✗|→ curl -X POST "http://127.0.0.1:8000/upload"   -F "file=@/Users/sabilfirdausi/Desktop/receipt.pdf"
{"message":"File uploaded successfully","id":2}05:14:14 sabilfirdausi@Sabils-Mac-mini receipt_checker ±|main ✗|→
05:14:17 sabilfirdausi@Sabils-Mac-mini receipt_checker ±|main ✗|→ curl -X POST "http://127.0.0.1:8000/validate?id=2"
{"id":2,"file_name":"receipt.pdf","is_valid":true,"invalid_reason":null}05:14:22 sabilfirdausi@Sabils-Mac-mini receipt_checker ±|main ✗|→
05:14:23 sabilfirdausi@Sabils-Mac-mini receipt_checker ±|main ✗|→ curl -X POST "http://127.0.0.1:8000/process?id=2"
{"message":"Receipt processed successfully","receipt_id":2}05:14:28 sabilfirdausi@Sabils-Mac-mini receipt_checker ±|main ✗|→
05:14:29 sabilfirdausi@Sabils-Mac-mini receipt_checker ±|main ✗|→ curl http://127.0.0.1:8000/receipts/2
{"purchased_at":"2024-05-20T00:00:00","merchant_name":"THE CHEESECAKE FACTORY","file_path":"uploaded_receipts/receipt.pdf","updated_at":"2025-05-30T23:44:28.183872","total_amount":58.93,"id":2,"created_at":"2025-05-27T21:40:26.593678"}05:14:32 sabilfirdausi@Sabils-Mac-mini receipt_checker ±|main ✗|→

