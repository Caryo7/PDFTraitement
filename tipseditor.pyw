from tkinter import *
from tkinter.ttk import *
from tkinter import ttk
from tkinter.filedialog import *
from PIL import *
from zipfile import *
from customwidgets import *
import sys

class ImageGenerator:
    def __init__(self, parent):
        self.rtn = None
        self.master = Toplevel(parent)
        self.master.transient(parent)
        self.master.title('Générateur d\'image')
        self.master.columnconfigure(1, weight = 1)
        self.master.rowconfigure(4, weight = 1)
        l1 = ttk.Label(self.master, text = 'Générer une image', font = ('Consolas', 14, 'bold'))
        l1.grid(row = 0, column = 0, padx = 5, pady = 5, columnspan = 2, sticky = 'we')
        l4 = ttk.Label(self.master, text = 'Fichier')
        l4.grid(row = 1, column = 0, padx = 5, pady = 5, sticky = 'e')
        l2 = ttk.Label(self.master, text = 'Hauteur')
        l2.grid(row = 2, column = 0, padx = 5, pady = 5, sticky = 'e')
        l3 = ttk.Label(self.master, text = 'Largeur')
        l3.grid(row = 3, column = 0, padx = 5, pady = 5, sticky = 'e')

        self.rapport = 1
        self.ver = IntVar(value = 1)
        cbt = ttk.Checkbutton(self.master, text = '', onvalue = 1, offvalue = 0, variable = self.ver, command = self.set_rap)
        cbt.grid(row = 2, column = 2, rowspan = 2, padx = 5, pady = 5)

        self.file = StringVar()
        fl = ttk.Entry(self.master, textvariable = self.file)
        fl.grid(row = 1, column = 1, padx = 5, pady = 5, sticky = 'we')
        b = ttk.Button(self.master, text = '...', width = 3, command = self.import_image)
        b.grid(row = 1, column = 2, padx = 5, pady = 5, sticky = 'nswe')

        self.w = ttk.Spinbox(self.master, from_ = 20, to=9999, command = lambda: self.draw(self.w))
        self.w.grid(row = 3, column = 1, padx = 5, pady = 5, sticky = 'we')
        self.h = ttk.Spinbox(self.master, from_ = 20, to=9999, command = lambda: self.draw(self.h))
        self.h.grid(row = 2, column = 1, padx = 5, pady = 5, sticky = 'we')

        self.canvas = Canvas(self.master)
        self.canvas.grid(row = 4, column = 0, columnspan = 2, padx = 5, pady = 5, sticky = 'nswe')
        ok = ttk.Button(self.master, text = 'Insérer', command = self.finish)
        ok.grid(row = 5, column = 0, columnspan = 2, padx = 5, pady = 5, sticky = 'we')

    def import_image(self):
        f = askopenfilename(title = 'Image', filetypes = [('Images', '*.png'), ('Tous les fichiers', '*.*')])
        if f:
            self.file.set(value = str(f))
            a = PhotoImage(file = f)
            h, w = a.width(), a.height()
            r = h/w
            self.rapport = r
            h = 200
            w = int(h * r)
            self.w.set(w)
            self.h.set(h)
            self.draw()

    def set_rap(self):
        self.rapport = int(self.w.get()) / int(self.h.get())

    def draw(self, wid = None):
        if self.ver.get():
            if wid == self.h:
                self.w.set(int(self.rapport * int(self.h.get())))
            elif wid == self.w:
                self.h.set(int(int(self.w.get()) / self.rapport))

        self.canvas.delete('all')
        f = self.file.get()
        try:
            img = Image.open(f)
            img = img.resize((int(self.w.get()), int(self.h.get())))
        except:
            return

        img = ImageTk.PhotoImage(img)
        self.canvas.create_image(10, 10, image = img, anchor = 'nw')
        self.canvas.image = img
        self.master.update()

    def finish(self):
        f = self.file.get()
        if not f:
            return
        try:
            width = int(self.w.get())
            height = int(self.h.get())
        except:
            return

        self.rtn = '<image href="{0}" size="{1}x{2}">'.format(f, width, height)
        self.master.destroy()

    def get(self):
        self.master.wait_window()
        return self.rtn


