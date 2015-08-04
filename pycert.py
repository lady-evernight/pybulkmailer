import csv, os
import PyPDF2
import StringIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import portrait, letter, landscape

# Import smtplib for the actual sending function
import smtplib
# Import the email modules we'll need
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

filepath = os.path.abspath('data/nameslist.csv')


class CertificateMaker():

    # https://automatetheboringstuff.com/chapter13/
    def write_string_to_pdf(self, participants_name):
        outputfiletemp = 'output/testoutput.pdf'
        pdf1File = open('templates/participants.pdf', 'rb')
        pdf1Reader = PyPDF2.PdfFileReader(pdf1File)
        pdfWriter = PyPDF2.PdfFileWriter()

        packet = StringIO.StringIO()

        cv=canvas.Canvas(packet, pagesize=letter)
        cv.setPageSize(landscape(letter))
        #create a string
        cv.drawString(350, 300, participants_name)
        #save to string
        cv.save()
        #write to a file
        with open(outputfiletemp,'wb') as fp:
            fp.write(packet.getvalue())

        certFirstPage = pdf1Reader.getPage(0)
        pdfWatermarkReader = PyPDF2.PdfFileReader(open(outputfiletemp, 'rb'))
        certFirstPage.mergePage(pdfWatermarkReader.getPage(0))
        pdfWriter.addPage(certFirstPage)

        pdfOutputFile = open('output/pyconph2015_certificate_' + participants_name + '.pdf', 'wb')
        pdfWriter.write(pdfOutputFile)
        pdfOutputFile.close()
        pdf1File.close()


class EmailSender():

    def send_email(self, participants_name, participants_email):
        msg = MIMEMultipart()
        msg['Subject'] = participants_name + ", here's your PyConPH 2015 Certificate"
        msg['From'] = "info@python.ph"
        msg['To'] = participants_email
        filename = 'pyconph2015_certificate_' + participants_name + '.pdf'
        certfile = 'output/' + filename
        pdfAttachment = MIMEApplication(open(certfile).read())
        pdfAttachment.add_header('content-disposition', 'attachment', filename = filename)
        text = MIMEMultipart('alternative')
        msg.attach(text)
        msg.attach(pdfAttachment)

        username = #username here
        password = #password here

        s = smtplib.SMTP('smtp.gmail.com')
        s.ehlo()
        s.starttls()
        s.login(username, password)
        s.sendmail("info@python.ph", participants_email, msg.as_string())
        s.quit()


if __name__ == "__main__":
    # iterate trough list of names from CSV
    with open(filepath, 'rb') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in spamreader:
            print row[0]

            cert = CertificateMaker()
            cert.write_string_to_pdf(row[0])

            # send email to each participant
            mail = EmailSender()
            mail.send_email(row[0], row[1])