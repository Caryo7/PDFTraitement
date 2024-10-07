from PyPDF2 import *
from pathlib import Path
from tkinter import *
from PIL import *
import fitz
import math

class ExtractPages: # Fonction d'extraction de pages depuis une fonction condition
    def __init__(self, origin, function, destination, folder, unit):
        self.unit = unit
        self.file = origin
        self.output = destination
        self.pdf = PdfReader(self.file)
        self.fpout = PdfWriter()
        self.function = function

        self.nb_iter = len(self.pdf.pages)

    def run(self):
        for i in range(len(self.pdf.pages)):
            if self.function(i, self.nb_iter):
                self.fpout.add_page(self.pdf.pages[i])
            yield 1

    def close(self):
        fp = open(self.output, 'wb')
        self.fpout.write(fp)
        fp.close()

class SimpleExtractor:
    def __init__(self, extraction, output):
        self.extraction = extraction
        self.output = output
        self.fpout = PdfWriter()

        self.nb_iter = len(self.extraction)

    def run(self):
        for path, page in self.extraction:
            pdf = PdfReader(path)
            self.fpout.add_page(pdf.pages[page])
            yield 1

    def close(self):
        fp = open(self.output, 'wb')
        self.fpout.write(fp)
        fp.close()

class ExtractImages: # Fonction d'extraction des images depuis une fonction condition
    def __init__(self, filepath, function, output, folder, unit):
        self.unit = unit
        self.function = function
        self.output = folder
        self.filepath = filepath
        self.path_file = Path(self.filepath)
        self.pdf = fitz.open(self.filepath)

        self.nb_iter = self.pdf.page_count

    def layout_name(self, nb):
        l = len(str(self.nb_iter))
        nb = str(nb)
        while len(nb) != l:
            nb = '0' + nb

        return nb

    def get_page(self, page_num, dpi):
        if dpi == 0:
            dpi = 330

        page = self.pdf.load_page(page_num)
        pix = page.get_pixmap(dpi = dpi)
        px1 = fitz.Pixmap(pix, 0) if pix.alpha else pix

        fp = self.output + '/' + str(self.path_file.name) + '-' + self.layout_name(page_num) + '.png'
        imgdata = px1.save(fp, 'png', 95)
        del page
        del px1
        del pix
        del imgdata

    def run(self):
        for i in range(self.pdf.page_count):
            yes, dpi = self.function(i, self.nb_iter)
            if yes:
                self.get_page(i, dpi)

            yield 1

    def close(self):
        del self.pdf

class SplitFile:
    def __init__(self, file, function, output, folder, unit):
        self.unit = unit
        self.function = function
        self.file = Path(file)
        self.output = folder
        self.pdf = PdfReader(self.file)
        self.cnt = 0
        self.writer = PdfWriter()
        self.pages = 0

        self.nb_iter = len(self.pdf.pages)

    def save(self):
        if self.pages == 0:
            return

        fp = open(self.output + '/' + str(self.file.name) + '-' + str(self.cnt + 1) + '.pdf', 'wb')
        self.writer.write(fp)
        fp.close()
        self.writer = PdfWriter()
        self.cnt += 1
        self.pages = 0

    def run(self):
        for i in range(len(self.pdf.pages)):
            self.writer.add_page(self.pdf.pages[i])
            self.pages += 1

            if self.function(i, self.nb_iter):
                self.save()

            yield 1

    def close(self):
        self.save()