class App:
    css = {
        'default': [False, {'font': ('Calibri', 12)}],
        'link': [False, {'foreground': 'blue', 'font': ('Calibri', 12, 'underline')}],
        'link_interne': [False, {'foreground': 'blue', 'font': ('Calibri', 12, 'underline')}],
        '1': [True, {'font': ('Calibri', 15, 'bold')}],
        '2': [True, {'font': ('Calibri', 13, 'underline')}],
        '3': [True, {'font': ('Calibri', 14, 'italic')}],
        '5': [False, {'font': ('Courier', 10), 'background': '#f0f0f0'}],
        '6': [False, {'font': ('Cambria', 12)}],
        '7': [False, {'font': ('Lucida Console', 10)}],
        '8': [False, {'font': ('Corbel', 10)}],
        '10': [False, {'font': ('Calibri', 12, 'italic'), 'foreground': '#ffff00'}],
        '11': [False, {'font': ('Calibri', 12), 'foreground': '#ff0000'}],
        }

    def __init__(self, argv):
        self.master = Tk()
        self.master.protocol('WM_DELETE_WINDOW', self.Quitter)
        self.master.title('Documentation - untitled.tips')
        self.master.columnconfigure(1, weight = 1)
        self.master.rowconfigure(1, weight = 1)

        self.file = 'untitled.tips'
        self.datas = {'untitled.tips': {'content': '', 'meta': '[meta]\nname = Sans Nom 001\nid = 001', 'saved': True, 'path': None},}

        styles = Frame(self.master)
        styles.grid(row = 0, column = 0, sticky = 'nswe', columnspan = 4)

        self.cmds = [
            {'balise': 'a', 'text': 'Lien', 'cmd': lambda: self.add_style('link'), 'tooltip': '<a href=""></a>'},
            {'balise': 'a', 'text': 'Lien interne', 'cmd': lambda: self.add_style('link_interne'), 'tooltip': '<a href="this."></a>'},
            {'balise': 'h1', 'text': 'Titre 1', 'cmd': lambda: self.add_style('h1'), 'tooltip': '<h1></h1>'},
            {'balise': 'h2', 'text': 'Titre 2', 'cmd': lambda: self.add_style('h2'), 'tooltip': '<h2></h2>'},
            {'balise': 'h3', 'text': 'Titre 3', 'cmd': lambda: self.add_style('h3'), 'tooltip': '<h3></h3>'},
            {'balise': 'h5', 'text': 'Programme Basique', 'cmd': lambda: self.add_style('h5'), 'tooltip': '<h5></h5>'},
            {'balise': 'h6', 'text': 'Mathématiques', 'cmd': lambda: self.add_style('h6'), 'tooltip': '<h6></h6>'},
            {'balise': 'h7', 'text': 'Terminal', 'cmd': lambda: self.add_style('h7'), 'tooltip': '<h7></h7>'},
            {'balise': 'h8', 'text': 'Bouton', 'cmd': lambda: self.add_style('h8'), 'tooltip': '<h8></h8>'},
            {'balise': 'h10', 'text': 'Note', 'cmd': lambda: self.add_style('h10'), 'tooltip': '<h10></h10>'},
            {'balise': 'h11', 'text': 'Attention', 'cmd': lambda: self.add_style('h11'), 'tooltip': '<h11></h11>'},
            {'balise': 'b', 'text': 'Gras', 'cmd': lambda: self.add_style('b'), 'tooltip': '<b></b>'},
            {'balise': 'i', 'text': 'Italique', 'cmd': lambda: self.add_style('i'), 'tooltip': '<i></i>'},
            {'balise': 'u', 'text': 'Souligné', 'cmd': lambda: self.add_style('u'), 'tooltip': '<u></u>'},
            {'balise': 'center', 'text': 'Centré', 'cmd': lambda: self.add_style('center'), 'tooltip': '<center></center>'},
            {'balise': 'image', 'text': 'Image', 'cmd': lambda: self.add_style('image'), 'tooltip': '<image>'},
            ]

        col = 0
        row = 0
        for i in range(len(self.cmds)):
            self.cmds[i]['widget'] = Button(styles, text = self.cmds[i]['text'], command = self.cmds[i]['cmd'])
            self.cmds[i]['widget'].grid(row = row, column = col, padx = 5, pady = 5)
            ToolTip(self.cmds[i]['widget'], self.cmds[i]['tooltip'])
            col += 1
            if col > 10:
                col = 0
                row += 1

        self.liste = Listbox(self.master, width = 40)
        self.liste.grid(row = 1, column = 0, sticky = 'nswe')
        self.liste.bind('<<ListboxSelect>>', self.select_file)
        self.liste.insert('end', 'untitled.tips')

        scroll = Scrollbar(self.master, orient = 'vertical')
        scroll.grid(row = 1, column = 2, sticky = 'ns')
        self.text = Text(self.master, yscrollcommand = scroll.set, wrap = WORD)
        self.text.grid(row = 1, column = 1, sticky = 'nswe')
        self.text.bind('<KeyPress>', self.unsave)
        self.text.bind('<KeyRelease>', self.color)
        self.text.bind('<Control-s>', self.save_file)
        self.text.bind('<Control-o>', self.open_file)
        self.text.bind('<Control-n>', self.new_file)
        self.text.bind('<Control-w>', self.close)
        self.text.bind('<Control-p>', self.show)
        self.text.bind('<Button-3>', self.clk_right)
        scroll.config(command = self.text.yview)

        self.meta = Text(self.master, width = 40, wrap = WORD)
        self.meta.grid(row = 1, column = 3, sticky = 'nswe')
        self.meta.bind('<KeyPress>', self.unsave)
        self.meta.bind('<KeyRelease>', self.color)

        menubar = Menu(self.master)
        self.master['menu'] = menubar
        menubar.add_command(label = 'Nouveau', command = self.new_file)
        menubar.add_command(label = 'Ouvrir', command = self.open_file)
        menubar.add_command(label = 'Enregistrer', command = self.save_file)
        menubar.add_command(label = 'Fermer', command = self.close)
        menubar.add_command(label = 'Quitter', command = self.master.destroy)
        menubar.add_command(label = 'Afficher', command = self.show)

        self.master.geometry('1000x500')

        if len(argv) >= 2:
            for i in range(len(argv)-1):
                self.open_file(a = argv[1+i])

    def select_file(self, evt = None):
        s = self.liste.curselection()
        if len(s) == 1:
            f = self.liste.get(s)
            self.switch(f)

    def clk_right(self, evt):
        popup = Menu(self.text, tearoff = 0)
        for cmd in self.cmds:
            popup.add_command(label = cmd['text'], command = cmd['cmd'], accelerator = cmd['tooltip'])
        popup.tk_popup(evt.x_root, evt.y_root)

    def color(self, evt):
        for t in self.text.tag_names():
            self.text.tag_delete(t)

        for c in self.cmds + [{'balise': 'image'}]:
            bal = c['balise']
            for i in range(2):
                balise = '<' if i == 0 else '</'
                balise += bal
                start = '1.0'
                while True:
                    start = self.text.search(balise, start, 'end')
                    if not start:
                        break

                    end = self.text.search('>', start, 'end')
                    if not end:
                        break

                    self.text.tag_add(balise, start, end+'+1c')
                    start = end

                if bal == 'image':
                    self.text.tag_configure(balise, foreground = '#0000ff')
                else:
                    self.text.tag_configure(balise, foreground = '#ff0000')

        start = '1.0'
        end = None
        while True:
            start = self.meta.search('\n', start, 'end')
            if not start:
                break

            if end != None:
                self.meta.tag_add('value', end, start)

            end = self.meta.search('=', start, 'end')
            if not end:
                break

            self.meta.tag_add('key', start, end)
            start = end

        start = '1.0'
        end = None
        while True:
            start = self.meta.search('[', start, 'end')
            if not start:
                break

            end = self.meta.search(']', start, 'end')
            if not end:
                break

            self.meta.tag_add('sect', start, end+'+1c')
            start = end

        self.meta.tag_configure('key', foreground = 'red')
        self.meta.tag_configure('value', foreground = 'blue')
        self.meta.tag_configure('sect', foreground = 'green')

    def layout_html(self):
        txt = self.text.get('0.0', 'end')
        while txt[-1] == '\n':
            txt = txt[:-1]

        txt = txt.replace('\n', '</p><p>')
        txt = '<p>' + txt + '</p>'
        self.color(None)
        return txt

    def show(self, evt = None):
        zak = Toplevel(self.master)
        zak.transient(self.master)
        zak.title('Aperçu')
        zak.columnconfigure(0, weight = 1)
        zak.rowconfigure(0, weight = 1)

        html = HTML(zak, view = 'table.scroll.summ')
        html.grid(sticky = 'nswe')
        for k, v in self.css.items():
            html.css[k] = v
        html.add_content(self.layout_html())

        zak.wait_window()

    def close(self, evt = None):
        if not self.datas[self.file]['saved'] or not self.datas[self.file]['path']:
            ask = askyesnocancel('Fermeture', 'Voulez vous enregistrer avant de fermer ?')
            if ask:
                self.save_file()
            elif ask == None:
                return

        self.text.delete('0.0', 'end')
        self.meta.delete('0.0', 'end')
        index = self.liste.get(0, "end").index(self.file)
        self.liste.delete(index)
        del self.datas[self.file]
        self.file = None

        if len(self.datas) == 0:
            self.new_file()
        else:
            self.switch(list(self.datas.keys())[-1])

    def new_file(self, evt = None):
        self.datas['untitled.tips'] = {'content': '', 'meta': '', 'saved': False, 'path': None}
        self.liste.insert('end', 'untitled.tips')
        self.switch('untitled.tips')

    def Quitter(self):
        for k, v in self.datas.items():
            self.switch(k)
            if not v['saved'] or not v['path']:
                ask = askyesnocancel('Fermeture', 'Voulez vous enregistrer le fichier {} avant de fermer ?'.format(k))
                if ask:
                    self.save_file()
                elif ask == None:
                    return

        self.master.destroy()

    def add_style(self, balise):
        if 'image' == balise:
            sapp = ImageGenerator(self.master)
            txt = sapp.get()
            if txt:
                self.text.insert('insert', txt)

        self.color(None)

        try:
            from_ = self.text.index('sel.first')
            to = self.text.index('sel.last')
        except:
            return

        txt = self.text.get(from_, to)

        if 'link' == balise:
            self.text.insert(to, '</a>')
            self.text.insert(from_, '<a href="' + txt + '">')

        elif 'link_interne' == balise:
            self.text.insert(to, '">voir plus</a>)')
            self.text.insert(from_, '(<a href="this.')

        else:
            self.text.insert(to, '</' + balise + '>')
            self.text.insert(from_, '<' + balise + '>')

        self.unsave()
        self.color(None)

    def unsave(self, evt = None):
        if evt:
            for k in ['control', 'alt', 'iso', 'shift']:
                if k in evt.keysym.lower(): return

        self.datas[self.file]['saved'] = False
        self.master.title('* Documentation - ' + self.file + ' *')

    def setsave(self):
        self.datas[self.file]['saved'] = True
        self.master.title('Documentation - ' + self.file)

    def open_file(self, evt = None, a = None):
        if a == None:
            a = askopenfilename(title = 'Ouvrir', filetypes = [('Fichier Astuces', '*.tips')])
        if a:
            f = ZipFile(a, 'r')
            txt = f.read('content.html').decode('utf-8')
            meta = f.read('meta.ini').decode('utf-8')
            f.close()

            txt = txt.replace('\n', '')
            txt = txt.replace('<p>', '')
            txt = txt.replace('</p>', '\n')
            f = str(Path(a).name)
            self.datas[f] = {'content': txt, 'meta': meta, 'saved': True, 'path': a}
            self.liste.insert('end', f)
            self.switch(f)

    def save_file(self, evt = None):
        if not self.datas[self.file]['path']:
            a = asksaveasfilename(title = 'Enregistrer sous', filetypes = [('Fichier documentation', '*.html')])
            if not a:
                return

            f = str(Path(a).name)
            index = self.liste.get(0, "end").index(self.file)
            self.liste.delete(index)
            self.liste.insert(index, f)
            self.datas[self.file]['path'] = a
            self.datas[f] = self.datas[self.file]
            del self.datas[self.file]
            self.switch(f)

        fs = open('./tips/style.css', 'rb')
        r = fs.read()
        fs.close()

        z = ZipFile(self.datas[self.file]['path'], 'w')
        f = z.open('content.html', 'w')
        f.write(self.layout_html().encode('utf-8'))
        f.close()

        m = self.meta.get('0.0', 'end')
        while m[-1] == '\n':
            m = m[:-1]
        f = z.open('meta.ini', 'w')
        f.write(m.encode('utf-8'))
        f.close()

        f = z.open('style.css', 'w')
        f.write(r)
        f.close()

        z.close()
        self.setsave()

    def switch(self, file):
        if self.file != None:
            r = self.text.get('0.0', 'end')
            m = self.meta.get('0.0', 'end')
            try:
                while r[-1] == '\n': r = r[:-1]
                while m[-1] == '\n': m = m[:-1]
            except:
                pass
            self.datas[self.file]['content'] = r
            self.datas[self.file]['meta'] = m

        self.file = file
        index = self.liste.get(0, "end").index(self.file)
        self.liste.selection_clear('0', 'end')
        self.liste.selection_set(index)
        self.text.delete('0.0', 'end')
        self.text.insert('end', self.datas[self.file]['content'])
        self.meta.delete('0.0', 'end')
        self.meta.insert('end', self.datas[self.file]['meta'])
        self.color(None)

        if self.datas[self.file]['saved']:
            self.master.title('Documentation - ' + self.file)
        else:
            self.master.title('* Documentation - ' + self.file + ' *')

    def Generate(self):
        self.master.mainloop()

if __name__ == '__main__':
    a = App(sys.argv)
    a.Generate()
