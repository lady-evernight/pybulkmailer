import csv, os
import PyPDF2
import StringIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import portrait, letter, landscape

filepath = os.path.abspath('data/nameslist.csv')

class CertificateMaker():

    def writeString(self):
        # fpath="/home/micaela/Projects/pycert/templates/participants.pdf"
        dumpfile = open('/home/micaela/Projects/pycert/templates/participants.pdf', 'rw+')
        packet = StringIO.StringIO()
        packet = StringIO.StringIO()
        cv=canvas.Canvas(packet, pagesize=letter)
        
        #create a string
        cv.drawString(250, 500, "Hello World!")
        #save to string
        cv.save()
        
        #get back to 0
        # packet.seek(0)
        
        #write to a file
        with open('output/testoutput.pdf','wb') as fp:
            fp.write(packet.getvalue())

        # outputfile = open('output/testoutput.pdf', 'wb')
        # writer = pdf.PdfFileWriter()

    # https://automatetheboringstuff.com/chapter13/
    def write_string_to_pdf(self):
        pdf1File = open('templates/participants.pdf', 'rb')
        pdf1Reader = PyPDF2.PdfFileReader(pdf1File)
        pdfWriter = PyPDF2.PdfFileWriter()

        packet = StringIO.StringIO()
        cv=canvas.Canvas(packet, pagesize=letter)
        #create a string
        cv.drawString(250, 500, "Hello World!")
        #save to string
        cv.save()
        #write to a file
        with open('output/testoutput.pdf','wb') as fp:
            fp.write(packet.getvalue())

        certFirstPage = pdf1Reader.getPage(0)
        pdfWatermarkReader = PyPDF2.PdfFileReader(open('output/testoutput.pdf', 'rb'))
        certFirstPage.mergePage(pdfWatermarkReader.getPage(0))
        pdfWriter.addPage(certFirstPage)

        # for pageNum in range(pdf1Reader.numPages):
        #     pageObj = pdf1Reader.getPage(pageNum)
        #     pdfWriter.addPage(pageObj)

        pdfOutputFile = open('output/particpant-output.pdf', 'wb')
        pdfWriter.write(pdfOutputFile)
        pdfOutputFile.close()
        pdf1File.close()


if __name__ == "__main__":
    with open(filepath, 'rb') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in spamreader:
            print row[0]

    cert = CertificateMaker()
    cert.write_string_to_pdf()