# The function requires the following packages:
# boto3, pdfrw, reportlab, and their dependencies.
# Ensure these packages are included in your Lambda layer or deployment package.
# The Montserrat font files should be placed in the /opt/fonts directory in the Lambda layer
# or deployment package.
# The function generates a yearly report PDF based on the provided event data,
# merges it with a template PDF, uploads the final PDF to an S3 bucket and returns the pdf back
# to the function call.

import boto3
import io
import pdfrw
import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from datetime import date, datetime
import base64

class UnclosableBytesIO(io.BytesIO):
    def close(self):
        pass  # Ignore close

def lambda_handler(event, context):
    # 1. Register Montserrat fonts
    font_dir = "/opt/fonts"  # For Lambda Layer, otherwise just "fonts" if in same zip
    pdfmetrics.registerFont(TTFont("Montserrat", os.path.join(font_dir, "Montserrat-Regular.ttf")))
    pdfmetrics.registerFont(TTFont("Montserrat-Bold", os.path.join(font_dir, "Montserrat-Bold.ttf")))

    # 2. Download template PDF from S3
    s3 = boto3.client('s3')
    bucket = 'trackmysubs-bucket'
    key = 'TrackMySubs-Yearly.pdf'
    template_stream = io.BytesIO()
    s3.download_fileobj(Bucket=bucket, Key=key, Fileobj=template_stream)
    template_stream.seek(0)

    # 3. Create overlay PDF
    overlay_stream = io.BytesIO()
    c = canvas.Canvas(overlay_stream, pagesize=letter)

    c.setFont("Montserrat", 12)
    c.drawString(280, 654, str(event['year'])) # e.g., 2025
    c.drawString(280, 630, str(date.today())) # e.g., "25/06/2025"

    y = 510
    for idx, month in enumerate(event['monthly_reports'], start=1):
        c.drawString(76, y, str(idx)) # Serial No
        c.drawString(120, y, month['month_name']) # Month Name
        c.drawString(382, y, f"$ {month['total_amount']}") # Total amount paid in that month
        y -= 22

    # Bold Grand Total, Budget, Note
    c.setFont("Montserrat-Bold", 12)
    c.drawString(382, 235, f"$ {event['grand_total']}")  # Sum of amount paid in all months
    c.drawString(382, 198, f"$ {event['yearly_budget_amount']}") # Yearly Budget
    c.drawString(100, 126, event['note']) # Note

    c.save()
    overlay_stream.seek(0)

    # 4. Merge overlay onto template
    template_pdf = pdfrw.PdfReader(template_stream)
    overlay_pdf = pdfrw.PdfReader(overlay_stream)
    for page, overlay_page in zip(template_pdf.pages, overlay_pdf.pages):
        merger = pdfrw.PageMerge(page)
        merger.add(overlay_page).render()

    # 5. Output and upload
    output_stream = UnclosableBytesIO()
    pdfrw.PdfWriter().write(output_stream, template_pdf)
    output_stream.seek(0)
    pdf_bytes = output_stream.getvalue()

    output_key = f"{event['year']}.pdf"
    s3.upload_fileobj(output_stream, bucket, output_key)

    pdf_base64 = base64.b64encode(pdf_bytes).decode('utf-8')

    return {
        "statusCode": 200,
        "pdf": pdf_base64,
        "body": f"PDF uploaded to s3://{bucket}/{output_key}"
    }
