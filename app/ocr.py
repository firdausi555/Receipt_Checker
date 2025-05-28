import pytesseract
from pdf2image import convert_from_path
import re
from datetime import datetime

def extract_receipt_data(file_path: str):
    images = convert_from_path(file_path)
    full_text = ""
    for img in images:
        full_text += pytesseract.image_to_string(img)

    purchased_at = None
    merchant_name = None
    total_amount = None

    match = re.search(r'Total[^\d\$]*\$?([0-9]+[.,][0-9]{2})', full_text, re.IGNORECASE)

    if match:
        total_amount = float(match.group(1).replace(',', '.'))

    date_match = re.search(r'([0-9]{2}/[0-9]{2}/[0-9]{4})', full_text)
    if date_match:
        try:
            purchased_at = datetime.strptime(date_match.group(1), '%d/%m/%Y').isoformat()
        except:
            pass

    lines = full_text.splitlines()
    if lines:
        merchant_name = lines[0].strip()

    return {
        "purchased_at": purchased_at,
        "merchant_name": merchant_name,
        "total_amount": total_amount,
    }

