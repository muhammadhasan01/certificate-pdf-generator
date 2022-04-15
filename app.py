from PyPDF2 import PdfFileWriter, PdfFileReader
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont


def main():
    pdfmetrics.registerFont(TTFont('Raleway', 'fonts/Raleway-Regular.ttf'))
    pdfmetrics.registerFont(TTFont('Raleway Semi Bold', 'fonts/Raleway-SemiBold.ttf'))
    pdfmetrics.registerFont(TTFont('Raleway Bold', 'fonts/Raleway-Bold.ttf'))

    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=letter)
    can.setFont('Raleway', 25)
    can.drawCentredString(360, 265, "Jauhar Wibisono")
    can.setFont('Raleway Bold', 16)
    can.drawCentredString(360, 207, "Event Leader")
    can.setFont('Raleway Semi Bold', 19)
    can.drawCentredString(360, 160, "Competitive Programming Bootcamp")
    can.save()

    packet.seek(0)

    # create a new PDF with Reportlab
    new_pdf = PdfFileReader(packet)
    # read your existing PDF
    existing_pdf = PdfFileReader(open("template/certificate.pdf", "rb"))
    output = PdfFileWriter()
    # add the "watermark" (which is the new pdf) on the existing page
    page = existing_pdf.getPage(0)
    page.mergePage(new_pdf.getPage(0))
    output.addPage(page)
    # finally, write "output" to a real file
    outputStream = open("template/result.pdf", "wb")
    output.write(outputStream)
    outputStream.close()


if __name__ == "__main__":
    main()
