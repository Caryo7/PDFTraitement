from tkinter import *
from tkinter import ttk
from tkinter.ttk import *
from proglister import *
from fnctwin import *
from tkinter.messagebox import *
from winlocker import *

class ProgWindow:
    FAVORI_ON  = '★'
    FAVORI_OFF = '☆'

    def __init__(self, parent, prog_name, title, infos):
        self.pl = ProgLister()
        self.locker = WinLocker()
        self.prog_name = prog_name
        self.infos = infos
        self.pm = Settings()
        self.pm = self.pm.prog

        self.master = Toplevel(parent)
        self.master.transient(parent)
        self.master.title('Paramètre du programme')
        self.master.protocol('WM_DELETE_WINDOW', self.Quitter)
        self.master.columnconfigure(0, weight = 1)
        self.master.rowconfigure(2, weight = 1)

        self.label_title = ttk.Label(self.master, text = 'Programme ' + title, style = 'Title.TLabel')
        self.label_title.grid(row = 0, column = 0, padx = 5, pady = 5, sticky = 'we')

        self.label_config = ttk.Label(self.master, text = 'Fonctions disponibles')
        self.label_config.grid(row = 1, column = 0, padx = 5, pady = 5, sticky = 'we')

        frame = ttk.Frame(self.master)
        frame.grid(row = 2, column = 0, padx = 5, pady = 5, sticky = 'nswe')
        frame.columnconfigure(0, weight = 1)
        frame.rowconfigure(0, weight = 1)
        self.scroll = ttk.Scrollbar(frame, orient = 'vertical')
        self.scroll.grid(row = 0, column = 1, sticky = 'ns')
        self.list_fnct = ttk.Treeview(frame, columns = ('#1', '#2', '#3'), yscrollcommand = self.scroll.set, selectmode = 'browse')
        self.list_fnct.grid(row = 0, column = 0, sticky = 'nswe')
        self.scroll.config(command = self.list_fnct.yview)
        self.list_fnct.heading('#0', text = 'Nom de la fonction')
        self.list_fnct.heading('#1', text = 'Type de fonction')
        self.list_fnct.heading('#2', text = 'Programme')
        self.list_fnct.heading('#3', text = self.FAVORI_OFF)
        self.list_fnct.column('#0', width = 200)
        self.list_fnct.column('#1', width = 115)
        self.list_fnct.column('#2', width = 150)
        self.list_fnct.column('#3', width = 30)
        #r = CellEditor(self.list_fnct, {'#3': {'type': 'switch', 'on': self.FAVORI_ON, 'off': self.FAVORI_OFF}})

        self.item_selected = None

        self.frame_button = ttk.Frame(self.master)
        self.frame_button.grid(row = 3, column = 0, sticky = 'nswe', padx = 5, pady = 5)
        for i in range(4): self.frame_button.columnconfigure(i, weight = 1)

        self.add_button = ttk.Button(self.frame_button, text = 'Créer une nouvelle fonction', command = self.new_fnct)
        self.add_button.grid(row = 0, column = 0, padx = 5, pady = 5, sticky = 'we')

        self.del_button = ttk.Button(self.frame_button, text = 'Modifier la fonction', command = self.change_fnct)
        self.del_button.grid(row = 0, column = 1, padx = 5, pady = 5, sticky = 'we')

        self.copy_button = ttk.Button(self.frame_button, text = 'Dupliquer', command = self.duplicate_fnct)
        self.copy_button.grid(row = 0, column = 2, padx = 5, pady = 5, sticky = 'we')

        self.del_button = ttk.Button(self.frame_button, text = 'Supprimer la fonction', command = self.del_fnct)
        self.del_button.grid(row = 0, column = 3, padx = 5, pady = 5, sticky = 'we')

        self.finish_button = ttk.Button(self.master, text = 'Valider', command = self.ok)
        self.finish_button.grid(row = 4, column = 0, padx = 5, pady = 5, sticky = 'we')

        self.insertPrograms()

    def new_fnct(self):
        if self.locker.open_function(self.new_fnct): return

        fnct = FunctionCreate(self.master, self.pl, self.prog_name, self.infos)
        fnct.Generate()
        self.insertPrograms()
        self.locker.close_function(self.new_fnct)

    def duplicate_fnct(self):
        if self.locker.open_function(self.duplicate_fnct): return

        item = self.list_fnct.selection()
        if len(item) != 0:
            name = self.list_fnct.item(item[0])['text']
        else:
            self.locker.close_function(self.duplicate_fnct)
            return

        self.pl.duplicate(self.prog_name, name) 

        self.insertPrograms()
        self.locker.close_function(self.duplicate_fnct)

    def change_fnct(self):
        if self.locker.open_function(self.change_fnct): return

        item = self.list_fnct.selection()
        if len(item) != 0:
            item = self.list_fnct.item(item[0])
            name = item['text']
            file = self.liste[name]['path']
            aload = item['values'][0]
            fav = '1' if item['values'][2] == self.FAVORI_ON else 0
        else:
            self.locker.close_function(self.change_fnct)
            return

        if aload.lower() == 'par défaut' and self.pm.default['aload_change'] == '0':
            showerror('Fonction', "Cette fonction est une fonction par défaut. Elle ne peut pas être modifiée par l'utilisateur !\nCependant, vous pouvez la copier puis modifier la copie, ou aller dans les paramètres : menu edition -> Préférences -> Programme")
            self.locker.close_function(self.change_fnct)
            return
        elif aload.lower() == 'personnel' and self.pm.perso['aload_change'] == '0':
            showerror('Fonction', "Cette fonction ne peut pas être modifiée par l'utilisateur !\nCependant, vous pouvez la copier puis modifier la copie, ou aller dans les paramètres : menu edition -> Préférences -> Programme")
            self.locker.close_function(self.change_fnct)
            return

        fnct = FunctionCreate(self.master, self.pl, self.prog_name, self.infos, file, name, fav)
        fnct.Generate()
        self.insertPrograms()
        self.locker.close_function(self.change_fnct)

    def del_fnct(self):
        if self.locker.open_function(self.del_fnct): return

        item = self.list_fnct.selection()
        if len(item) != 0:
            name = self.list_fnct.item(item[0])['text']
            aload = self.list_fnct.item(item[0])['values'][0]
        else:
            self.locker.close_function(self.del_fnct)
            return

        if aload.lower() == 'par défaut' and self.pm.default['aload_del'] == '0':
            showerror('Fonction', "Cette fonction est une fonction par défaut. Elle ne peut pas être supprimée par l'utilisateur !\nCependant, vous pouvez la copier puis modifier la copie, ou aller dans les paramètres : menu edition -> Préférences -> Programme")
            self.locker.close_function(self.del_fnct)
            return
        elif aload.lower() == 'personnel' and self.pm.perso['aload_del'] == '0':
            showerror('Fonction', "Cette fonction ne peut pas être supprimée par l'utilisateur !\nCependant, vous pouvez la copier puis modifier la copie, ou aller dans les paramètres : menu edition -> Préférences -> Programme")
            self.locker.close_function(self.del_fnct)
            return

        self.pl.delete(self.prog_name, name)
        self.insertPrograms()
        self.locker.close_function(self.del_fnct)

    def clearPrograms(self):
        for x in self.list_fnct.get_children():
            self.list_fnct.delete(x)

    def insertPrograms(self):
        self.clearPrograms()
        self.liste = self.pl.getList(self.prog_name)
        for name, item in self.liste.items():
            self.list_fnct.insert('', 'end', text = name, values = [item['type'], item['file'], self.FAVORI_ON if item['favori'] else self.FAVORI_OFF])

    def ok(self):
        iid = self.list_fnct.selection()
        if len(iid) == 1:
            item = self.list_fnct.item(iid[0])['text']
            self.item_selected = self.liste[item]['path']
            self.master.destroy()
        else:
            showerror('Séléction', "Vous devez impérativement séléctionner un programme à utiliser !")

    def Quitter(self):
        self.master.destroy()

    def Generate(self):
        self.master.wait_window()
        return self.item_selected

if __name__ == '__main__':
    from mainwin import *
    mw = MainWindow()
    mw.Generate()
