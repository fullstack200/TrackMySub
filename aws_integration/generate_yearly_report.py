"""
AWS Lambda function to generate a yearly PDF report, merge it with a template,
upload it to S3, and return the PDF as base64.

Required packages:
- boto3
- pdfrw
- reportlab

Requirements:
- Montserrat font files (Regular & Bold) should be in /opt/fonts for Lambda Layer.
- Template PDF 'TrackMySubs-Yearly.pdf' must exist in the S3 bucket 'trackmysubs-bucket'.

Function workflow:
1. Registers Montserrat fonts for use in ReportLab.
2. Downloads the template PDF from S3.
3. Generates an overlay PDF with dynamic data (year, monthly totals, grand total, budget, note).
4. Merges overlay onto the template PDF using pdfrw.
5. Uploads the final PDF back to S3.
6. Returns the PDF content in base64 for immediate use.
"""

import boto3
import io
import pdfrw
import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import base64

class UnclosableBytesIO(io.BytesIO):
    """BytesIO subclass that ignores the close() method to allow multiple reads/writes."""
    def close(self):
        pass

def lambda_handler(event, context):
    """
    Generate a yearly report PDF, merge with a template, upload to S3, and return PDF content.

    Parameters:
        event (dict): Required keys:
            - 'year' (int): Report year.
            - 'date_report_generated' (str): Date of report generation, e.g., "25/06/2025".
            - 'monthly_reports' (list of dicts): Each dict with 'month_name' and 'total_amount'.
            - 'grand_total' (float): Total spending for the year.
            - 'yearly_budget_amount' (float): User's yearly budget.
            - 'note' (str): Any note or message to include in the report.
        context: AWS Lambda context (not used).

    Returns:
        dict:
            - statusCode: HTTP-like status code (200 if successful)
            - pdf: Base64-encoded PDF content
            - body: Message confirming upload to S3
    """
    # 1. Register Montserrat fonts
    font_dir = "/opt/fonts"  # Path in Lambda Layer
    pdfmetrics.registerFont(TTFont("Montserrat", os.path.join(font_dir, "Montserrat-Regular.ttf")))
    pdfmetrics.registerFont(TTFont("Montserrat-Bold", os.path.join(font_dir, "Montserrat-Bold.ttf")))

    # 2. Download template PDF from S3
    s3 = boto3.client('s3')
    bucket = 'trackmysubs-bucket'
    key = 'TrackMySubs-Yearly.pdf'
    template_stream = io.BytesIO()
    s3.download_fileobj(Bucket=bucket, Key=key, Fileobj=template_stream)
    template_stream.seek(0)

    # 3. Create overlay PDF with dynamic data
    overlay_stream = io.BytesIO()
    c = canvas.Canvas(overlay_stream, pagesize=letter)

    # Add year and generation date
    c.setFont("Montserrat", 12)
    c.drawString(280, 654, str(event['year']))
    c.drawString(280, 630, event['date_report_generated'])

    # Insert monthly report data
    y = 510
    for idx, month in enumerate(event['monthly_reports'], start=1):
        c.drawString(76, y, str(idx))  # Serial No
        c.drawString(120, y, month['month_name'])
        c.drawString(382, y, f"$ {month['total_amount']}")
        y -= 22

    # Add bold text for grand total, budget, and note
    c.setFont("Montserrat-Bold", 12)
    c.drawString(382, 235, f"$ {event['grand_total']}")
    c.drawString(382, 198, f"$ {event['yearly_budget_amount']}")
    c.drawString(100, 126, event['note'])

    c.save()
    overlay_stream.seek(0)

    # 4. Merge overlay onto template
    template_pdf = pdfrw.PdfReader(template_stream)
    overlay_pdf = pdfrw.PdfReader(overlay_stream)
    for page, overlay_page in zip(template_pdf.pages, overlay_pdf.pages):
        merger = pdfrw.PageMerge(page)
        merger.add(overlay_page).render()

    # 5. Output final PDF and upload to S3
    output_stream = UnclosableBytesIO()
    pdfrw.PdfWriter().write(output_stream, template_pdf)
    output_stream.seek(0)
    pdf_bytes = output_stream.getvalue()

    output_key = f"{event['year']}.pdf"
    s3.upload_fileobj(output_stream, bucket, output_key)

    # Return PDF as base64
    pdf_base64 = base64.b64encode(pdf_bytes).decode('utf-8')

    return {
        "statusCode": 200,
        "pdf": pdf_base64,
        "body": f"PDF uploaded to s3://{bucket}/{output_key}"
    }
