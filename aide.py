from tkinter import *
from tkinter import ttk
from customwidgets import *
from pathlib import Path

class About:
    curseurs = ['arrow', 'man', 'based_arrow_down', 'middlebutton', 'based_arrow_up', 'mouse', 'boat', 'pencil', 'bogosity', 'pirate', 'bottom_left_corner', 'plus',
                'bottom_right_corner', 'question_arrow', 'bottom_side', 'right_ptr', 'bottom_tee', 'right_side', 'box_spiral', 'right_tee', 'center_ptr', 'rightbutton', 'circle',
                'rtl_logo', 'clock', 'sailboat', 'coffee_mug', 'sb_down_arrow', 'cross', 'sb_h_double_arrow', 'cross_reverse', 'sb_left_arrow', 'crosshair', 'sb_right_arrow',
                'diamond_cross', 'sb_up_arrow', 'dot', 'sb_v_double_arrow', 'dotbox', 'shuttle', 'double_arrow', 'sizing', 'draft_large', 'spider', 'draft_small', 'spraycan',
                'draped_box', 'star', 'exchange', 'target', 'fleur', 'tcross', 'gobbler', 'top_left_arrow', 'gumby', 'top_left_corner', 'hand1', 'top_right_corner', 'hand2',
                'top_side', 'heart', 'top_tee', 'icon', 'trek', 'iron_cross', 'ul_angle', 'left_ptr', 'umbrella', 'left_side', 'ur_angle', 'left_tee', 'watch', 'leftbutton',
                'xterm', 'll_angle', 'X_cursor', 'lr_angle']

    def __init__(self, parent, Imager):
        self.root = Toplevel(parent)
        self.root.transient(parent)
        self.root.iconbitmap(Imager.ICONS['Help'])
        self.root.config(borderwidth = 5)
        self.root.title('A propos')
        self.root.columnconfigure(1, weight = 1)
        self.root.rowconfigure(1, weight = 1)

        style = ttk.Style()
        style.configure('Aide.TFrame', bg = '#bbbbbb')
        style.configure('Name.TLabel', fg = '#000000', font = ('Courier', 20, 'bold'))
        style.configure('Aide.TLabel', bg = '#bbbbbb', fg = '#000000', font = ('Courier', 11, ''), justify = 'left')
        style.configure('Link.TLabel', bg = '#bbbbbb', foreground = 'blue', font = ('Courier', 11, 'underline'), cursor = 'hand2', justify = 'left')
        style.configure('Sep.TFrame', bg = '#bbbbbb', height = 2, relief = 'sunken', borderwidth = 1)
        style.configure('Aide.TButton', relief = SOLID, bd = 3)

        ong = ttk.Notebook(self.root)
        ong.grid(row = 1, column = 0, columnspan = 2, padx = 5, pady = 5, sticky = 'nswe')
        cad = ttk.Frame(ong, style = 'Aide.TFrame')
        cad.columnconfigure(0, weight = 1)
        cad.columnconfigure(1, weight = 1)
        ong.add(text = 'Version', child = cad)

        img = Imager.Logo.size64
        logo = ttk.Frame(self.root, style = 'Aide.TFrame')
        logo.grid(row = 0, column = 0, sticky = 'we', padx = 10, pady = 0, columnspan = 2)
        lb = Label(logo, image = img)
        lb.grid(row = 0, column = 0, sticky = 'e', rowspan=2, padx = 10, pady = 0)
        lb.image = img
        ttk.Label(logo, text = 'Traitement de PDF', style = 'Aide.TLabel').grid(row = 0, column = 1, sticky = 'e', padx = 10, pady = 0)

        self.URL = 'https://benoit.charreyron.com/'
        url = self.URL.replace('https://', '')
        url = url.split('/')
        url = url[0]

        dic = {'Version :': '1.0',
               'Site internet :': url,
               'Copyright :': 'All Right Reserved',
               'separator1': None,
               'Python :': '3.12.2',
               'separator2': None,
               'Interface Graphique': '2.0',
               'Compilateur': '2.0',
               'Langues': '0.0',
               'Version de l\'interface fichier': '3.0',
               'Version des PDFPRO': '1.0',
               'Version des PDFSEA': '2.0',}

        row = 1
        for k, v in dic.items():
            if not v:
                ttk.Frame(cad, style = 'Sep.TFrame').grid(row=row, column=0, sticky='ew', columnspan=3, padx=5, pady=5)

            else:
                ttk.Label(cad, text = k, style = 'Aide.TLabel').grid(row = row, column = 0, sticky = 'e', padx = 0, pady = 5)
                l = ttk.Label(cad, text = v, justify = 'left', style = 'Aide.TLabel', cursor = 'hand2' if k == 'Site internet :' else None)
                l.grid(row = row, column = 1, sticky = 'w', padx = 10, pady = 5)
                if k == 'Site internet :':
                    l.bind('<Button-1>', lambda evt: self.URL)
                    l.config(style = 'Link.TLabel')

            row += 1

        h, w = 23, 70

        auth = ttk.Frame(ong, style = 'Aide.TFrame')
        auth.columnconfigure(0, weight = 1)
        auth.rowconfigure(0, weight = 1)
        ong.add(text = 'Auteurs', child = auth)
        ta = HTML(auth, view = 'text.noscroll', width = w, bg = '#f0f0f0', fg = 'black', height = h)
        ta.grid(sticky = 'nswe')
        ta.css = {'default': [False, {'font': ('Courier', 10)}],
                  'link': [False, {'foreground': 'blue', 'font': ('Courier', 10, 'underline')}],
                  '1': [False, {'font': ('Courier', 13, 'bold')}],
                  '2': [False, {'font': ('Courier', 10, 'underline')}],
                  '3': [False, {'font': ('Courier', 10, 'italic')}],
             }

        f = open('./docs/authors.html', 'r', encoding = 'utf-8')
        ta.add_content(f.read())
        f.close()

        cpr = ttk.Frame(ong, style = 'Aide.TFrame')
        cpr.columnconfigure(0, weight = 1)
        cpr.rowconfigure(0, weight = 1)
        ong.add(text = 'License', child = cpr)
        t = HTML(cpr, view = 'text.scroll', width = w, bg = '#f0f0f0', fg = 'black', height = h, font = ('Courier', 10))
        t.grid(row = 0, column = 0, sticky = 'nswe')
        f = open('./docs/license.html', 'r', encoding = 'utf-8')
        t.add_content(f.read())
        f.close()

        def close():
            self.root.destroy()
            self.dialoging = False

        ttk.Button(self.root, text = 'Fermer', command = close, style = 'Aide.TButton').grid(row = 2, column = 0, padx = 20, pady = 10, columnspan = 2, sticky = 'we')
        self.root.bind('<Escape>', lambda evt: close())
        self.root.bind('<Return>', lambda evt: close())
        self.root.update()

    def Generate(self):
        self.root.wait_window()


class Documentation:
    def __init__(self, file, parent, Imager):
        if file == 'all':
            content = ''
            p = Path('./docs/')
            files = list(p.glob('**/*.html'))
            sorted(files)
            for file in files:
                if '-' not in str(file):
                    continue

                fp = open(file, 'r', encoding = 'utf-8')
                if '-' not in str(file):
                    name = str(file.name).replace('.html', '')
                    content += '<p><h1>' + name.capitalize() + '</h1></p>\n'

                content += fp.read() + '\n<p></p>'
                fp.close()

        else:
            f = open(file, 'r', encoding = 'utf-8')
            content = f.read()
            f.close()

        self.master = Toplevel(parent)
        self.master.iconbitmap(Imager.ICONS['Help'])
        self.master.transient(parent)
        self.master.title('Documentation')
        self.master.columnconfigure(0, weight = 1)
        self.master.rowconfigure(0, weight = 1)

        self.text = HTML(self.master, view = 'table.scroll.summ')
        self.text.grid(sticky = 'nswe')
        self.text.load_css('./docs/style.css')

        self.text.add_content(content)

    def Generate(self):
        self.master.wait_window()

if __name__ == '__main__':
    from test import *
    e = Tester(['show_aide'])
