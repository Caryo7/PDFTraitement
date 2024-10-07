from PyPDF2 import *
import os


class Poster:
    def __init__(self, file, page, output):
        self.page = page
        self.file = file
        self.output = output
        mm = 10/7.2
        margin = int(15*mm)
        self.margins = {'left': margin, 'right': margin, 'up': margin, 'down': margin}
        self.fpout = PdfWriter()

    def run(self, nw, nh):
        dim_x, dim_y = 1/nw, 1/nh
        areas = []
        for i in range(nw):
            x0 = (1/nw) * (i + 1)
            for j in range(nh):
                y0 = (1/nh) * (j + 1)
                areas.append([dim_x, dim_y, x0, y0])

        for p in areas:
            reader = PdfReader(self.file)
            page = reader.pages[self.page]

            xM = p[2]
            yM = p[3]
            xm = xM - p[0]
            ym = yM - p[1]
            tx = -xm
            ty = -ym

            w, h = page.mediabox.upper_right
            w, h = float(w), float(h)
            blank = PageObject.create_blank_page(width = w, height = h)

            page.cropbox.upper_right = (w*xM, h*yM)
            page.cropbox.downer_left = (w*xm, h*ym)
            transform = Transformation()
            transform = transform.translate(tx = w*tx, ty = h*ty)
            page.add_transformation(transform)

            rapx = (w - (self.margins['left'] + self.margins['right'])) / (w/2)
            rapy = (h - (self.margins['down'] + self.margins['up'])) / (h/2)

            scaler = Transformation()
            scaler = scaler.scale(sx = rapx, sy = rapy)
            scaler = scaler.translate(tx = self.margins['left'], ty = self.margins['down'])
            blank.merge_page(page)
            blank.add_transformation(scaler)

            self.fpout.add_page(blank)

    def close(self):
        fp = open(self.output, 'wb')
        self.fpout.write(fp)
        fp.close()
