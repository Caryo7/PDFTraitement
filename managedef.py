from tkinter import *
from tkinter import ttk
from tkinter.ttk import *
from tkinter.messagebox import *
from customwidgets import *
from userform import *
import os, humanize
import datetime as dt

class EditProgram:
    def __init__(self, parent, name, content):
        self.old_content = content
        self.data = None

        self.master = Toplevel(parent)
        self.master.protocol('WM_DELETE_WINDOW', lambda: None)
        self.master.title('Edition - ' + name)
        self.master.columnconfigure(0, weight = 1)
        self.master.columnconfigure(1, weight = 1)
        self.master.rowconfigure(0, weight = 1)

        self.text = ProgramText(self.master, data = content, lang = 'basic')
        self.text.grid(row = 0, column = 0, padx = 5, pady = 5, sticky = 'nswe', columnspan = 2)

        ok = ttk.Button(self.master, text = 'Valider', command = self.ok)
        ok.grid(row = 1, column = 0, padx = 5, pady = 5, sticky = 'we')

        can = ttk.Button(self.master, text = 'Annuler', command = self.cancel)
        can.grid(row = 1, column = 1, padx = 5, pady = 5, sticky = 'we')

    def ok(self):
        self.data = self.text.get('0.0', 'end')
        self.master.destroy()

    def cancel(self):
        self.data = self.old_content
        self.master.destroy()

    def show(self):
        self.master.wait_window()
        return self.data

