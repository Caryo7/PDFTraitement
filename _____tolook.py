from tkinter import *
from tkinter import ttk
from tkinter.ttk import *
from tkinter.filedialog import *
from tkinter.simpledialog import *
from io import BytesIO
import win32clipboard
from output import *
from pathlib import *
from printsettings import *
import PIL.Image as Image
from scorelayout import *
from PIL import Image, ImageTk
from livret import *

def TextView(data, root, pm, icons):
    master = Toplevel(root)
    master.transient(root)
    master.title('Vue du texte')
    master.resizable(False, False)

    scroll = ttk.Scrollbar(master, orient = 'vertical')
    scroll.grid(row = 1, column = 2, sticky = 'ns', pady = 5, padx = 5)
    text = Text(master, width = pm.textview_width, height = pm.textview_height, yscrollcommand = scroll.set, wrap = 'word', insertbackground = pm.textview_cursor)
    text.grid(row = 1, column = 0, columnspan = 2, padx = 5, pady = 5)
    scroll.config(command = text.yview)

    i = 0
    for t in data:
        i += 1
        ind = ' Page ' + str(i) + ' '
        separation = '*' * (int(pm.textview_width/2) - int(len(ind)/2))
        separation += ind
        separation += '*' * (pm.textview_width - len(separation))
        separation += '\n\n'
        text.insert('end', separation)
        text.insert('end', t)
        text.insert('end', '\n\n')

    def copy():
        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardText(text.get('0.0', 'end').encode('utf-8'))
        win32clipboard.CloseClipboard()

    cl = ttk.Button(master, text = 'FERMER', command = master.destroy, image = icons('Close', True), compound = 'left')
    cl.grid(row = 0, column = 0, padx = 5, pady = 5, sticky = 'we')
    cop = ttk.Button(master, text = 'COPIER', command = copy, image = icons('Copy', True), compound = 'left')
    cop.grid(row = 0, column = 1, padx = 5, pady = 5, sticky = 'we')


class ImageView:
    def __init__(self, images, root, pm, icons):
        self.images = images
        master = Toplevel(root)
        master.transient(root)
        master.title('Vue d\'images')
        master.resizable(False, False)
        self.old_path = '.'

        cop = ttk.Button(master, text = 'COPIER', command = self.copy, image = icons('Copy', True), compound = 'left')
        cop.grid(row = 0, column = 0, padx = 5, pady = 5, sticky = 'we')
        sav = ttk.Button(master, text = 'ENREGISTRER SOUS', command = self.saveas, image = icons('Save', True), compound = 'left')
        sav.grid(row = 0, column = 1, padx = 5, pady = 5, sticky = 'we')
        prv = ttk.Button(master, text = 'PRECEDENTE', command = self.prev_image, image = icons('LeftArrow', True), compound = 'left')
        prv.grid(row = 0, column = 2, padx = 5, pady = 5, sticky = 'we')
        nxt = ttk.Button(master, text = 'SUIVANTE', command = self.next_image, image = icons('RightArrow', True), compound = 'left')
        nxt.grid(row = 0, column = 3, padx = 5, pady = 5, sticky = 'we')
        clo = ttk.Button(master, text = 'FERMER', command = master.destroy, image = icons('Close', True), compound = 'left')
        clo.grid(row = 0, column = 4, padx = 5, pady = 5, sticky = 'we')

        self.pos = ttk.Scale(master, orient = 'horizontal', from_ = 1, to = len(self.images))
        self.pos.grid(row = 1, column = 0, columnspan = 5, padx = 5, pady = 5, sticky = 'we')
        self.pos.config(command = self.move)

        self.w, self.h = pm.imageview_width, pm.imageview_height
        self.canvas = Canvas(master, width = self.w, height = self.h)
        self.canvas.grid(row = 2, column = 0, columnspan = 5, padx = 5, pady = 5)

        self.index = None if len(self.images) == 0 else 0
        self.draw()

    def saveas(self):
        if self.index == None:
            return

        file = self.images[self.index]
        n = len(file) - 1
        while file[n] != '.':
            n -= 1
        ext = file[n:]
        path = asksaveasfilename(title = 'Enregistrer sous', initialdir = self.old_path, filetypes = [('Image', '*' + ext)])
        if path:
            n = len(path) - 1
            while path[n] != '.':
                n -= 1
            if path[n:] != ext:
                path += ext

            self.old_path = str(Path(path).parent)
            ffrom = open(file, 'rb')
            fto = open(path, 'wb')
            fto.write(ffrom.read())
            ffrom.close()
            fto.close()

    def move(self, evt = None):
        if self.index != None:
            p = int(round(self.pos.get(), 0))
            self.index = p-1
            self.draw(noscale = True)

    def draw(self, noscale = False):
        self.canvas.delete('all')
        x, y = int(self.w/2), int(self.h/2)
        if self.index == None:
            self.canvas.create_text(x, y, text = 'Pas d\'images dans le fichier', font = ('Consolas', 16))
            return

        self.PILimage = Image.open(self.images[self.index])
        w, h = self.PILimage.width, self.PILimage.height
        zm = 1
        if w > self.w or h > self.h:
            zmw, zmh = 1, 1
            if w > self.w:
                zmw = self.w / w
            if h > self.h:
                zmh = self.h / h

            if zmh > zmw:
                zm = zmw
            else:
                zm = zmh

        image = self.PILimage.resize((int(w * zm), int(h * zm)))
        image = ImageTk.PhotoImage(image)
        self.canvas.create_image(x, y, image = image)
        self.canvas.image = image
        if not noscale:
            self.pos.set(self.index+1)

    def copy(self):
        if self.index == None:
            return

        def send_to_clipboard(clip_type, data):
            win32clipboard.OpenClipboard()
            win32clipboard.EmptyClipboard()
            win32clipboard.SetClipboardData(clip_type, data)
            win32clipboard.CloseClipboard()

        image = self.PILimage
        output = BytesIO()
        image.convert("RGB").save(output, "BMP")
        data = output.getvalue()[14:]
        output.close()
        send_to_clipboard(win32clipboard.CF_DIB, data)

    def next_image(self):
        if self.index == None:
            return

        if self.index < len(self.images) - 1:
            self.index += 1
            self.draw()

    def prev_image(self):
        if self.index == None:
            return

        if self.index > 0:
            self.index -= 1
            self.draw()


