from PyPDF2 import *
from PyPDF2.generic import RectangleObject
from pathlib import Path

class OrganizePages: # Change l'ordre des pages selon une fonction
    def __init__(self, file, function, output, folder, unit):
        self.unit = unit
        self.function = function
        self.file = file
        self.output = output
        self.pdf = PdfReader(self.file)
        self.writer = PdfWriter()

        self.nb_iter = len(self.pdf.pages)

    def run(self):
        for i in range(len(self.pdf.pages)):
            pos = self.function(i, self.nb_iter)[0]
            self.writer.add_page(self.pdf.pages[pos])

            yield 1

    def close(self):
        fp = open(self.output, mode = 'wb')
        self.writer.write(fp)
        fp.close()

class RemovePages: # Met toutes les pages saufes celles respectant la fonction
    def __init__(self, file, function, output, folder, unit):
        self.unit = unit
        self.function = function
        self.file = file
        self.output = output
        self.pdf = PdfReader(self.file)
        self.writer = PdfWriter()

        self.nb_iter = len(self.pdf.pages)

    def run(self):
        for i in range(len(self.pdf.pages)):
            if not self.function(i, self.nb_iter):
                self.writer.add_page(self.pdf.pages[i])

            yield 1

    def close(self):
        fp = open(self.output, mode = 'wb')
        self.writer.write(fp)
        fp.close()

class ArrangerDuo:
    def test_parity(self, file):
        tests_parity = PdfReader(file)
        blank = PageObject.create_blank_page(width = tests_parity.pages[0].mediabox.width,
                                             height = tests_parity.pages[0].mediabox.height)
        
        t = PdfWriter()
        for page in tests_parity.pages:
            t.add_page(page)

        l = len(tests_parity.pages)
        while l % 2 != 0:
            t.add_page(blank)
            l += 1

        file = Path(file).name

        file = './temp_files/' + file
        f = open(file, 'wb')
        t.write(f)
        f.close()
        return file

    def __init__(self, file, function, output, folder, unit):
        self.unit = unit
        self.function = function
        file = self.test_parity(file)

        self.reader = PdfReader(file) # On ouvre le fichier
        self.fpout = PdfWriter()
        self.output = output
        self.nb_pages = len(self.reader.pages)

        self.nb_iter = int(self.nb_pages/2)

    def run(self):
        for i in range(int(self.nb_pages/2)):
            data = self.function(i, self.nb_pages)
            if len(data) == 3:
                index1, index2, force = data
            else:
                index1, index2, force, alignement = data

            page1 = self.reader.pages[index1] # Récupération de la page
            page2 = self.reader.pages[index2]

            width1 = page1.cropbox.right # Largeur de la page 1
            width2 = page2.cropbox.right # Largeur de la page 2
            height1 = page1.cropbox.top # Hauteur page 1
            height2 = page2.cropbox.top # Hauteur page 2
            width = width1 + width2
            height = max([height1, height2])
            if force:
                height = PaperSize.A4.width
                width = PaperSize.A4.height

            offsetx1 = (width - width1 - width2) / 2
            offsety1 = (height - height1) / 2
            offsetx2 = offsetx1 + width1
            offsety2 = (height - height2) / 2

            new_page = PageObject.create_blank_page(None, width=width, height=height)

            op1 = Transformation()
            op1 = op1.translate(tx=offsetx1, ty=offsety1) # On bouge la page 1
            page1.add_transformation(op1) # Application du déplacement
            cb1 = page1.cropbox # Récupération des dimensions de la page 1

            rect1 = RectangleObject((cb1.left + offsetx1, cb1.bottom + offsety1, cb1.right + offsetx1, cb1.top + offsety1))
            page1.mediabox = rect1
            page1.cropbox = rect1
            page1.trimbox = rect1
            page1.bleedbox = rect1
            page1.artbox = rect1

            op2 = Transformation()
            op2 = op2.translate(tx=offsetx2, ty=offsety2) # On bouge la page 2
            page2.add_transformation(op2) # Application du déplacement
            cb2 = page2.cropbox # Récupération des dimensions de la page 2

            rect2 = RectangleObject((cb2.left + offsetx2, cb2.bottom + offsety2, cb2.right + offsetx2, cb2.top + offsety2))
            page2.mediabox = rect2
            page2.cropbox = rect2
            page2.trimbox = rect2
            page2.bleedbox = rect2
            page2.artbox = rect2

            new_page.merge_page(page1, expand=False)
            new_page.merge_page(page2, expand=False) # On ajoute la page au fichier de sorti

            self.fpout.add_page(new_page)

            yield 1

    def close(self):
        with open(self.output, "wb") as fp:
            self.fpout.write(fp)

