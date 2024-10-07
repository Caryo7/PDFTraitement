from tkinter import *
from tkinter import ttk
from tkinter.ttk import *
from tkinter.messagebox import *

class ExportWindow:
    def __init__(self, parent):
        self.parent = parent
        self.data = {}

        self.master = Toplevel(self.parent)
        self.master.transient(self.parent)
        self.master.title('Paramètre de l\'export')
        self.master.protocol('WM_DELETE_WINDOW', self.Quitter)
        self.master.rowconfigure(0, weight = 1)
        self.master.columnconfigure(0, weight = 1)
        self.master.columnconfigure(1, weight = 1)

        self.note = ttk.Notebook(self.master)
        self.note.grid(row = 0, column = 0, padx = 5, pady = 5, sticky = 'nswe', columnspan = 2)

        frame_secu = ttk.Frame(self.note)
        frame_secu.columnconfigure(1, weight = 1)
        self.note.add(text = 'Sécurité', child = frame_secu)

        self.wids = {
            'lb_title': {'type': 'label', 'text': 'Paramètres de Sécurité'},
            'pswd': {'type': 'string', 'text': "Mot de passe utilisateur", 'variable': StringVar()},
            'pswd_confirm': {'type': 'string', 'text': "Confirmation", 'variable': StringVar()},
            'pswd_admin': {'type': 'string', 'text': "Mot de passe administrateur", 'variable': StringVar()},
            'pswd_admin_confirm': {'type': 'string', 'text': "Confirmation", 'variable': StringVar()},
            'pass': {'type': 'separator'},
            'aload_print': {'type': 'bool', 'text': "Autoriser l'impression", 'variable': IntVar(value = 4), 'on': 4},
            'aload_modify': {'type': 'bool', 'text': "Autoriser les modifications", 'variable': IntVar(value = 8), 'on': 8},
            'aload_annotation': {'type': 'bool', 'text': "Autoriser les annotations", 'variable': IntVar(value = 16+32), 'on': 16+32},
            'aload_fields': {'type': 'bool', 'text': "Autoriser l'édition des champs", 'variable': IntVar(value = 128), 'on': 128},
            'aload_extract': {'type': 'bool', 'text': "Autoriser l'extraction du contenu (texte et images)", 'variable': IntVar(value = 256), 'on': 256},
            }
        row = 0
        for name, w in self.wids.items():
            if w['type'] == 'label':
                self.wids[name]['widget'] = ttk.Label(frame_secu, text = w['text'], style = 'Title.TLabel')
                self.wids[name]['widget'].grid(row = row, column = 0, columnspan = 2, padx = 5, pady = 5, sticky = 'w')
            elif w['type'] == 'string':
                self.wids[name]['widget_label'] = ttk.Label(frame_secu, text = w['text'])
                self.wids[name]['widget_label'].grid(row = row, column = 0, padx = 5, pady = 5, sticky = 'e')
                self.wids[name]['widget'] = ttk.Entry(frame_secu, textvariable = w['variable'], show = '*')
                self.wids[name]['widget'].grid(row = row, column = 1, sticky = 'we', padx = 5, pady = 5)
            elif w['type'] == 'bool':
                self.wids[name]['widget'] = ttk.Checkbutton(frame_secu, variable = w['variable'], onvalue = w['on'], offvalue = 0, text = w['text'])
                self.wids[name]['widget'].grid(row = row, column = 1, padx = 5, pady = 5, sticky = 'w')
            elif w['type'] == 'separator':
                self.wids[name]['widget'] = ttk.Label(frame_secu, text = '')
                self.wids[name]['widget'].grid(row = row, column = 0, columnspan = 2, padx = 5, pady = 5)

            row += 1

        valider = ttk.Button(self.master, text = 'Valider', command = self.valider)
        valider.grid(row = 1, column = 0, padx = 10, pady = 10, sticky = 'we')

        cancel = ttk.Button(self.master, text = 'Annuler', command = self.Quitter)
        cancel.grid(row = 1, column = 1, padx = 10, pady = 10, sticky = 'we')

    def valider(self):
        for name, w in self.wids.items():
            if 'variable' in list(w.keys()):
                self.data[name] = w['variable'].get()

        if self.data['pswd'] != self.data['pswd_confirm'] or self.data['pswd_admin'] != self.data['pswd_admin_confirm']:
            showerror('Mot de passe', 'Les mots de passe ne correspondent pas !')
            self.wids['pswd']['widget'].focus()
            self.data = {}
            return

        self.master.destroy()

    def Quitter(self):
        self.master.destroy()

    def show(self):
        self.master.wait_window()
        return self.data

if __name__ == '__main__':
    e = ExportWindow(None)
    e.show()
