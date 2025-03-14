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

from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import LETTER, landscape

from PyPDF2 import PdfFileWriter, PdfFileReader


# set the log level to info and specify the format we want to use
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s %(module)s %(lineno)d - %(message)s',
)
# create a custom logger with the name __name__
log = logging.getLogger(__name__)


namelist_csv = os.path.abspath("data/nameslist.csv")
cert_template = os.path.abspath("templates/certificate_template.pdf")
participant_template = os.path.abspath("templates/participant_template.pdf")

settings_file = os.path.abspath("config/settings.json")


def load_settings():
    with open(settings_file) as f:
        data = json.load(f)
    return data


settings = load_settings()
gmail_user = settings['gmail_user']
gmail_password = settings['gmail_password']


def create_participant_pdf(name):
    # create participant pdf, save it on output folder
    canvas = Canvas(participant_template, pagesize=landscape(LETTER))
    canvas.setFont("Helvetica-Bold", 25)
    canvas.drawString(1.5 * inch, 4.10 * inch, name)
    canvas.save()


def create_certificate_pdf(name, cert_template=cert_template):
    watermark = PdfFileReader(open(participant_template, "rb"))

    output_file = PdfFileWriter()
    input_file = PdfFileReader(open(cert_template, "rb"))

    input_page = input_file.getPage(0)
    input_page.mergePage(watermark.getPage(0))
    output_file.addPage(input_page)

    output_path = "output/" + name.strip().replace(" ", "_").lower() + ".pdf"

    with open(output_path, "wb") as outputStream:
        output_file.write(outputStream)

    return output_path


def form_email_message(name, to_email, subject, body, participant_cert):
    from_email = gmail_user

    email_msg = MIMEMultipart()
    email_msg['Subject'] = subject
    email_msg['From'] = from_email
    email_msg['To'] = to_email
    text_message = MIMEText(body, 'plain')
    email_msg.attach(text_message)

    with open(participant_cert, "rb") as attachment:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())

    encoders.encode_base64(part)

    filename = os.path.basename(participant_cert)
    log.info(filename)

    part.add_header(
        "Content-Disposition",
        f"attachment; filename= {filename}",
    )

    # Add attachment to message and convert message to string
    email_msg.attach(part)

    return email_msg.as_string()


def send_email(name, to_email, participant_cert):
    context = ssl.create_default_context()
    subject = "Your PythonPH Certificate"
    body = (
        "Hi {}, here's your Intro to Python for Professionals Certificate"
        .format(name)
    )
    email_msg = form_email_message(
        name, to_email, subject, body, participant_cert)
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) \
                as server:
            server.login(gmail_user, gmail_password)
            server.sendmail(gmail_user, to_email, email_msg)
            server.close()
            log.info('Email sent!')
    except Exception as e:
        log.error('Something went wrong... {}'.format(e))


if __name__ == "__main__":
    # read the participants csv
    # for each row, create a certificate
    with open(namelist_csv, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            participant_name = row['name']
            participant_email = row['email']
            log.info("Creating certificate for {}".format(participant_name))
            create_participant_pdf(participant_name)
            cleaned_name = participant_name.replace("ñ", "n")
            participant_cert = create_certificate_pdf(cleaned_name)
            send_email(participant_name, participant_email, participant_cert)

        log.info("Done!")
