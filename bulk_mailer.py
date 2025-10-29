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
    subject = """PythonAsia 2026 CFP now open, and we’d love to hear from you again!"""
    html_body = f"""
    <html>
    <body style="margin:0;padding:0;background:#f6f7fb;">
    <div style="max-width:640px;margin:0 auto;padding:32px 20px;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Helvetica,Arial,sans-serif;line-height:1.6;color:#111;background:#ffffff;">
        <p style="margin:0 0 16px;">Hi {name},</p>

        <p style="margin:0 0 16px;">
        We’re thrilled to share that the Call for Proposals for <strong>PythonAsia 2026</strong> (formerly PyCon APAC) is now open! 🎉
        </p>

        <p style="margin:0 0 16px;">
        This year’s theme, <strong>“Kalinga,”</strong> draws from the Filipino word for care and compassion, the quiet strength that nurtures, heals, and allows us to grow. It celebrates the people and stories that make the Python community thrive.
        </p>

        <p style="margin:0 0 16px;">
        As someone who has submitted or spoken at <strong>[Event]</strong>, you are already familiar with the power of sharing ideas on this platform. We’d love to see your proposal again, or your help in discovering new voices to feature at PythonAsia 2026.
        </p>

        <h2 style="margin:24px 0 12px;font-size:18px;">💡 Here’s how you can help:</h2>

        <ol style="margin:0 0 16px 0;padding:0;list-style-type:none;">
        <li style="margin:0 0 16px;">
            <p style="margin:0 0 8px;"><strong>1. Submit a proposal</strong></p>
            <p style="margin:0 0 12px;">Got something new to share? Submit your talk, workshop, or poster idea here:</p>
            <p style="margin:0 0 12px;">
            <a href="https://pretalx.com/python-asia-2026"
                style="display:inline-block;text-decoration:none;padding:12px 18px;border-radius:6px;background:#2b6cb0;color:#ffffff;font-weight:600;">
                👉 Submit via pretalx
            </a>
            </p>
            <p style="margin:0 0 12px;">
            or open: <a href="https://pretalx.com/python-asia-2026" style="color:#2b6cb0;">https://pretalx.com/python-asia-2026</a>
            </p>
        </li>

        <li style="margin:0 0 16px;">
            <p style="margin:0 0 8px;"><strong>2. Invite others to speak</strong></p>
            <p style="margin:0 0 12px;">You probably know talented Pythonistas who would make great speakers. A personal message from you can make a huge difference.</p>
            <p style="margin:0 0 8px;"><em>Here are quick templates you can use:</em></p>
            <blockquote style="margin:0 0 12px;padding:8px 12px;border-left:4px solid #e2e8f0;background:#f8fafc;">
            “Hi (name), I really enjoyed your talk on (topic). Have you thought about submitting it to PythonAsia 2026? Details:
            <a href="https://pretalx.com/python-asia-2026" style="color:#2b6cb0;">https://pretalx.com/python-asia-2026</a>”
            </blockquote>
            <blockquote style="margin:0 0 12px;padding:8px 12px;border-left:4px solid #e2e8f0;background:#f8fafc;">
            “Hi (name), your work on (project/topic) is inspiring. It would make a great talk for PythonAsia 2026! Submit here:
            <a href="https://pretalx.com/python-asia-2026" style="color:#2b6cb0;">https://pretalx.com/python-asia-2026</a>”
            </blockquote>
        </li>

        <li style="margin:0 0 16px;">
            <p style="margin:0 0 8px;"><strong>3. Spread the word</strong></p>
            <p style="margin:0;">Help us reach more people by sharing the CFP on social media.</p>
        </li>
        </ol>

        <h3 style="margin:24px 0 8px;font-size:16px;">Need help?</h3>
        <p style="margin:0 0 16px;">
        Our program team is happy to answer questions or assist potential speakers with proposal ideas or guidance.<br />
        📧 <a href="mailto:pyconprogram@python.ph" style="color:#2b6cb0;">pyconprogram@python.ph</a>
        </p>

        <p style="margin:0 0 16px;">
        Together, we can create a conference that highlights the diversity, care, and creativity of the Python community across Asia.
        </p>

        <p style="margin:0 0 16px;">
        Thank you for being part of our journey. We can’t wait to hear from you again!
        </p>

        <p style="margin:0 0 4px;">Best regards,</p>
        <p style="margin:0;">The PythonAsia 2026 Program Team</p>
    </div>
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
