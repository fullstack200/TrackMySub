# AWS Lambda function to send a PDF report as an email attachment.
# Required packages: smtplib, email (standard library), base64.
# Sensitive information like email credentials should be stored in environment variables.

import smtplib
from email.message import EmailMessage
import os
import base64

def lambda_handler(event, context):
    """
    Sends an email with a PDF attachment to the user.

    Parameters:
        event (dict): Event data passed to the Lambda function. Must contain:
            - 'report_data' (bytes or str): PDF report content, either raw binary or base64-encoded.
            - 'email_to' (str): Recipient email address.
            - 'subject' (str): Subject of the email.
            - 'username' (str): Username to include in the filename.
            - 'body' (str): Plain text body of the email.
        context (object): Lambda Context runtime methods and attributes. Not used in this function.

    Returns:
        dict: Status of the email sending operation.
            - {'status': 'Email with report sent'} on success.
            - {'status': 'Error', 'message': str(e)} on failure.

    Notes:
        - Uses Gmail SMTP server to send emails.
        - 'password' environment variable must be set with the sender email password.
        - Ensure the sender email allows less secure apps or uses an app-specific password.
        - The attached PDF file will be named '<username>_Report.pdf'.
    """
    try:
        # Extract input fields from the event payload
        report_data = event['report_data']
        email_to = event['email_to']
        subject = event['subject']
        username = event['username']
        body = event['body']

        # Sender email and password from environment variable
        email_from = 'fullstackdeveloper404@gmail.com'
        password = os.environ['password']

        # Decode report data if it is base64-encoded
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

        # Attach the PDF file
        msg.add_attachment(
            report_bytes,
            maintype='application',
            subtype='pdf',
            filename=f'{username}_Report.pdf'
        )

        # Send the email using Gmail SMTP
        smtp_server = 'smtp.gmail.com'
        port = 587

        with smtplib.SMTP(smtp_server, port) as server:
            server.starttls()          # Start TLS encryption
            server.login(email_from, password)  # Login to SMTP server
            server.send_message(msg)   # Send the email
            print("Email with attachment sent successfully")

        return {'status': 'Email with report sent'}

    except Exception as e:
        # Catch any exception and return an error response
        return {'status': 'Error', 'message': str(e)}
