from tkinter import *
from tkinter import ttk
from tkinter.ttk import *
from tkinter.simpledialog import *
from customwidgets import *
from proglister import *
import os
import datetime

class FunctionCreate:
    FAVORI_ON  = '★'
    FAVORI_OFF = '☆'
    infos_title = {'output': 'Informations sur la sortie du programme',
                   'input': 'Informations sur les entrées du programme',
                   'infos': 'Informations générales sur le programme'}

    def __init__(self, parent, pl, cat, infos, file = None, name = None, fav = None):
        self.pl = pl
        self.cat = cat
        self.skip = False
        if file != None:
            fp = PDFSEA(file)
            self.r = fp.read()
            fp.close()
            self.name = name
            self.title = "Mise à jour de " + name
            self.fav = fav
        else:
            self.name = askstring('Nom de la fonction', "Veuillez donner un nom à votre fonction.\nCe nom pourra être changé plus tard dans l'édition de la fonction")
            if not self.name:
                self.skip = True
                return

            self.r = {'python.py': """# Nouvelle fonction crée par {0} le {1}\n
def fonction(index, length):
    return True""".format(os.getlogin(), datetime.datetime.now(datetime.UTC).strftime("%d/%m/%Y à %H:%M")),
                 'conditions.ini' : '10\\i = i\\i\n',}
            self.title = 'Nouvelle fonction : ' + self.name
            self.fav = False

        self.master = Toplevel(parent)
        self.master.transient(parent)
        self.master.title("Traitement de fonction")
        self.master.protocol('WM_DELETE_WINDOW', self.Quitter)
        self.master.columnconfigure(0, weight = 1)
        self.master.rowconfigure(1, weight = 1)

        frame_title = ttk.Frame(self.master)
        frame_title.grid(row = 0, column = 0, padx = 15, pady = 15, sticky = 'we')
        frame_title.columnconfigure(1, weight = 1)

        self.label_title = ttk.Label(frame_title, text = ' ' + self.title, style = 'Title.TLabel')
        self.label_title.grid(row = 0, column = 1, padx = 0, pady = 0, sticky = 'we')

        self.btn_fav = ttk.Button(frame_title, text = self.FAVORI_ON if self.fav else self.FAVORI_OFF, command = self.switch_fav)
        self.btn_fav.grid(row = 0, column = 0, padx = 0, pady = 0, sticky = 'we')

        self.onglets = ttk.Notebook(self.master)
        self.onglets.grid(row = 1, column = 0, padx = 15, pady = 15, sticky = 'nswe')

        self.frame_prog = ttk.Frame(self.onglets)
        self.frame_prog.columnconfigure(0, weight = 1)
        self.frame_prog.rowconfigure(0, weight = 1)

        self.prog = ProgramText(self.frame_prog, data = self.r['python.py'], width = 60, height = 15)
        self.prog.grid(row = 0, column = 0, sticky = 'nswe')
        self.prog.text.focus()

        self.frame_cond = ttk.Frame(self.onglets)
        self.frame_cond.columnconfigure(0, weight = 1)
        self.frame_cond.columnconfigure(1, weight = 1)
        self.frame_cond.columnconfigure(2, weight = 1)
        self.frame_cond.rowconfigure(0, weight = 1)

        self.scroll_cond = ttk.Scrollbar(self.frame_cond, orient = 'vertical')
        self.scroll_cond.grid(row = 0, column = 3, sticky = 'ns')
        self.conditions = ttk.Treeview(self.frame_cond, column = ('#1', '#2'), yscrollcommand = self.scroll_cond.set)
        self.scroll_cond.config(command = self.conditions.yview)
        self.conditions.grid(row = 0, column = 0, sticky = 'nswe', columnspan = 3)
        self.conditions.column('#0', width = 50)
        self.conditions.column('#1', width = 200)
        self.conditions.column('#2', width = 200)
        self.conditions.heading('#0', text = 'N°')
        self.conditions.heading('#1', text = 'A = B ?')
        self.conditions.heading('#2', text = 'Sortie')
        r = CellEditor(self.conditions, actions = {'#0': {'type': 'Entry'},
                                                   '#1': {'type': 'Entry'},
                                                   '#2': {'type': 'Entry'},
                                                   })
        self.read_file_conditions()

        btn_add = ttk.Button(self.frame_cond, text = 'Ajouter', command = self.add_line)
        btn_add.grid(row = 1, column = 0, sticky = 'nswe')
        btn_dup = ttk.Button(self.frame_cond, text = 'Dupliquer', command = self.duplicate_line)
        btn_dup.grid(row = 1, column = 1, sticky = 'nswe')
        btn_rem = ttk.Button(self.frame_cond, text = 'Supprimer', command = self.remove_line)
        btn_rem.grid(row = 1, column = 2, sticky = 'nswe')

        self.frame_info = ttk.Frame(self.onglets)
        scrollt = ttk.Scrollbar(self.frame_info, orient = 'vertical')
        self.label_infos = Text(self.frame_info, wrap = 'word', yscrollcommand = scrollt.set)
        scrollt.config(command = self.label_infos.yview)
        scrollt.grid(row = 0, column = 1, sticky = 'ns')
        self.label_infos.grid(row = 0, column = 0, sticky = 'nswe')
        for k, v in infos.items():
            if k in ('name', 'class'):
                continue
            txt = self.infos_title[k]
            deb = self.label_infos.index('end')
            row, col = deb.split('.')
            col, row = int(col), int(row)
            col += len(txt)
            if txt == None:
                txt = ''
            if v == None:
                v = ''
            self.label_infos.insert('end', '\n' + txt + '\n' + v + '\n')
            end = self.label_infos.index(str(row) + '.' + str(col))
            self.label_infos.tag_add('title', deb, end)

        self.label_infos.tag_configure('title', font = ('Consolas', 12, 'bold'))
        self.label_infos.config(stat = 'disabled')

        self.onglets.add(text = 'Conditions', child = self.frame_cond)
        self.onglets.add(text = 'Programme', child = self.frame_prog)
        self.onglets.add(text = 'Informations', child = self.frame_info)

        self.frame_name = ttk.Frame(self.master)
        self.frame_name.grid(row = 2, column = 0, padx = 10, pady = 10, sticky = 'we')
        self.frame_name.columnconfigure(1, weight = 1)

        self.name_label = ttk.Label(self.frame_name, text = 'Nom de la fonction')
        self.name_label.grid(row = 0, column = 0, sticky = 'e')

        self.new_name = StringVar(value = self.name)
        self.new_entry = ttk.Entry(self.frame_name, textvariable = self.new_name)
        self.new_entry.grid(row = 0, column = 1, sticky = 'we')

        close_button = ttk.Button(self.master, text = 'Valider', command = self.ok)
        close_button.grid(row = 3, column = 0, padx = 15, pady = 15, sticky = 'we')

    def clear_conditions(self):
        for x in self.conditions.get_children():
            self.conditions.delete(x)

    def add_line(self):
        n = 0
        for x in self.conditions.get_children():
            n = int(self.conditions.item(x)['text'])
        n = 10 * (n//10 + 1)
        self.conditions.insert('', 'end', text = str(n), values = ['i = i', 'i'])

    def remove_line(self):
        selected = self.conditions.selection()
        for x in selected:
            self.conditions.delete(x)

    def duplicate_line(self):
        n = 0
        for x in self.conditions.get_children():
            n = int(self.conditions.item(x)['text'])
        n = 10 * (n//10 + 1)
        selected = self.conditions.selection()
        for x in selected:
            item = self.conditions.item(x)
            self.conditions.insert('', 'end', text = n, values = item['values'])
            n += 10

    def read_file_conditions(self):
        self.clear_conditions()
        if 'conditions.ini' not in self.r:
            self.r['conditions.ini'] = '10\\i = i\\i\n'

        for line in self.r['conditions.ini'].split('\n'):
            if not line:
                continue

            nb, equation, output = line.split('\\')
            self.conditions.insert('', 'end', text = nb, values = [equation, output])

    def generate_text_condition(self):
        txt = []
        for x in self.conditions.get_children():
            item = self.conditions.item(x)
            nb = item['text']
            equation, output = item['values']
            txt.append(str(nb) + '\\' + str(equation) + '\\' + str(output))

        self.r['conditions.ini'] = '\n'.join(txt)

    def switch_fav(self):
        self.fav = not self.fav
        self.btn_fav.config(text = self.FAVORI_ON if self.fav else self.FAVORI_OFF)

    def get_text(self):
        text = self.prog.get('0.0', 'end')
        if len(text) >= 1:
            while text[-1] == '\n':
                text = text[:-1]

        self.generate_text_condition()
        return {'python.py': text, 'conditions.ini': self.r['conditions.ini']}

    def ok(self):
        self.pl.update(self.name, self.cat, self.get_text(), self.new_name.get(), 1 if self.fav else 0)
        self.master.destroy()

    def Generate(self):
        if not self.skip:
            self.master.wait_window()

    def Quitter(self):
        self.master.destroy()

if __name__ == '__main__':
    from mainwin import *
    mw = MainWindow()
    mw.Generate()
