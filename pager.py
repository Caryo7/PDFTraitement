from tkinter import *
from tkinter import ttk
from tkinter.ttk import *
from customwidgets import *

class Object:
    def __init__(self, name = None, page = 0):
        self.name = name
        self.x = 0
        self.y = 0
        self.width = 0
        self.height = 0
        self.page = page
        widget = None

class Page:
    kind = 'page'
    width = 140
    height = 210
    ox = 0
    ox = 0

    def __init__(self, name = None):
        self.name = name

class TextValue(Object):
    kind = 'text'
    content = ''
    css = ''

def mm(value):
    return int(value*4.7)

class Zoomer:
    def __init__(self):
        self.zoom = 1
        self.ox = 0
        self.oy = 0

    def config(self, ox, oy):
        self.ox = ox
        self.oy = oy

    def set_zoom(self, zoom):
        self.zoom = zoom

    def zm(self, value, from_o = True):
        if not from_o:
            return int(self.zoom * value)
        elif from_o == 'y':
            return int(self.zoom * (self.oy - value))
        elif from_o == 'x':
            return int(self.zoom * (self.ox - value))

class Pager:
    def __init__(self, parent):
        self.variables = {}
        self.content = [Page(0), TextValue('entry1', 0)]
        self.content[1].width = 30
        self.content[1].height = 30
        self.pages = {}

        self.parent = parent
        self.master = Toplevel(parent)
        self.TITLE = 'Création de PDF'
        self.master.title(self.TITLE)
        self.master.protocol('WM_DELETE_WINDOW', self.Quitter)
        self.master.columnconfigure(0, weight = 1)
        self.master.rowconfigure(0, weight = 1)
        self.master.geometry('1000x800')

        xscroll = ttk.Scrollbar(self.master, orient = 'horizontal')
        xscroll.grid(row = 1, column = 0, sticky = 'we')
        yscroll = ttk.Scrollbar(self.master, orient = 'vertical')
        yscroll.grid(row = 0, column = 1, sticky = 'ns')

        self.canvas = Canvas(self.master, yscrollcommand = yscroll.set, xscrollcommand = xscroll.set)
        self.canvas.grid(row = 0, column = 0, sticky = 'nswe')
        xscroll.config(command = self.canvas.xview)
        yscroll.config(command = self.canvas.yview)

        self.zoom = Zoomer()
        self.zm = lambda value, mode: self.zoom.zm(value, mode)
        self.draw()

    def draw(self):
        self.canvas.delete('all')
        for element in self.content:
            if element.kind == 'page':
                if len(self.pages) == 0:
                    ox, oy = 0, 0
                else:
                    ox = 0
                    oy = self.pages[list(self.pages.keys())[-1]].oy + 10

                self.canvas.create_rectangle(ox, oy, self.zm(ox + mm(element.width), False), self.zm(oy + mm(element.height), False), fill = 'white')
                element.ox = ox
                element.oy = oy + mm(element.height)
                self.pages[element.name] = element
                continue
            else:
                ox = self.pages[element.page].ox
                oy = self.pages[element.page].oy
                self.zoom.config(ox, oy)

            if element.kind == 'text':
                element.widget = HTML(self.canvas, 'noscroll.notable')
                element.widget.load_css(content = element.css)
                element.widget.add_content(element.content)
                element.widget.config(width = self.zm(mm(element.width), False), height = self.zm(mm(element.height), False))

                print(self.zoom.ox, self.zoom.oy)
                self.canvas.create_window(self.zm(mm(element.x), 'x'), self.zm(mm(element.y), 'y'), window = element.widget)

        region = list(self.canvas.bbox('all'))
        region = [i - 10 for i in region]
        self.canvas.configure(scrollregion = region)

    def Quitter(self):
        self.master.destroy()

    def Generate(self):
        self.master.wait_window()
        
if __name__ == '__main__':
    root = Tk()
    root.iconify()
    app = Pager(root)
    app.Generate()
    root.mainloop()
