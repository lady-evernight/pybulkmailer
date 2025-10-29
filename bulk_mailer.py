import csv
import os
import smtplib
import json
import ssl
import logging
import certifi  # <-- add this

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# set the log level to info and specify the format we want to use
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s %(module)s %(lineno)d - %(message)s",
)
log = logging.getLogger(__name__)

namelist_csv = os.path.abspath("data/nameslist.csv")
settings_file = os.path.abspath("config/settings.json")

def load_settings():
    with open(settings_file) as f:
        return json.load(f)

settings = load_settings()
gmail_user = settings["gmail_user"]
gmail_password = settings["gmail_password"]
carbon_copy = settings.get("carbon_copy") or settings.get("carbon-copy")  # tolerant to either key

def form_email_message(name, to_email, subject, nickname, body_html):
    from_email = gmail_user

    email_msg = MIMEMultipart("alternative")
    email_msg["Subject"] = subject
    email_msg["From"] = from_email
    email_msg["To"] = to_email
    if carbon_copy:
        email_msg["Cc"] = carbon_copy

    # Plain and HTML versions (attach plain first, then HTML)
    plain_text = f"Hi {nickname},\n\nThis is a fallback version of the email.\n\nCheers,\nThe PyLadies Manila Team"
    text_part = MIMEText(plain_text, "plain")
    html_part = MIMEText(body_html, "html")
    email_msg.attach(text_part)
    email_msg.attach(html_part)
    return email_msg

def send_email(name, to_email, nickname):
    subject = "Hello from PyLadies Manila!"
    html_body = f"""
        <html>
            <body>
                <p>Hi {nickname},</p>
                <p>
                    Cheers,<br>
                    The PyLadies Manila Team
                </p>
            </body>
        </html>
    """  # <-- use {nickname}, not {{nickname}}

    email_msg = form_email_message(name, to_email, subject, nickname, html_body)

    # SSL context that trusts certifi's CA bundle
    context = ssl.create_default_context()
    context.load_verify_locations(cafile=certifi.where())
    context.minimum_version = ssl.TLSVersion.TLSv1_2

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(gmail_user, gmail_password)
            recipients = [to_email] + ([carbon_copy] if carbon_copy else [])
            server.sendmail(gmail_user, recipients, email_msg.as_string())
            log.info(f"Email sent! to {name} ({to_email})")
    except Exception:
        log.exception("Something went wrong...")  # prints full traceback

if __name__ == "__main__":
    with open(namelist_csv, newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            participant_name = row["name"]
            participant_email = row["email"]
            nickname = row["nickname"]
            send_email(participant_name, participant_email, nickname)

        log.info("Done!")
