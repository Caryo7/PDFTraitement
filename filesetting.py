from tkinter import *
from tkinter.filedialog import *
from confr import *
from pathlib import *

class FileTypes:
    filetypes = {
        'PDF': {'ext': [('Fichiers Portable Document Format', '*.pdf *.pdff')], 'exts': ['.pdf', '.pdff'], 'default': '.pdf'},
        'CSV': {'ext': [('Tous les fichiers pris en charge', '*.csv *.txt *.log *.xlsx'), ('Fichiers CSV', '*.csv'), ('Fichiers texte', '*.txt *.log'), ('Fichiers Excel', '*.xlsx')], 'exts': ['.csv', '.txt', '.log', '.xlsx'], 'default': '.csv'},
        'PRO': {'ext': [('Projet de Traitement', '*.pdfpro')], 'exts': ['.pdfpro'], 'default': '.pdfpro'},
        'SEA': {'ext': [('Fonction pour les programmes', '*.pdfsea')], 'exts': ['.pdfsea'], 'default': '.pdfsea'},
        'IMG': {'ext': [('Toutes les images prises en charge', '*.png *.jpg *.jpeg *.gif *.tif *.bmp *.ico *.webp')], 'exts': ['.png', '.jpg', '.jpeg', '.gif', '.tif', '.bmp', '.ico', '.webp'], 'default': '.png'},
        'ALL': {'ext': [('Tous les fichiers', '*.*')], 'default': '.pdf'},
        }

    def __init__(self, paras):
        self.initialdir_open = paras['open']
        self.initialdir_save = paras['save']
        self.initialdir_dir = paras['dir']
        self.rem_open = paras['rem_open']
        self.rem_save = paras['rem_save']
        self.rem_dir = paras['rem_dir']

    def open_file(self, title, filetype = 'PDF', initialdir = None, multiple = False):
        if initialdir == None:
            initialdir = self.initialdir_open
        name = n = askopenfilename(title = title, initialdir = initialdir, filetypes = self.filetypes[filetype]['ext'] + self.filetypes['ALL']['ext'], multiple = multiple)
        if name and self.rem_open:
            if multiple:
                n = name[0]

            p = Path(n)
            self.initialdir_open = str(p.parent)

        return name

    def save_file(self, title, filetype = 'PDF', initialdir = None):
        if initialdir == None:
            initialdir = self.initialdir_save
        name = asksaveasfilename(title = title, initialdir = initialdir, filetypes = self.filetypes[filetype]['ext'] + self.filetypes['ALL']['ext'])
        if name and self.rem_save:
            p = Path(name)
            self.initialdir_save = str(p.parent)

        if name:
            e = False
            for ext in self.filetypes[filetype]['exts']:
                if name[-len(ext):] == ext:
                    e = True
                    break

            if not e:
                name += self.filetypes[filetype]['default']

        return name

    def open_dir(self, title, initialdir = None):
        if initialdir == None:
            initialdir = self.initialdir_dir
        name = askdirectory(title = title, initialdir = initialdir)
        if name and self.rem_dir:
            p = Path(name)
            self.initialdir_dir = str(p.parent)
        return name

    def identify(self, file):
        for kind, content in self.filetypes.items():
            if kind == 'ALL':
                return kind
            for ext in content['exts']:
                if file[-len(ext):] == ext:
                    return kind

if __name__ == '__main__':
    mwf = MainWinFiles()
    print(mwf.open_file(title = 'Ouvrir', filetype = 'CSV', multiple = True))
