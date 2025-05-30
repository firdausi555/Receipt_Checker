import pytesseract
from pdf2image import convert_from_path
import re
from datetime import datetime

def extract_receipt_data(file_path: str):
    images = convert_from_path(file_path)
    full_text = ""
    for img in images:
        full_text += pytesseract.image_to_string(img)

  
    # print(full_text)

    total_amount = None
    total_matches = re.findall(r'TOTAL[:\s]*\$?\s*([0-9]+[.,][0-9]{2})', full_text, re.IGNORECASE)
    if total_matches:
        total_amount = float(total_matches[-1].replace(',', '.'))

    purchased_at = None
    date_matches = re.findall(r'([0-9]{2}/[0-9]{2}/[0-9]{2,4})', full_text)
    if date_matches:
        date_str = date_matches[-1]  # Pick the last date found
        try:
            if len(date_str.split('/')[-1]) == 2:
                purchased_at = datetime.strptime(date_str, '%m/%d/%y').isoformat()
            else:
                purchased_at = datetime.strptime(date_str, '%m/%d/%Y').isoformat()
        except ValueError:
            pass

    lines = full_text.splitlines()
    merchant_name = None
    for line in lines:
        if line.strip() != '':
            merchant_name = line.strip()
            break

    return {
        "purchased_at": purchased_at,
        "merchant_name": merchant_name,
        "total_amount": total_amount,
    }
