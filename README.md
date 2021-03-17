pycert
======

Certificate maker for Certificate maker for PyCon PH and other PythonPH events

A script that accepts a CSV file which contains a list of attendee names and emails then outputs multiple PDFs (certificate of attendance)

- certificate maker
- email sender with pdf attachment

## Settings
Add a `settings.json` in `config/` folder with the following format:
```
{
    "gmail_user": "you@gmail.com",
    "gmail_password": "<your-app-password>"
}
```

## References:

### Generate PDF
- https://realpython.com/creating-modifying-pdf/#setting-font-properties
- https://medium.com/@schedulepython/how-to-watermark-your-pdf-files-with-python-f193fb26656e

### Sending Email
- https://realpython.com/python-send-email/#adding-attachments-using-the-email-package