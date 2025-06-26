import smtplib
from email.message import EmailMessage

def send_email(email_to, subject, body, email_from="fullstackdeveloper404@gmail.com"):
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = email_from
    msg['To'] = email_to
    msg.set_content(body)

    smtp_server = 'smtp.gmail.com'
    port = 587

    with smtplib.SMTP(smtp_server, port) as server:
        server.starttls()
        server.login('fullstackdeveloper404@gmail.com', '')  # Use the app password
        server.send_message(msg)
