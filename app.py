import csv
from PyPDF2 import PdfFileWriter, PdfFileReader
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

LIST_TO_GENERATE = [
    ('Participant', 'Participants', './data/participants.csv'),
    ('Most Valuable Participant', 'MVP', './data/mvp.csv'),
    ('Mentor', 'Mentor', './data/mentor.csv'),
    ('Event Leader', 'Leader', './data/leader.csv'),
]


def setup():
    pdfmetrics.registerFont(TTFont('Raleway', 'fonts/Raleway-Regular.ttf'))
    pdfmetrics.registerFont(TTFont('Raleway Semi Bold', 'fonts/Raleway-SemiBold.ttf'))
    pdfmetrics.registerFont(TTFont('Raleway Bold', 'fonts/Raleway-Bold.ttf'))


def generate(honor: str, slug: str, data_path: str):
    print(f'Starting on generating certificates with honor as {honor}')
    with open(data_path) as csv_file:
        csv_reader = list(csv.reader(csv_file, delimiter=','))
        for category, nim, name in csv_reader[1:]:
            packet = io.BytesIO()
            can = canvas.Canvas(packet, pagesize=letter)
            can.setFont('Raleway', 25)
            can.drawCentredString(355, 265, name)
            can.setFont('Raleway Bold', 16)
            can.drawCentredString(355, 207, honor)
            can.setFont('Raleway Semi Bold', 19)
            can.drawCentredString(360, 160, f"{category} Bootcamp")
            can.save()

            packet.seek(0)

            # create a new PDF with Reportlab
            new_pdf = PdfFileReader(packet)
            # read existing PDF
            existing_pdf = PdfFileReader(open("./template/certificate.pdf", "rb"))
            output = PdfFileWriter()
            # add the "watermark" (which is the new pdf) on the existing page
            page = existing_pdf.getPage(0)
            page.mergePage(new_pdf.getPage(0))
            output.addPage(page)
            # finally, write "output" to a real file
            output_stream = open(f"./certificates/{slug}/bootcamp-hmif-tech-2022-{honor}-{nim}-{name}.pdf", "wb")
            output.write(output_stream)
            output_stream.close()

    print(f'Finished generating certificates with honor as {honor}')


def main():
    for honor, slug, data_path in LIST_TO_GENERATE:
        generate(honor, slug, data_path)


if __name__ == "__main__":
    setup()
    main()