class PosterConfig:
    def __init__(self, parent, image, pm, icon, path):
        self.tv = parent
        self.img = image
        self.pm = pm
        self.icon = icon
        self.path = path
        self.carres = []

        self.root = Toplevel(self.tv)
        self.root.transient(self.tv)
        self.root.title('Poster Generator')
        self.root.columnconfigure(1, weight = 1)
        self.root.columnconfigure(3, weight = 1)
        self.root.rowconfigure(1, weight = 1)

        l = Label(self.root, text = 'Grille de')
        l.grid(row = 0, column = 0, padx = 5, pady = 5, sticky='e')

        self.cutinw = IntVar(value = 2)
        ctw = ttk.Spinbox(self.root, from_ = 2, to = self.pm.maxcut, textvariable = self.cutinw)
        ctw.grid(row = 0, column = 1, padx = 5, pady = 5, sticky='we')
        ctw.set(2)

        i = Label(self.root, text = 'par')
        i.grid(row = 0, column = 2, padx = 5, pady = 5, sticky='we')

        self.cutinh = IntVar(value = 2)
        cth = ttk.Spinbox(self.root, from_ = 2, to = self.pm.maxcut, textvariable = self.cutinh)
        cth.grid(row = 0, column = 3, padx = 5, pady = 5, sticky='we')
        cth.set(2)

        p = Label(self.root, text = 'pages')
        p.grid(row = 0, column = 4, padx = 5, pady = 5, sticky = 'w')

        self.area = Canvas(self.root, bg = 'red')
        self.area.grid(row = 1, column = 0, columnspan = 5, padx = 5, pady = 5, sticky='nswe')

        okbt = ttk.Button(self.root, text = 'Exporter', command = self.export)
        okbt.grid(row = 2, column = 0, columnspan = 5, padx = 5, pady = 5, sticky = 'we')

        self.draw()
        self.root.bind('<Configure>', self.resize_win)
        self.cutinw.trace('w', lambda *args: self.draw())
        self.cutinh.trace('w', lambda *args: self.draw())

    def export(self):
        self.carres = []
        w, h = self.cutinw.get(), self.cutinh.get()
        for i in range(w):
            x0 = (1/w) * i
            x1 = (1/w) * (i + 1)
            for j in range(h):
                y0 = (1/h) * j
                y1 = (1/h) * (j + 1)
                self.carres.append([x0, y0, x1, y1])

        self.root.destroy()

    def resize_win(self, evt):
        if evt.widget == self.root:
            self.draw()

    def resize_image(self, img_file, width, height, force=None):
        w, h = img_file.width, img_file.height # Dimensions
        zm = 1
        if w > width or h > height: # Calcul du zoom
            zmw, zmh = 1, 1
            if w > width:
                zmw = width / w
            if h > height:
                zmh = height / h

            if zmw < zmh:
                zm = zmw
            else:
                zm = zmh

            if force == 'width':
                zm = zmw
            elif force == 'height':
                zm = zmh

        zm -= 0.01
        image = img_file.resize((int(w*zm), int(h*zm)))
        self.size_page = [int(w*zm), int(h*zm)]
        return image

    def draw(self):
        self.area.delete('all')
        w, h = self.area.winfo_width(), self.area.winfo_height()
        if w < 10 or h < 10:
            w, h = self.area.winfo_reqwidth(), self.area.winfo_reqheight()
        cx, cy = w/2, h/2
        
        image = self.resize_image(self.img, w, h)
        image = ImageTk.PhotoImage(image)
        self.area.create_image(cx, cy, image = image, anchor = 'center')
        self.area.image = image

        nb_height = int(self.cutinh.get())
        nb_width = int(self.cutinw.get())
        x_left = cx - (self.size_page[0]/2)
        x_right = cx + (self.size_page[0]/2)
        y_top = cy - (self.size_page[1]/2)
        y_bottom = cy + (self.size_page[1]/2)

        for i in range(nb_height+1):
            self.area.create_line(x_left, y_top + i*(self.size_page[1]/nb_height), x_right, y_top + i*(self.size_page[1]/nb_height), fill = 'black')

        for i in range(nb_width+1):
            self.area.create_line(x_left + i*(self.size_page[0]/nb_width), y_top, x_left + i*(self.size_page[0]/nb_width), y_bottom, fill = 'black')

    def wait(self):
        self.root.wait_window()
        return self.carres
