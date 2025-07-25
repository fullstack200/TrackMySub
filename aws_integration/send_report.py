# This function requires the `smtplib` and `email` libraries to send an email with a PDF attachment.
# It uses environment variables for sensitive data like email credentials.
# The function sends a report as a PDF attachment to the user.

import smtplib
from email.message import EmailMessage
import os
import base64

def lambda_handler(event, context):
    try:
        # Extract input fields from event
        report_data = event['report_data']  # This should be raw binary or base64-encoded
        email_to = event['email_to']
        subject = event['subject']
        username = event['username']
        body = event['body']

        # Prepare sender info
        email_from = 'fullstackdeveloper404@gmail.com'
        password = os.environ['password']  # Set this in Lambda environment variables

        # Decode report data if base64 encoded (just to be safe)
        if isinstance(report_data, str):
            report_bytes = base64.b64decode(report_data)
        else:
            report_bytes = report_data

        # Create the email message
        msg = EmailMessage()
        msg['Subject'] = subject
        msg['From'] = email_from
        msg['To'] = email_to
        msg.set_content(body)

        # Attach the PDF
        msg.add_attachment(
            report_bytes,
            maintype='application',
            subtype='pdf',
            filename=f'{username}_Report.pdf'
        )

        # Send the email via Gmail SMTP
        smtp_server = 'smtp.gmail.com'
        port = 587

        with smtplib.SMTP(smtp_server, port) as server:
            server.starttls()
            server.login(email_from, password)
            server.send_message(msg)
            print("Email with attachment sent successfully")

        return {'status': 'Email with report sent'}

    except Exception as e:
        return {'status': 'Error', 'message': str(e)}
