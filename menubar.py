from tkinter import *
from config import *
from project import *
from aide import *
from searchwin import *
from recentfiles import *
from managedef import *

class IOMenu:
    def load_menus(self):
        self.barremenu = [
            {'type': 'cascade', 'label': '_Fichier', 'key': None, 'image': self.Imager.none.menu},
            {'type': 'command', 'label': '_Nouveau Projet', 'key': '<Control-n>', 'command': lambda *_: None, 'image': None},
            {'type': 'command', 'label': 'Nouvelle Fonction', 'key': None, 'command': lambda *_: None, 'image': None},
            {'type': 'command', 'label': 'Nouveau Programme', 'key': None, 'command': lambda *_: None, 'image': None},
            {'type': 'separator'},
            {'type': 'command', 'label': 'Ouvrir un projet', 'key': '<Control-o>', 'command': lambda *_: self.open_project(), 'image': self.Imager.Open.menu},
            {'type': 'recent',  'label': 'Ouvrir un fichier _récent', 'image': self.Imager.Open.menu},
            {'type': 'command', 'label': 'Ajouter une fonction', 'key': None, 'command': lambda *_: self.add_function(), 'image': self.Imager.Add.menu},
            {'type': 'command', 'label': 'Importer un fichier', 'key': '<Control-i>', 'command': lambda *_: self.open_PDFfile(), 'image': self.Imager.Import.menu},
            {'type': 'command', 'label': 'Importer une image', 'key': '<Control-e>', 'command': lambda *_: self.import_images(), 'image': self.Imager.Import.menu},
            {'type': 'command', 'label': 'Importer un projet', 'key': '<Control-r>', 'command': lambda *_: self.import_project(), 'image': self.Imager.Import.menu},
            {'type': 'command', 'label': 'Importer une liste de fichiers', 'key': '<Control-l>', 'command': lambda *_: self.open_CSVfile(), 'image': self.Imager.Import.menu},
            {'type': 'separator'},
            {'type': 'command', 'label': 'Enregistrer le projet', 'key': '<Control-s>', 'command': lambda *_: self.save_project(), 'image': self.Imager.Save.menu},
            {'type': 'command', 'label': 'Enregistrer le projet sous', 'key': '<Control-S>', 'command': lambda *_: self.saveas_project(), 'image': self.Imager.SaveAs.menu},
            {'type': 'command', 'label': 'Enregistrer une copie du projet sous', 'key': '<Control-Alt-s>', 'command': lambda *_: self.saveascopy_project(), 'image': self.Imager.SaveCopyAs.menu},
            {'type': 'separator'},
            {'type': 'command', 'label': 'Exporter la liste', 'key': '<Alt-l>', 'command': lambda *_: self.export_list(), 'image': self.Imager.Export.menu},
            {'type': 'command', 'label': 'Exporter la fusion', 'key': '<Alt-f>', 'command': lambda *_: self.export_fusion(), 'image': self.Imager.Export.menu},
            {'type': 'command', 'label': 'Exporter les images de la fusion', 'key': '<Alt-i>', 'command': lambda *_: self.export_images(), 'image': self.Imager.Export.menu},
            {'type': 'separator'},
            {'type': 'command', 'label': 'Imprimer', 'key': '<Control-p>', 'command': lambda *_: self.print_files(), 'image': self.Imager.Print.menu},
            {'type': 'separator'},
            {'type': 'command', 'label': 'Fermer le projet', 'key': '<Control-w>', 'command': lambda *_: self.close_project(), 'image': self.Imager.Close.menu},
            {'type': 'command', 'label': 'Fermer tous les fichiers ouverts', 'key': '<Control-q>', 'command': lambda *_: self.clear_files(), 'image': self.Imager.Close.menu},
            {'type': 'command', 'label': 'Fermer le logiciel', 'key': '<Alt-F4>', 'command': lambda *_: self.Quitter(), 'image': self.Imager.Exit.menu},
            {'type': 'end'},

            {'type': 'cascade', 'label': '_Edition', 'key': None, 'image': self.Imager.none.menu},
            {'type': 'command', 'label': 'Annuler', 'key': '<Control-z>', 'command': lambda *_: None, 'image': self.Imager.Undo.menu},
            {'type': 'command', 'label': 'Rétablir', 'key': '<Control-y>', 'command': lambda *_: None, 'image': self.Imager.Redo.menu},
            {'type': 'command', 'label': 'Historique', 'key': '<Control-h>', 'command': lambda *_: None, 'image': None},
            {'type': 'separator'},
            {'type': 'command', 'label': 'Séléctionner toutes les pages', 'key': '<Control-a>', 'command': lambda *_: self.selectall(None, True), 'image': None},
            {'type': 'command', 'label': 'Tout déséléctionner', 'key': '<Control-A>', 'command': lambda *_: self.selectall(None, False), 'image': None},
            {'type': 'separator'},
            {'type': 'command', 'label': 'Sépararer le document à la page', 'key': '<Alt-s>', 'command': lambda *_: self.split_page(), 'image': None},
            {'type': 'separator'},
            {'type': 'command', 'label': 'Rechercher dans les pages', 'key': '<Control-f>', 'command': lambda *_: self.search(), 'image': self.Imager.Search.menu},
            {'type': 'separator'},
            {'type': 'command', 'label': 'Préférences', 'key': '<F12>', 'command': lambda *_: self.configure(), 'image': None},
            {'type': 'end'},

            {'type': 'cascade', 'label': '_Vue', 'key': None, 'image': self.Imager.none.menu},
            {'type': 'command', 'label': 'Basculer la vue', 'key': '<Control-Tab>', 'command': lambda *_: self.onglets.select(2 - self.onglets.index(self.onglets.select())), 'image': None},
            {'type': 'separator'},
            {'type': 'command', 'label': 'Afficher l\'arborescence des fichiers', 'key': None, 'command': lambda *_: self.onglets.select(0), 'image': None},
            {'type': 'command', 'label': 'Afficher la liste des pages', 'key': None, 'command': lambda *_: self.onglets.select(1), 'image': None},
            {'type': 'command', 'label': 'Afficher l\'arborescence d\'insertion', 'key': None, 'command': lambda *_: self.onglets.select(2), 'image': None},
            {'type': 'end'},

            {'type': 'cascade', 'label': '_Projet', 'key': None, 'image': self.Imager.none.menu},

            {'type': 'cascade', 'label': '_Définitions', 'key': None, 'image': self.Imager.none.menu},
            {'type': 'command', 'label': 'Ajouter une interface', 'key': None, 'image': None, 'command': lambda *_: self.new_userForm()},
            {'type': 'command', 'label': 'Gérer les interfaces', 'key': None, 'image': None, 'command': lambda *_: self.config_def(mode = 0)},
            {'type': 'command', 'label': 'Ajouter un script', 'key': None, 'image': None, 'command': lambda *_: None},
            {'type': 'command', 'label': 'Gérer les scripts', 'key': None, 'image': None, 'command': lambda *_: self.config_def(mode = 1)},
            {'type': 'end'},

            {'type': 'cascade', 'label': '_Aide', 'key': None, 'image': self.Imager.none.menu},
            {'type': 'command', 'label': 'A propos', 'key': None, 'command': lambda *_: self.about(), 'image': self.Imager.Help.menu},
            {'type': 'separator'},
            {'type': 'command', 'label': 'Documentation', 'key': '<F1>', 'command': lambda *_: self.aide_doc('all'), 'image': self.Imager.Help.menu},
            {'type': 'command', 'label': 'Documentation des programmes', 'key': None, 'command': lambda *_: self.aide_doc('./docs/02- programmes.html'), 'image': self.Imager.Help.menu},
            {'type': 'command', 'label': 'Documentation sur l\'interface', 'key': None, 'image': self.Imager.Help.menu, 'command': lambda *_: self.aide_doc('./docs/03- guilang.html')},
            {'type': 'end'},
            #{'type': 'command', 'label': '', 'key': None, 'image': self.Imager.none.menu, 'command': lambda *_: None},
            ]

        self.right_click_files = [
            {'type': 'command', 'label': 'Monter', 'key': '<Up>', 'image': self.Imager.Up.menu, 'command': lambda *_: self.move('up')},
            {'type': 'command', 'label': 'Descendre', 'key': '<Down>', 'image': self.Imager.Down.menu, 'command': lambda *_: self.move('down')},
            {'type': 'command', 'label': 'Trier', 'key': None, 'image': self.Imager.none.menu, 'command': lambda *_: self.sort_files()},
            {'type': 'separator'},
            {'type': 'command', 'label': 'Ouvrir un projet', 'key': '<Control-o>', 'command': lambda *_: self.open_project(), 'image': self.Imager.Open.menu},
            {'type': 'command', 'label': 'Importer un fichier', 'key': '<Control-i>', 'command': lambda *_: self.open_PDFfile(), 'image': self.Imager.Import.menu},
            {'type': 'command', 'label': 'Importer une image', 'key': '<Control-e>', 'command': lambda *_: self.import_images(), 'image': self.Imager.Import.menu},
            {'type': 'command', 'label': 'Importer un projet', 'key': '<Control-r>', 'command': lambda *_: self.import_project(), 'image': self.Imager.Import.menu},
            {'type': 'command', 'label': 'Importer une liste de fichiers', 'key': '<Control-l>', 'command': lambda *_: self.open_CSVfile(), 'image': self.Imager.Import.menu},
            {'type': 'separator'},
            {'type': 'command', 'label': 'Ouvrir les fichiers', 'key': '<Alt-o>', 'image': self.Imager.Open.menu, 'command': lambda *_: self.open_file()},
            {'type': 'command', 'label': 'Recharger les fichiers', 'key': '<F5>', 'image': self.Imager.Upgrade.menu, 'command': lambda *_: self.reload_file()},
            {'type': 'command', 'label': 'Retirer les fichiers', 'key': '<Delete>', 'image': self.Imager.Close.menu, 'command': lambda *_: self.delete_file()},
            {'type': 'separator'},
            {'type': 'command', 'label': 'Séparer le fichier', 'key': None, 'image': self.Imager.none.menu, 'command': lambda *_: self.split_page()},
            {'type': 'command', 'label': 'Dupliquer les fichiers', 'key': '<Control-d>', 'image': self.Imager.Copy.menu, 'command': lambda *_: self.duplicate_file()},
            {'type': 'command', 'label': 'Renommer le fichier', 'key': '<F2>', 'image': self.Imager.none.menu, 'command': lambda *_: self.rename_file()},
            {'type': 'separator'},
            {'type': 'command', 'label': 'Propriétés', 'key': 'i', 'image': self.Imager.none.menu, 'command': lambda *_: self.show_infos()},
            ]