class ArrangerTrio:
    def test_parity(self, file):
        tests_parity = PdfReader(file)
        blank = PageObject.create_blank_page(width = tests_parity.pages[0].mediabox.width,
                                             height = tests_parity.pages[0].mediabox.height)

        t = PdfWriter()
        for page in tests_parity.pages:
            t.add_page(page)

        l = len(tests_parity.pages)
        while l % 6 != 0:
            t.add_page(blank)
            l += 1

        file = Path(file).name

        file = './temp_files/' + file
        f = open(file, 'wb')
        t.write(f)
        f.close()
        return file

    def __init__(self, file, function, output, folder, unit):
        self.unit = unit
        self.function = function
        file = self.test_parity(file)

        self.reader = PdfReader(file) # On ouvre le fichier
        self.fpout = PdfWriter()
        self.output = output
        self.nb_pages = len(self.reader.pages)

        self.nb_iter = int(self.nb_pages/3)

    def run(self):
        for i in range(int(self.nb_pages/3)):
            data = self.function(i, self.nb_pages)
            if len(data) == 4:
                index1, index2, index3, force = data
            else:
                index1, index2, index3, force, alignement = data

            page1 = self.reader.pages[index1] # Récupération des pages
            page2 = self.reader.pages[index2]
            page3 = self.reader.pages[index3]

            width1 = page1.cropbox.right # Largeur de la page 1
            width2 = page2.cropbox.right # Largeur de la page 2
            width3 = page3.cropbox.right # Largeur de la page 3
            height1 = page1.cropbox.top # Hauteur page 1
            height2 = page2.cropbox.top # Hauteur page 2
            height3 = page3.cropbox.top # Hauteur page 3
            width = width1 + width2 + width3
            height = max([height1, height2, height3])
            if force:
                height = PaperSize.A4.width
                width = PaperSize.A4.height

            offsetx1 = (width - width1 - width2 - width3) / 2
            offsety1 = (height - height1) / 2
            offsetx2 = offsetx1 + width1
            offsety2 = (height - height2) / 2
            offsetx3 = offsetx2 + width2
            offsety3 = (height - height3) / 2

            if width >= height:
                width, height = height, width
                offsetx1, offsety1 = offsety1, offsetx1
                offsetx2, offsety2 = offsety2, offsetx2
                offsetx3, offsety3 = offsety3, offsetx3

            new_page = PageObject.create_blank_page(None, width=width, height=height)

            op1 = Transformation()
            op1 = op1.translate(tx=offsetx1, ty=offsety1) # On bouge la page 1
            page1.add_transformation(op1) # Application du déplacement
            cb1 = page1.cropbox # Récupération des dimensions de la page 1

            rect1 = RectangleObject((cb1.left + offsetx1, cb1.bottom + offsety1, cb1.right + offsetx1, cb1.top + offsety1))
            page1.mediabox = rect1
            page1.cropbox = rect1
            page1.trimbox = rect1
            page1.bleedbox = rect1
            page1.artbox = rect1

            op2 = Transformation()
            op2 = op2.translate(tx=offsetx2, ty=offsety2) # On bouge la page 2
            page2.add_transformation(op2) # Application du déplacement
            cb2 = page2.cropbox # Récupération des dimensions de la page 2

            rect2 = RectangleObject((cb2.left + offsetx2, cb2.bottom + offsety2, cb2.right + offsetx2, cb2.top + offsety2))
            page2.mediabox = rect2
            page2.cropbox = rect2
            page2.trimbox = rect2
            page2.bleedbox = rect2
            page2.artbox = rect2

            op3 = Transformation()
            op3 = op3.translate(tx=offsetx3, ty=offsety3) # On bouge la page 3
            page3.add_transformation(op3) # Application du déplacement
            cb3 = page3.cropbox # Récupération des dimensions de la page 3

            rect3 = RectangleObject((cb3.left + offsetx3, cb3.bottom + offsety3, cb3.right + offsetx3, cb3.top + offsety3))
            page3.mediabox = rect3
            page3.cropbox = rect3
            page3.trimbox = rect3
            page3.bleedbox = rect3
            page3.artbox = rect3

            new_page.merge_page(page1, expand=False)
            new_page.merge_page(page2, expand=False)
            new_page.merge_page(page3, expand=False) # On ajoute la page au fichier de sorti

            self.fpout.add_page(new_page)

            yield 1

    def close(self):
        with open(self.output, "wb") as fp:
            self.fpout.write(fp)

