from pathlib import Path
from tkinter import PhotoImage
from PIL import Image
import fitz
import math
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm, mm
from reportlab.lib import utils

class Thumbail: # Fonction d'extraction des images depuis une fonction condition
    def __init__(self, filepath):
        self.filepath = filepath
        self.path_file = Path(self.filepath)
        self.pdf = fitz.open(self.filepath)
        self.nb_pages = self.pdf.page_count

    def get_page(self, page_num):
        page = self.pdf.load_page(page_num)
        pix = page.get_pixmap()
        px1 = fitz.Pixmap(pix, 0) if pix.alpha else pix

        fp = './temp_files/' + str(self.path_file.name) + '-' + str(page_num) + '.png'
        imgdata = px1.save(fp, 'png', 95)
        a = Image.open(fp)
        return a

    def run(self):
        for i in range(self.pdf.page_count):
            yield self.get_page(i)

def GeneratePDFfromImage(image_file, save_file):
    c = canvas.Canvas(save_file, pagesize = A4)
    image = utils.ImageReader(image_file)
    img_width, img_height = image.getSize()
    paper_width = (210-30)*mm
    height = (img_height/img_width) * paper_width

    c.drawImage(image, x = 15*mm, y = 297*mm - height - 15*mm, width = paper_width, height = height)
    c.showPage()
    c.save()
