Simple Bulk Mailer for PyLadies Manila
======

Derived from the original PyCon PH certificate generator, this script has been adapted into a bulk mailer. It's designed for community groups like PyLadies Manila to send personalized, rich-text (HTML) emails for newsletters, announcements, and other communications.

It takes a CSV file of recipients and an HTML email template, then sends a personalized email to each person on the list.

## ✨ Features
Bulk Emailing: Sends emails to a large list of recipients specified in a CSV file.

Rich-Text Formatting: Uses an HTML file as a template for visually appealing emails. 📧

Personalization: Automatically inserts data from the CSV (like names) into each email using placeholders.

CC & BCC Support: Easily add recipients to the CC and BCC fields for every email sent.

Attachments: Option to attach files to your bulk emails.

## 💻 Dev Environment Setup
```
(bulkenv) $ pip install -r requirements.txt
```

## ⚙️ Settings
Add a `settings.json` in `config/` folder with the following format:
```
{
    "gmail_user": "you@gmail.com",
    "gmail_password": "<your-app-password>",
    "carbon-copy": "cc@gmail.com"
}
```

## ✍️ Write your Email
On the `send_email` function, add your subject title to the `subject` variable, and write the content of your mail to the `html_body` in HTML format.

```python
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
```

## 🚀 Running the Script
```
(pycert) $ python bulk_maker.py

[2021-03-18 11:59:32,783] INFO certificate_maker 118 - Email sent! to Real Name
[2021-03-18 11:59:36,374] INFO bulk_maker 136 - Done!
```

## References:

### Sending Email
- https://realpython.com/python-send-email/#adding-attachments-using-the-email-package

### PyCert: Automated Certificate Generator and Emailer for PyCon PH
- https://github.com/codemickeycode/pycert
