import csv, os
import PyPDF2
import StringIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import portrait, letter, landscape

filepath = os.path.abspath('data/nameslist.csv')

class CertificateMaker():

    # https://automatetheboringstuff.com/chapter13/
    def write_string_to_pdf(self, namestring):
        outputfiletemp = 'output/testoutput.pdf'
        pdf1File = open('templates/participants.pdf', 'rb')
        pdf1Reader = PyPDF2.PdfFileReader(pdf1File)
        pdfWriter = PyPDF2.PdfFileWriter()

        packet = StringIO.StringIO()

        cv=canvas.Canvas(packet, pagesize=letter)
        cv.setPageSize(landscape(letter))
        #create a string
        cv.drawString(350, 300, namestring)
        #save to string
        cv.save()
        #write to a file
        with open(outputfiletemp,'wb') as fp:
            fp.write(packet.getvalue())

        certFirstPage = pdf1Reader.getPage(0)
        pdfWatermarkReader = PyPDF2.PdfFileReader(open(outputfiletemp, 'rb'))
        certFirstPage.mergePage(pdfWatermarkReader.getPage(0))
        pdfWriter.addPage(certFirstPage)

        pdfOutputFile = open('output/pyconph2015_certificate' + namestring + '.pdf', 'wb')
        pdfWriter.write(pdfOutputFile)
        pdfOutputFile.close()
        pdf1File.close()


if __name__ == "__main__":
    # iterate trough list of names from CSV
    with open(filepath, 'rb') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in spamreader:
            print row[0]

            cert = CertificateMaker()
            cert.write_string_to_pdf(row[0])

    # TODO:
    # send email to each participant