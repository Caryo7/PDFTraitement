from tkinter import *
from tkinter import ttk
from tkinter.ttk import *
from filesetting import *
from pathlib import Path
from proglister import *
from tkinter.messagebox import *
import os

class NewFunction:
    def __init__(self, master, file):
        self.parent = master
        pm = Settings()
        self.file_unit = FileTypes(pm.paths.newfnctwin)
        self.data = None

        self.master = Toplevel(master)
        self.master.transient(master)
        self.master.title('Ajout d\'une fonction')
        self.master.protocol('WM_DELETE_WINDOW', self.Quitter)
        self.master.columnconfigure(1, weight = 1)
        self.master.resizable(True, False)
        self.master.minsize(700, 100)

        self.file = StringVar(value = file)
        self.name = StringVar()

        lb_f = ttk.Label(self.master, text = 'Fichier')
        lb_f.grid(row = 0, column = 0, padx = 5, pady = 5, sticky = 'e')

        lb_prog = ttk.Label(self.master, text = 'Programme')
        lb_prog.grid(row = 2, column = 0, padx = 5, pady = 5, sticky = 'e')

        lb_de = ttk.Label(self.master, text = 'Nom de la fonction')
        lb_de.grid(row = 1, column = 0, padx = 5, pady = 5, sticky = 'e')

        ent_file = ttk.Entry(self.master, textvariable = self.file)
        ent_file.grid(row = 0, column = 1, padx = 5, pady = 5, sticky = 'we')

        self.prog = ttk.Combobox(self.master, values = ['ArrangerDuo', 'SplitFiles', 'MarginFile', 'RognerFile', 'OrganizePages', 'RemovePages', ])
        self.prog.grid(row = 2, column = 1, padx = 5, pady = 5, sticky = 'we', columnspan = 2)
        self.prog.current(0)

        ent_desc = ttk.Entry(self.master, textvariable = self.name)
        ent_desc.grid(row = 1, column = 1, padx = 5, pady = 5, sticky = 'we', columnspan = 2)

        btn = ttk.Button(self.master, text = '...', width = 3, command = self.open_fnct)
        btn.grid(row = 0, column = 2, padx = 5, pady = 5)

        button = ttk.Button(self.master, text = 'Ajouter', command = self.Valider)
        button.grid(row = 3, padx = 5, pady = 5, column = 0, columnspan = 3, sticky = 'we')

    def open_fnct(self):
        name = self.file_unit.open_file(title = 'Ajouter une fonction', filetype = 'SEA')
        if name:
            self.file.set(value = name)

    def Valider(self):
        file = self.file.get()
        cat = self.prog.get()
        self.pl = ProgLister()
        liste = self.pl.getList(cat)
        for k, l in liste.items():
            if str(os.path.abspath(l['path'])) == str(os.path.abspath(file)):
                showerror('Nouvelle Fonction', 'Ce fichier est déjà paramétré pour ce programme.\nIl est nommé : ' + str(k))
                return

        self.data = file, cat, self.name.get()
        self.master.destroy()

    def Quitter(self):
        self.master.destroy()

    def show(self):
        self.master.wait_window()
        return self.data

if __name__ == '__main__':
    from mainwin import *
    mw = MainWindow()
    mw.Generate()