class ScaleFile:
    def __init__(self, file, function, output, folder, unit):
        self.unit = unit
        self.file = file
        self.output = output
        self.function = function

        self.pdf = PdfReader(file)
        self.fpout = PdfWriter()
        self.nb_iter = len(self.pdf.pages)

    def run(self):
        for page in self.pdf.pages:
            w = self.function(0, self.nb_iter)
            h = self.function(1, self.nb_iter)
            width = w
            height = h
            adapte = self.function(2, self.nb_iter)
            transform = Transformation()
            rapx = w / float(page.mediabox.width)
            rapy = h / float(page.mediabox.height)
            transform = transform.scale(sx = rapx, sy = rapy)
            if adapte:
                width = PaperSize.A4.width if w >= h else PaperSize.A4.height
                height = PaperSize.A4.width if w < h else PaperSize.A4.height
                tx = (width - w) / 2
                ty = (height - h) / 2
                transform = transform.translate(tx = tx, ty = ty)

            r = RectangleObject((0, 0, width, height))
            page.mediabox = r
            page.cropbox = r

            page.add_transformation(transform)

            blank = PageObject.create_blank_page(width = width, height = height)
            blank.merge_page(page)
            self.fpout.add_page(blank)
            yield 1

    def close(self):
        fp = open(self.output, 'wb')
        self.fpout.write(fp)
        fp.close()

class MarginFile:
    def __init__(self, file, function, output, folder, unit):
        self.unit = unit
        self.file = file
        self.output = output
        self.function = function

        self.pdf = PdfReader(file)
        self.fpout = PdfWriter()

        self.nb_iter = len(self.pdf.pages)

    def run(self):
        for page in self.pdf.pages:
            margin_left = self.function(0, self.nb_iter)
            margin_right = self.function(1, self.nb_iter)
            margin_top = self.function(2, self.nb_iter)
            margin_bottom = self.function(3, self.nb_iter)
            adapte = self.function(4, self.nb_iter)

            transform = Transformation()
            L = float(page.mediabox.width)
            a = L - margin_left - margin_right
            H = float(page.mediabox.height)
            b = H - margin_top - margin_bottom
            width = page.mediabox.width
            height = page.mediabox.height
            
            if adapte:
                width = float(width) + margin_left + margin_right
                height = float(height) + margin_top + margin_bottom
            else:
                transform = transform.scale(sx = a/L, sy = b/H)

            r = RectangleObject((0, 0, width, height))
            page.mediabox = r
            page.cropbox = r
            transform = transform.translate(tx = margin_left, ty = margin_bottom)
            page.add_transformation(transform)

            blank = PageObject.create_blank_page(width = width, height = height)
            blank.merge_page(page)
            self.fpout.add_page(blank)
            yield 1

    def close(self):
        fp = open(self.output, 'wb')
        self.fpout.write(fp)
        fp.close()