class MenuBar(IOMenu):
    def test_number(self, string):
        for char in string:
            if char.isdigit():
                return False

        return True

    def name_key(self, event):
        if event == None:
            return event

        event = event.replace('<', '')
        event = event.replace('>', '')
        event = event.replace('-', ' + ')
        event = event.replace('Control', 'Ctrl')
        event = event.replace('Tab', 'tab')
        bloc = event.split(' + ')
        if 'Ctrl' in event or 'Alt' in event:
            letter = bloc[-1]
            if letter != letter.lower() and self.test_number(letter): # On est en majuscule
                bloc.insert(len(bloc)-1, 'Shift')

        for i in range(len(bloc)):
            bloc[i] = bloc[i].capitalize()
        key = ' + '.join(bloc)
        return key

    def clear_menuprojet(self):
        self.menu_projet.delete('0', 'end')

    def draw_menu(self):
        self.menubar = Menu(self.master)
        self.master['menu'] = self.menubar
        self.menu_projet = None
        mp = False

        menu_win = [self.menubar]
        for menu in self.barremenu:
            if menu['type'] == 'cascade' and menu['label'] == '_Projet':
                mp = True
            elif menu['type'] == 'cascade':
                mp = False

            if not mp:
                if menu['type'] == 'cascade':
                    if '_' in menu['label']:
                        ul = menu['label'].index('_')
                        menu['label'] = menu['label'].replace('_', '')
                    else:
                        ul = None

                    menu_win.append(Menu(menu_win[-1], tearoff = 0))
                    menu_win[-2].add_cascade(label = menu['label'], menu = menu_win[-1], accelerator = menu['key'], image = menu['image'], compound = 'left', underline = ul)

                elif menu['type'] == 'command':
                    if '_' in menu['label']:
                        ul = menu['label'].index('_')
                        menu['label'] = menu['label'].replace('_', '')
                    else:
                        ul = None

                    menu_win[-1].add_command(label = menu['label'], accelerator = self.name_key(menu['key']), image = menu['image'], compound = 'left', command = menu['command'], underline = ul)
                    if menu['key']:
                        self.master.bind_all(menu['key'], menu['command'])

                elif menu['type'] == 'separator':
                    menu_win[-1].add_separator()

                elif menu['type'] == 'end':
                    menu_win.pop(-1)

                elif menu['type'] == 'recent':
                    if '_' in menu['label']:
                        ul = menu['label'].index('_')
                        menu['label'] = menu['label'].replace('_', '')
                    else:
                        ul = None

                    self.menu_recent = MenuRecent(self.open_recent, self.pm)
                    menu_win[-1].add_cascade(menu = self.menu_recent, label = menu['label'], image = menu['image'], compound = 'left', underline = ul)

            else:
                if menu['type'] == 'cascade':
                    if '_' in menu['label']:
                        ul = menu['label'].index('_')
                        menu['label'] = menu['label'].replace('_', '')
                    else:
                        ul = None

                    self.menu_projet = Menu(self.menubar, tearoff = 0)
                    self.menubar.add_cascade(label = menu['label'], menu = self.menu_projet, underline = ul)

        for menu in self.right_click_files:
            if menu['type'] == 'command' and menu['key']:
                self.tree_files.bind(menu['key'], menu['command'])

        self.menu_recent.load_story()

    def clkright_pages(self, evt): # Les fonctions sont dans pagesfncts.py
        popup = Menu(self.pages_draw, tearoff = 0)
        popup.add_command(label = 'Extraire cette page', command = lambda: self.extract(evt, 'this'))
        popup.add_command(label = 'Retirer cette page', command = lambda: self.remove(evt, 'this'))
        popup.add_separator()
        popup.add_command(label = 'Extraire les pages séléctionnées', command = lambda: self.extract(evt, 'selected'))
        popup.add_command(label = 'Retirer les pages séléctionnées', command = lambda: self.remove(evt, 'selected'))
        popup.add_separator()
        popup.add_command(label = 'Retirer le fichier', command = lambda: self.remove_file(evt))
        popup.add_command(label = 'Séparer le fichier', command = lambda: self.split_page(evt))
        popup.tk_popup(evt.x_root, evt.y_root)

    def clkright_files(self, evt):
        popup = Menu(self.tree_files, tearoff = 0)
        menu_win = [popup]
        for menu in self.right_click_files:
            if menu['type'] == 'cascade':
                menu_win.append(Menu(menu_win[-1], tearoff = 0))
                menu_win[-2].add_cascade(label = menu['label'], menu = menu_win[-1], accelerator = menu['key'], image = menu['image'], compound = 'left')

            elif menu['type'] == 'command':
                menu_win[-1].add_command(label = menu['label'], accelerator = self.name_key(menu['key']), image = menu['image'], compound = 'left', command = menu['command'])

            elif menu['type'] == 'separator':
                menu_win[-1].add_separator()

            elif menu['type'] == 'end':
                menu_win.pop(-1)

        popup.tk_popup(evt.x_root, evt.y_root)

    def clkright_insert(self, evt):
        pass

    def configure(self):
        if self.locker.open_function(self.configure): return

        cf = Configurator(self.master, self.Imager)
        cf.Generate()
        self.locker.close_function(self.configure)

    def about(self):
        if self.locker.open_function(self.about): return

        ab = About(self.master, self.Imager)
        ab.Generate()
        self.locker.close_function(self.about)

    def search(self):
        if self.locker.open_function(self.search): return

        pages = self.get_pages()
        file = self.Runner.export_fusion({'pages': pages})
        srw = SearchWin(self.master, file)
        srw.Generate()
        self.locker.close_function(self.search)

    def aide_doc(self, file):
        if self.locker.open_function(self.aide_doc): return
        self.locker.aload(self.new_userForm)

        doc = Documentation(file, self.master)
        doc.Generate()
        self.locker.close_function(self.aide_doc)

if __name__ == '__main__':
    from mainwin import *
    mw = MainWindow()
    mw.Generate()
