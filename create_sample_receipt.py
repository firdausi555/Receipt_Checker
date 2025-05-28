from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def create_sample_receipt(file_path):
    c = canvas.Canvas(file_path, pagesize=letter)
    width, height = letter

    # Sample receipt text
    c.setFont("Helvetica-Bold", 16)
    c.drawString(72, height - 72, "Sabil Store")

    c.setFont("Helvetica", 12)
    c.drawString(72, height - 100, "123 Sample Street")
    c.drawString(72, height - 115, "City, Country 12345")
    c.drawString(72, height - 140, "Date: 15/05/2025")
    
    c.drawString(72, height - 170, "Item 1: Widget A      $10.00")
    c.drawString(72, height - 185, "Item 2: Widget B      $20.00")
    c.drawString(72, height - 200, "------------------------------")
    c.drawString(72, height - 250, "Total:               $30.00")

    c.save()

create_sample_receipt("sample_receipt.pdf")
print("Sample receipt PDF created: sample_receipt.pdf")
