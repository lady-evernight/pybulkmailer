import csv
import os

from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.units import inch, cm
from reportlab.lib.pagesizes import LETTER, landscape

from PyPDF2 import PdfFileWriter, PdfFileReader


namelist_csv = os.path.abspath("data/nameslist.csv")
cert_template = os.path.abspath("templates/certificate_template.pdf")
participant_template = os.path.abspath("templates/participant_template.pdf")


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

    output_path = "output/" + name.strip().replace(" ","_").lower() + ".pdf"

    with open(output_path, "wb") as outputStream:
        output_file.write(outputStream)


def send_email(name, email):
    pass


if __name__ == "__main__":
    # read the particpants csv
    # for each row, create a certificate
    with open(namelist_csv, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            participant_name = row['name']
            participant_email = row['email']
            print("Creating certificate for {}".format(participant_name))
            create_participant_pdf(participant_name)
            create_certificate_pdf(participant_name)

        print("Done!")
