from dotenv import load_dotenv
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import os
load_dotenv()
from typing import Union

def account_creation(mail: str, code: Union[str, int]) -> None:
    html = f"""\
    <html>
    <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;font-size:20px;">
        <h2>Welcome to Codraw!</h2>
        <p>Good Morning,</p>
        <p>
        Thank you for creating an account on <strong>CoDraw</strong>.
        This mail is the confirmation of account creation<br>Authentication code is the following: <strong style="font-size:28px">{code}</strong>
        </p>
        <p>Best regards,<br><em>CoDraw Support Team</em></p>
    </body>
    </html>
    """

    msg = MIMEMultipart("alternative")
    msg["Subject"] = "Creation of account on CoDraw."
    msg["From"] = "codraw.io@gmail.com"
    msg["To"] = mail
    # Optional plain text version
    plain_message = """\
    Good Morning,

    Thank you for creating an account on CoDraw
    This mail is the confirmation of account creation<br>Authentication code is the following: {code}.

    Best regards,
    CoDraw Support Team
    """

    msg.attach(MIMEText(plain_message, "plain", "utf-8"))
    msg.attach(MIMEText(html, "html", "utf-8"))

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login('codraw.io@gmail.com', os.getenv('GMAIL_PASS'))
    server.sendmail(msg["From"], msg["To"], msg.as_string())
    server.quit()
    print(f"Email sent to {mail} with code {code}")