from tkinter import *
from tkinter import ttk
from tkinter.ttk import *
from tkinter.messagebox import *
import os

from pagecount import *
from customwidgets import *

class PrintSettings:
    def __init__(self, parent, len_pages, pages_selected):
        self.parent = parent
        self.len_pages = len_pages
        self.pages_selected = pages_selected

        self.master = Toplevel(parent)
        self.master.transient(parent)
        self.TITLE = 'Imprimer'
        self.master.title(self.TITLE)
        self.master.protocol('WM_DELETE_WINDOW', self.Quitter)
        self.master.resizable(True, False)
        self.master.columnconfigure(0, weight = 1)
        self.master.columnconfigure(1, weight = 1)

        ptnm = ttk.LabelFrame(self.master, text = 'Imprimante')
        ptnm.grid(row = 0, column = 0, padx = 10, pady = 10, sticky = 'nswe', columnspan = 2)
        ptnm.columnconfigure(1, weight = 1)

        nom_label = ttk.Label(ptnm, text = 'Nom de l\'imprimante')
        nom_label.grid(row = 0, column = 0, padx = 5, pady = 5, sticky = 'e')

        self.printer = ttk.Combobox(ptnm, values = ['Canon TR4600 series'])
        self.printer.grid(row = 0, column = 1, padx = 5, pady = 5, sticky = 'we')
        self.printer.set('Canon TR4600 series')

        settings = ttk.Button(ptnm, text = 'Paramètres', command = self.open_settings)
        settings.grid(row = 0, column = 2, padx = 5, pady = 5, sticky = 'nswe')

        kind_label = ttk.Label(ptnm, text = 'Type d\'imprimante')
        kind_label.grid(row = 1, column = 0, padx = 5, pady = 5, sticky = 'e')

        self.kind_of_printer = StringVar()
        kind_entry = ttk.Label(ptnm, textvariable = self.kind_of_printer)
        kind_entry.grid(row = 1, column = 1, padx = 5, pady = 5, sticky = 'w')

        copies_label = ttk.Label(ptnm, text = 'Nombre de copies')
        copies_label.grid(row = 2, column = 0, padx = 5, pady = 5, sticky = 'e')

        self.nb_copies = ttk.Spinbox(ptnm, from_ = 1, to = 999, command = self.update)
        self.nb_copies.grid(row = 2, column = 1, padx = 5, pady = 5, sticky = 'we')
        self.nb_copies.set(1)
        self.nb_copies.bind('<KeyRelease>', self.update)

        area = ttk.LabelFrame(self.master, text = 'Zone d\'impression')
        area.grid(row = 1, column = 0, padx = 10, pady = 10, sticky = 'nswe', columnspan = 2)
        area.columnconfigure(1, weight = 1)

        self.default = StringVar(value = 'all')
        all_pages = ttk.Radiobutton(area, variable = self.default, value = 'all', text = 'Toutes les pages', command = self.update)
        all_pages.grid(row = 0, column = 0, padx = 5, pady = 5, sticky = 'w')
        sel_pages = ttk.Radiobutton(area, variable = self.default, value = 'selected', text = 'Pages séléctionnées', command = self.update)
        sel_pages.grid(row = 1, column = 0, padx = 5, pady = 5, sticky = 'w')
        cus_pages = ttk.Radiobutton(area, variable = self.default, value = 'custom', text = 'Pages Personnalisées', command = self.update)
        cus_pages.grid(row = 2, column = 0, padx = 5, pady = 5, sticky = 'w')

        self.custom = StringVar()
        cus_entry = ttk.Entry(area, textvariable = self.custom)
        cus_entry.grid(row = 2, column = 1, padx = 5, pady = 5, sticky = 'we')
        cus_entry.bind('<KeyPress>', self.select_perso)
        cus_entry.bind('<KeyRelease>', self.update)
        ToolTip(cus_entry, 'Entrez des numéros de pages et des intervalles. Exemple: 1; 2; 3; 4 - 12. Vous pouvez mettre des ";" ou des ",".\nPour mettre plusieurs fois la même page, écrivez par exemple 1; 1; 1.')

        keep_label = ttk.Label(area, text = 'Conserver')
        keep_label.grid(row = 3, column = 0, padx = 5, pady = 5, sticky = 'e')

        self.under_sets = ['Toutes les pages', 'Les pages paires', 'Les pages impaires']
        self.under_set = ttk.Combobox(area, values = self.under_sets)
        self.under_set.grid(row = 3, column = 1, padx = 5, pady = 5, sticky = 'we')
        self.under_set.current(0)
        self.under_set.bind('<<ComboboxSelected>>', self.update)

        self.invert = IntVar(value = 0)
        inv_order = ttk.Checkbutton(area, text = 'Inverser l\'ordre', onvalue = 1, offvalue = 0, variable = self.invert)
        inv_order.grid(row = 3, column = 2, padx = 5, pady = 5)

        infos = ttk.LabelFrame(self.master, text = 'Informations')
        infos.grid(row = 2, column = 0, padx = 10, pady = 10, sticky = 'nswe', columnspan = 2)

        self.nb_feuille_total = IntVar()
        self.nb_feuille_task = IntVar()

        label_feuille = ttk.Label(infos, text = 'Nombre de feuilles total')
        label_feuille.grid(row = 0, column = 0, padx = 5, pady = 5, sticky = 'e')
        entry_feuille = ttk.Label(infos, textvariable = self.nb_feuille_total)
        entry_feuille.grid(row = 0, column = 1, padx = 5, pady = 5, sticky = 'w')
        label_task = ttk.Label(infos, text = 'Nombre de feuilles par copie')
        label_task.grid(row = 1, column = 0, padx = 5, pady = 5, sticky = 'e')
        entry_task = ttk.Label(infos, textvariable = self.nb_feuille_task)
        entry_task.grid(row = 1, column = 1, padx = 5, pady = 5, sticky = 'w')

        lancer = ttk.Button(self.master, text = 'Imprimer', command = self.launch)
        lancer.grid(row = 3, column = 0, padx = 10, pady = 10, sticky = 'nswe')

        annuler = ttk.Button(self.master, text = 'Annuler', command = self.master.destroy)
        annuler.grid(row = 3, column = 1, padx = 10, pady = 10, sticky = 'nswe')

        self.update()

    def launch(self):
        self.master.destroy()

    def select_perso(self, evt=None):
        for k in ['control', 'shift', 'alt', 'iso', 'tab']:
            if k in evt.keysym.lower():
                return
        self.default.set(value = 'custom')

    def update(self, evt = None):
        try:
            nb = int(self.nb_copies.get())
            mode = self.default.get()
            if mode == 'all':
                pages = self.len_pages
            elif mode == 'selected':
                pages = len(self.pages_selected)
            elif mode == 'custom':
                p = getPagesNumber(self.custom.get(), getCompleteList = True)
                pages = len(p)

            _us = self.under_sets.index(self.under_set.get())
            if _us == 0:
                us = 1
            else:
                us = 0.5

            n = pages * us
            if n > int(n):
                n = int(n) + 1
            else:
                n = int(n)

            self.nb_feuille_task.set(n)
            self.nb_feuille_total.set(n * nb)
        except:
            pass

    def open_settings(self):
        printer = self.printer.get()
        if not printer:
            showerror('Imprimante', 'Vous devez séléctionner une imprimante à configurer !')
            return

        cmd = 'rundll32 printui.dll,PrintUIEntry /e /n"{}"'.format(printer)
        os.popen(cmd)

    def Quitter(self):
        self.master.destroy()

    def show(self):
        self.master.wait_window()

if __name__ == '__main__':
    root = Tk()
    ps = PrintSettings(root, 24, [0, 1, 5, 10, 3, 7])
    ps.show()
    root.mainloop()
