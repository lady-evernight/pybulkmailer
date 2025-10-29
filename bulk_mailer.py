import csv
import os
import smtplib
import json
import ssl
import logging

from email import encoders
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.message import EmailMessage


# set the log level to info and specify the format we want to use
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s %(module)s %(lineno)d - %(message)s",
)
# create a custom logger with the name __name__
log = logging.getLogger(__name__)


namelist_csv = os.path.abspath("data/nameslist.csv")
 
settings_file = os.path.abspath("config/settings.json")


def load_settings():
    with open(settings_file) as f:
        data = json.load(f)
    return data


settings = load_settings()
gmail_user = settings["gmail_user"]
gmail_password = settings["gmail_password"]
carbon_copy = settings["carbon_copy"]

def form_email_message(name, to_email, subject, nickname, body_html):
    from_email = gmail_user

    email_msg = MIMEMultipart("alternative")
    email_msg["Subject"] = subject
    email_msg["From"] = from_email
    email_msg["To"] = to_email
    email_msg["Cc"] = carbon_copy
    text_message = MIMEText(body_html, "plain")
    email_msg.attach(text_message)

    # Plain and HTML versions
    plain_text = f"Hi {nickname},\n\nThis is a fallback version of the email."
    text_part = MIMEText(plain_text, "plain")
    html_part = MIMEText(body_html, "html")

    email_msg.attach(text_part)
    email_msg.attach(html_part)

    return email_msg


def send_email(name, to_email, nickname):
    subject = "Hello from PyLadies Manila!"
    html_body = f"""
        <html>
            <p>Hi {{nickname}},</p>
            <p>
                Cheers,<br>
                The PyLadies Manila Team
            </p>
        </html>
    """
    email_msg = form_email_message(
        name, to_email, subject, nickname, html_body)

    context = ssl.create_default_context()
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) \
                as server:
            server.login(gmail_user, gmail_password)
            server.sendmail(gmail_user, [to_email, carbon_copy], email_msg.as_string())
            server.close()
            log.info(f"Email sent! to {name}")
    except Exception as e:
        log.error("Something went wrong... {}".format(e))


if __name__ == "__main__":
    # read the participants csv
    # for each row, send email
    with open(namelist_csv, newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            participant_name = row["name"]
            participant_email = row["email"]
            nickname = row["nickname"]
            send_email(participant_name, participant_email, nickname)

        log.info("Done!")