class Manager:
    def __init__(self, parent, onglet, programs, userforms):
        self.programs = self.old_programs = programs
        self.userforms = self.old_userforms = userforms
        self.old_title = None

        self.master = Toplevel(parent)
        self.master.transient(parent)
        self.master.protocol('WM_DELETE_WINDOW', lambda: None)
        self.master.title('Gérer les définitions')
        self.master.columnconfigure(0, weight = 1)
        self.master.columnconfigure(1, weight = 1)
        self.master.rowconfigure(0, weight = 1)

        self.note = ttk.Notebook(self.master)
        self.note.grid(row = 0, column = 0, padx = 5, pady = 5, sticky = 'nswe', columnspan = 2)

        self.uf = ttk.Frame(self.note)
        self.uf.columnconfigure(0, weight = 1)
        self.uf.rowconfigure(0, weight = 1)
        self.note.add(text = 'UserForms', child = self.uf)

        self.prog = ttk.Frame(self.note)
        self.prog.columnconfigure(0, weight = 1)
        self.prog.rowconfigure(0, weight = 1)
        self.note.add(text = 'Programmes', child = self.prog)

        scrolluf = ttk.Scrollbar(self.uf, orient = 'vertical')
        scrolluf.grid(row = 0, column = 1, sticky = 'ns')
        self.tree_uf = ttk.Treeview(self.uf, yscrollcommand = scrolluf.set, columns = ('#1', '#2'), selectmode = 'browse')
        self.tree_uf.grid(row = 0, column = 0, sticky = 'nswe')
        scrolluf.config(command = self.tree_uf.yview)
        self.tree_uf.heading('#0', text = 'Nom')
        self.tree_uf.heading('#1', text = 'Taille')
        self.tree_uf.heading('#2', text = 'Création')
        #self.tree_uf.bind('<Double-Button-1>', self.select_uf)
        self.tree_uf.bind('<Button-3>', self.right_uf)
        user_editor = CellEditor(self.tree_uf, actions = {'#0': {'type': 'Entry'}}, command = lambda : self.update_names('uf'), beg_cmd = lambda: self.store_name('uf'))

        scrollpr = ttk.Scrollbar(self.prog, orient = 'vertical')
        scrollpr.grid(row = 0, column = 1, sticky = 'ns')
        self.tree_pr = ttk.Treeview(self.prog, yscrollcommand = scrollpr.set, columns = ('#1', '#2'), selectmode = 'browse')
        self.tree_pr.grid(row = 0, column = 0, sticky = 'nswe')
        scrollpr.config(command = self.tree_pr.yview)
        self.tree_pr.heading('#0', text = 'Nom')
        self.tree_pr.heading('#1', text = 'Taille')
        self.tree_pr.heading('#2', text = 'Création')
        #self.tree_pr.bind('<Double-Button-1>', self.select_pr)
        self.tree_pr.bind('<Button-3>', self.right_pr)
        prog_editor = CellEditor(self.tree_pr, actions = {'#0': {'type': 'Entry'}}, command = lambda : self.update_names('pr'), beg_cmd = lambda: self.store_name('pr'))

        new_pr = ttk.Button(self.prog, text = 'Nouveau programme', command = self.new_prog)
        new_pr.grid(row = 1, column = 0, padx = 5, pady = 5, sticky = 'we')

        self.note.select(onglet)

        okbtn = ttk.Button(self.master, text = 'Valider', command = self.ok)
        okbtn.grid(row = 1, column = 0, padx = 5, pady = 5, sticky = 'we')
        clbtn = ttk.Button(self.master, text = 'Annuler', command = self.cancel)
        clbtn.grid(row = 1, column = 1, padx = 5, pady = 5, sticky = 'we')

        self.update()

    def store_name(self, mode):
        if mode == 'pr':
            self.old_title = self.tree_pr.item(self.tree_pr.selection())['text']
        elif mode == 'uf':
            self.old_title = self.tree_uf.item(self.tree_uf.selection())['text']

    def update_names(self, mode):
        if mode == 'pr':
            data = self.programs[self.old_title]
            del self.programs[self.old_title]
        elif mode == 'uf':
            data = self.userforms[self.old_title]
            del self.userforms[self.old_title]
        if mode == 'pr':
            new_iid = self.tree_pr.item(self.tree_pr.selection())['text']
        elif mode == 'uf':
            new_iid = self.tree_uf.item(self.tree_uf.selection())['text']
        if mode == 'pr':
            self.programs[new_iid] = data
        elif mode == 'uf':
            self.userforms[new_iid] = data

        self.update()

    def update(self, evt = None):
        for x in self.tree_uf.get_children():
            self.tree_uf.delete(x)
        for x in self.tree_pr.get_children():
            self.tree_pr.delete(x)

        for name, content in self.programs.items():
            self.tree_pr.insert('', 'end', text = name, values = [humanize.naturalsize(len(content)), ''])
        for name, content in self.userforms.items():
            self.tree_uf.insert('', 'end', text = name, values = [humanize.naturalsize(len(content)), ''])


    def right_uf(self, evt):
        popup = Menu(self.tree_uf, tearoff = 0)
        popup.add_command(label = 'Modifier', command = self.select_uf)
        popup.add_command(label = 'Supprimer', command = self.del_uf)
        popup.add_command(label = 'Renommer', command = None)
        popup.tk_popup(evt.x_root, evt.y_root)

    def right_pr(self, evt):
        popup = Menu(self.tree_pr, tearoff = 0)
        popup.add_command(label = 'Modifier', command = self.select_pr)
        popup.add_command(label = 'Supprimer', command = self.del_pr)
        popup.add_command(label = 'Renommer', command = None)
        popup.tk_popup(evt.x_root, evt.y_root)


    def new_prog(self, evt = None):
        e = EditProgram(self.master, 'untitled.prog', '')
        content = e.show()
        self.programs['untitled.prog'] = content
        self.update()

    def new_usfo(self, evt = None):
        e = UserFormGenerator(self.master, 'untitled.uf', '')
        content = e.show()
        self.userforms['untitled.uf'] = content
        self.update()


    def del_pr(self):
        for x in self.tree_pr.selection():
            del self.programs[self.tree_pr.item(x)['text']]
        self.update()

    def del_uf(self):
        for x in self.tree_uf.selection():
            del self.userforms[self.tree_uf.item(x)['text']]
        self.update()


    def select_pr(self, evt = None):
        selection = self.tree_pr.selection()
        for s in selection:
            item = self.tree_pr.item(s)
            e = EditProgram(self.master, item['text'], self.programs[item['text']])
            content = e.show()
            self.programs[item['text']] = content
            self.update()

    def select_uf(self, evt = None):
        selection = self.tree_uf.selection()
        for s in selection:
            item = self.tree_uf.item(s)
            e = UserFormGenerator(self.master, item['text'], self.userforms[item['text']])
            content = e.show()
            self.userforms[item['text']] = content
            self.update()


    def ok(self):
        self.master.destroy()

    def cancel(self):
        self.programs = self.old_programs
        self.userforms = self.old_userforms
        self.master.destroy()

    def Generate(self):
        self.master.wait_window()
        return self.programs, self.userforms

if __name__ == '__main__':
    from project import *
    root = Tk()
    f = PDFPRO('test1.pdfpro')
    m = Manager(root, 0, f.programs, f.userforms)
    f.close()
    m.Generate()
    root.mainloop()