class RognerFile:
    def __init__(self, file, function, output, folder, unit):
        self.unit = unit
        self.file = file
        self.output = output
        self.function = function

        self.pdf = PdfReader(file)
        self.fpout = PdfWriter()
        self.nb_iter = len(self.pdf.pages)

    def run(self):
        for i in range(self.nb_iter):
            top, bottom, left, right, page_id = self.function(i, self.nb_iter)
            if page_id == None:
                yield 1
                continue

            page = self.pdf.pages[page_id]
            page.cropbox.top = float(page.cropbox.top) - top*self.unit
            page.cropbox.bottom = bottom*self.unit
            page.cropbox.left = left*self.unit
            page.cropbox.right = float(page.cropbox.right) - right*self.unit
            self.fpout.add_page(page)
            yield 1

    def close(self):
        fp = open(self.output, 'wb')
        self.fpout.write(fp)
        fp.close()

class RotateFile:
    def __init__(self, file, function, output, folder, unit):
        self.unit = unit
        self.file = file
        self.output = output
        self.function = function

        self.pdf = PdfReader(file)
        self.fpout = PdfWriter()
        self.nb_iter = len(self.pdf.pages)

    def run(self):
        for i in range(self.nb_iter):
            page = self.pdf.pages[i]
            angle = self.function(i, self.nb_iter)[0]
            iwidth, height = page.mediabox.width, page.mediabox.height
            if angle == 1: # Transformation horizontale
                op = Transformation((-1, 0, 0, 1, iwidth, 0))
            elif angle == 2: # Transformation verticale
                op = Transformation((1, 0, 0, -1, 0, height))
            else: # Rotation
                op = Transformation()
                op = op.rotate(angle)

            page.add_transformation(op)
            self.fpout.add_page(page)
            yield 1

    def close(self):
        fp = open(self.output, 'wb')
        self.fpout.write(fp)
        fp.close()

class AdditionPage:
    def __init__(self, file, function, output, folder, unit):
        self.unit = unit
        self.file = file
        self.output = output
        self.function = function

        self.pdf = PdfReader(file)
        self.fpout = PdfWriter()
        self.nb_iter = len(self.pdf.pages)

    def run(self):
        for i in range(self.nb_iter):
            page_bg, page_fg, width, height, x, y = self.function(i, self.nb_iter)

            bg = self.pdf.pages[page_bg]
            fg = self.pdf.pages[page_fg]
            if width == 0:
                width = int(bg.mediabox.width)/self.unit
            if height == 0:
                height = int(bg.mediabox.height)/self.unit

            op = Transformation()
            page1 = PageObject.create_blank_page(width = fg.mediabox.width, height = fg.mediabox.height)
            page1.merge_page(fg)
            rx = width*self.unit / int(fg.mediabox.width)
            ry = height*self.unit / int(fg.mediabox.height)
            op = op.scale(rx, ry)
            op = op.translate(tx = x*self.unit, ty = int(bg.mediabox.height) - height * self.unit - y*self.unit)
            page1.add_transformation(op)

            page2 = PageObject.create_blank_page(width = bg.mediabox.width, height = bg.mediabox.height)
            page2.merge_page(bg)
            page2.merge_page(page1)
            self.fpout.add_page(page2)
            yield 1

    def close(self):
        fp = open(self.output, 'wb')
        self.fpout.write(fp)
        fp.close()

def f(i, l):
    if i == 0:
        return 0, 0, 0, 0, 0, 0
    else:
        return 0, i, 0, 0, 10, 10

def htest():
    e = AdditionPage('./tests/jaquette.pdf', f, 'output.pdf', '', 842/297)
    n = 0
    for i in e.run():
        n += i
        print(100 * n/e.nb_iter)
    e.close()

    import os
    os.popen('output.pdf')

if __name__ == '__main__':
    from test import *
    e = Tester()
