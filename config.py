from tkinter import *
from tkinter import ttk
from tkinter.ttk import *
from customwidgets import *
from confr import *
from tkinter.messagebox import *
from tkinter.filedialog import *
from filesetting import *
from tkinter.colorchooser import *

class TextPage:
    errors = 0

    def show(self, parent):
        self.master = parent
        self.master.columnconfigure(0, weight = 1)
        title = ttk.Label(self.master, text = self.TITLE, style = 'Title.TLabel', justify = 'left')
        title.grid(row = 0, column = 0, padx = 5, pady = 5, sticky = 'we')
        label = ttk.Label(self.master, text = self.TEXT, justify = 'left', wraplength = 400)
        label.grid(row = 1, column = 0, padx = 5, pady = 5, sticky = 'we')

    def save(self):
        pass

class AccueilPage(TextPage):
    TITLE = "Page de configuration"
    TEXT = """Dans ce menu des préférences, vous trouverez l'ensemble des informations relatives au logiciel pour une personnalisation au mieux.
Vous pourrez configurer les boutons en haut de la fenêtre principale pour une meilleur convivialité, selon vos programme personnels."""

class FichierPage(TextPage):
    TITLE = "Traitement et enregistrement des fichiers"
    TEXT = """Dans cet onglet, vous pourrez paramétrer les chemins des fichiers, les éxécutions ainsi que les paramètres d'enregistrement des métadonnées dans les fichiers de projet.
Tous les paramètres seront repris dans le reste du programme."""

class ThemeGUI:
    def __init__(self, settings):
        self.s = settings
        self.errors = 0
        self.lgs = ['Français', 'Anglais']
        self.units = ['défaut', 'cm', 'mm', 'inch', 'pouce']

    def show(self, parent):
        self.master = parent
        title = ttk.Label(self.master, text = 'Préférences générales de l\'interface', style = 'Title.TLabel')
        title.grid(row = 0, column = 0, padx = 5, pady = 10, sticky = 'w', columnspan = 3)

        self.style = StringVar(value = self.s.general['style'])
        stl = ttk.Label(self.master, text = 'Style de l\'interface')
        stl.grid(row = 1, column = 0, padx = 5, pady = 5, sticky = 'w')
        row = 1
        radio = []
        for i, st in enumerate(ttk.Style().theme_names()):
            row += 1
            radio.append(ttk.Radiobutton(self.master, variable = self.style, text = st, value = st))
            radio[-1].grid(row = row, column = 0, padx = 5, pady = 0, sticky = 'w')

        lg = ttk.Label(self.master, text = 'Langue')
        lg.grid(row = 1, column = 1, padx = 5, pady = 5, sticky = 'e')

        self.langue = ttk.Combobox(self.master, values = self.lgs)
        self.langue.grid(row = 1, column = 2, padx = 5, pady = 5, sticky = 'we')
        self.langue.current(self.lgs.index(self.s.general['langue']))

        ic = ttk.Label(self.master, text = 'Taille des icones')
        ic.grid(row = 2, column = 1, padx = 5, pady = 0, sticky = 'e', rowspan = 3)

        self.icon_size = StringVar(value = self.s.general['icon_size'])
        icon_grand = ttk.Radiobutton(self.master, text = 'Grand (48x48)', value = 'big', variable = self.icon_size)
        icon_grand.grid(row = 2, column = 2, padx = 5, pady = 0, sticky = 'w')
        icon_moyen = ttk.Radiobutton(self.master, text = 'Moyen (32x32)', value = 'medium', variable = self.icon_size)
        icon_moyen.grid(row = 3, column = 2, padx = 5, pady = 0, sticky = 'w')
        icon_small = ttk.Radiobutton(self.master, text = 'Petit (16x16)', value = 'small', variable = self.icon_size)
        icon_small.grid(row = 4, column = 2, padx = 5, pady = 0, sticky = 'w')

        self.zomed = StringVar(value = self.s.general['zomed'])
        self.draw_menu = StringVar(value = self.s.general['menu'])
        zm = ttk.Checkbutton(self.master, text = 'Maximiser la fenêtre au démarrage', onvalue = '1', offvalue = '0', variable = self.zomed)
        zm.grid(row = 5, column = 1, padx = 5, pady = 0, columnspan = 2, sticky = 'w')
        zm = ttk.Checkbutton(self.master, text = 'Afficher la barre de menu', onvalue = '1', offvalue = '0', variable = self.draw_menu)
        zm.grid(row = 6, column = 1, padx = 5, pady = 0, columnspan = 2, sticky = 'w')

        col_btn = ttk.Label(self.master, text = 'Boutons par colonnes')
        col_btn.grid(row = 7, column = 1, padx = 5, pady = 0, sticky = 'e')
        self.btn_per_col = ttk.Spinbox(self.master, from_ = 1, to = 20)
        self.btn_per_col.grid(row = 7, column = 2, padx = 5, sticky = 'we')
        self.btn_per_col.insert('end', self.s.general['buttons_col'])

        rfl_btn = ttk.Label(self.master, text = 'Nombre de fichiers récents')
        rfl_btn.grid(row = 8, column = 1, padx = 5, pady = 0, sticky = 'e')
        self.recent_file = ttk.Spinbox(self.master, from_ = 1, to = 20)
        self.recent_file.grid(row = 8, column = 2, padx = 5, sticky = 'we')
        self.recent_file.insert('end', self.s.general['recent_files'])

        ut = ttk.Label(self.master, text = 'Unité de mesure')
        ut.grid(row = 9, column = 1, padx = 5, pady = 5, sticky = 'e')
        self.unite = ttk.Combobox(self.master, values = self.units)
        self.unite.grid(row = 9, column = 2, padx = 5, pady = 5, sticky = 'we')
        self.unite.current(self.units.index(self.s.general['unit']))

        self.tips = StringVar(value = self.s.general['tips'])
        tip = ttk.Checkbutton(self.master, onvalue = '1', offvalue = '0', variable =  self.tips, text = 'Afficher les conseils au démarrage')
        tip.grid(row = 10, column = 0, columnspan = 3, padx = 5, pady = 5, sticky = 'w')

    def save(self):
        self.errors = 0
        self.s.set('general', 'style', self.style.get())
        if self.langue.get() not in self.lgs:
            self.errors += 1
        self.s.set('general', 'langue', self.langue.get())
        self.s.set('general', 'icon_size', self.icon_size.get())
        self.s.set('general', 'zomed', self.zomed.get())
        self.s.set('general', 'menu', self.draw_menu.get())
        self.s.set('general', 'buttons_col', self.btn_per_col.get())
        self.s.set('general', 'recent_files', self.recent_file.get())
        if self.unite.get() not in self.units:
            self.errors += 1
        self.s.set('general', 'unit', self.unite.get())
        self.s.set('general', 'tips', self.tips.get())

class ThemeEditor:
    def __init__(self, settings):
        self.s = settings
        self.errors = 0

    def select_color(self, evt):
        widget = evt.widget
        new_color = askcolor(color = widget.get(), parent = self.master, title = 'Nouvelle couleur')
        if new_color[1]:
            widget.delete('0', 'end')
            widget.insert('end', str(new_color[1]))
            self.change_color(evt)

    def show(self, parent):
        self.master = parent
        self.master.columnconfigure(0, weight = 1)
        title = ttk.Label(self.master, text = 'Préférence de l\'éditeur', style = 'Title.TLabel')
        title.grid(row = 0, column = 0, padx = 5, pady = 10, sticky = 'w', columnspan = 2)

        onglets = ttk.Notebook(self.master)
        onglets.grid(row = 1, column = 0, padx = 5, pady = 5, sticky = 'nswe')

        frame_colors = ttk.Frame(onglets)
        frame_colors.columnconfigure(1, weight = 1)
        frame_colors.columnconfigure(2, weight = 1)
        self.mots_clefs = []
        for k, v in self.s.getAll():
            if k == 'keys':
                continue
            self.mots_clefs.append({
                'name': v['text'],
                'fg': StringVar(value = v['fg']),
                'bg': StringVar(value = v['bg']),
                'option': k
                })

        row = 1
        title_fg = ttk.Label(frame_colors, text = 'Couleur de police')
        title_fg.grid(row = 0, column = 1, sticky = 'w', padx = 5, pady = 10)
        title_bg = ttk.Label(frame_colors, text = 'Couleur de fond')
        title_bg.grid(row = 0, column = 2, sticky = 'w', padx = 5, pady = 10)
        for kwd in self.mots_clefs:
            kwd['style'] = ttk.Style()
            kwd['style'].configure(kwd['name'] + '.TEntry', foreground = 'black', fieldbackground = 'white')
            kwd['style'].configure(kwd['name'] + '.TLabel', foreground = 'black', background = 'white')

            kwd['label'] = ttk.Label(frame_colors, text = kwd['name'], style = kwd['name'] + '.TLabel')
            kwd['label'].grid(row = row, column = 0, padx = 5, pady = 5, sticky = 'w')
            kwd['entry_fg'] = ttk.Entry(frame_colors, textvariable = kwd['fg'], style = kwd['name'] + '.TEntry')
            kwd['entry_fg'].grid(row = row, column = 1, padx = 5, pady = 5, sticky = 'we')
            kwd['entry_fg'].bind('<KeyRelease>', self.change_color)
            kwd['entry_fg'].bind('<Double-Button-1>', self.select_color)
            kwd['entry_bg'] = ttk.Entry(frame_colors, textvariable = kwd['bg'], style = kwd['name'] + '.TEntry')
            kwd['entry_bg'].grid(row = row, column = 2, padx = 5, pady = 5, sticky = 'we')
            kwd['entry_bg'].bind('<KeyRelease>', self.change_color)
            kwd['entry_bg'].bind('<Double-Button-1>', self.select_color)
            self.change_color(None, kwd)
            row += 1

        frame_keys = ttk.Frame(onglets)
        self.auto_backspace = IntVar(value = self.s.keys['auto_backspace'])
        self.auto_tab = IntVar(value = self.s.keys['auto_tab'])

        atb = ttk.Checkbutton(frame_keys, text = "Effectuer la tabulation au retour à la ligne", variable = self.auto_tab, onvalue = 1, offvalue = 0)
        atb.grid(row = 0, column = 0, padx = 5, pady = 5, sticky = 'w', columnspan = 2)
        nb_sps = ttk.Label(frame_keys, text = "Nombre d'espaces")
        nb_sps.grid(row =2, column= 0, padx = 5, pady = 5, sticky = 'e')
        self.nb_spaces = ttk.Spinbox(frame_keys, from_ = 2, to = 16)
        self.nb_spaces.set(self.s.keys['spaces'])
        self.nb_spaces.grid(row = 2, column = 1, padx =5, pady = 5, sticky = 'we')
        abp = ttk.Checkbutton(frame_keys, text = "Supprimer la tabulation en corrigeant un espace", variable = self.auto_backspace, onvalue = 1, offvalue = 0)
        abp.grid(row = 3, column = 0, padx = 5, pady = 5, sticky = 'w', columnspan = 2)

        onglets.add(text = 'Couleurs', child = frame_colors)
        onglets.add(text = 'Touches', child = frame_keys)

    def change_color(self, evt, line = None):
        if not line:
            for i in self.mots_clefs:
                if i['entry_fg'] == evt.widget or i['entry_bg'] == evt.widget:
                    line = i
                    continue

        style = line['style']
        fg = line['fg'].get()
        bg = line['bg'].get()
        try:
            style.configure(line['name'] + '.TEntry', foreground = fg, fieldbackground = bg)
            style.configure(line['name'] + '.TLabel', foreground = fg, background = bg)
        except:
            pass

    def save(self):
        self.errors = 0
        for mc in self.mots_clefs:
            if not mc['fg']: self.errors += 1
            if not mc['bg']: self.errors += 1
            self.s.set(mc['option'], 'fg', mc['fg'].get())
            self.s.set(mc['option'], 'bg', mc['bg'].get())

        if not self.nb_spaces.get(): self.errors += 1
        self.s.set('keys', 'auto_backspace', self.auto_backspace.get())
        self.s.set('keys', 'auto_tab', self.auto_tab.get())
        self.s.set('keys', 'spaces', self.nb_spaces.get())

class KeySelection:
    def __init__(self, settings):
        self.s = settings
        self.errors = 0

    def show(self, parent):
        self.master = parent
        self.master.columnconfigure(0, weight = 1)
        self.master.rowconfigure(0, weight = 1)

        scroll = ttk.Scrollbar(self.master, orient = 'vertical')
        scroll.grid(row = 0, column = 1, sticky = 'ns')

        self.tree = ttk.Treeview(self.master, columns = ('#1', '#2'), yscrollcommand = scroll.set)
        self.tree.grid(row = 0, column = 0, sticky = 'nswe')
        scroll.config(command = self.tree.yview)
        r = CellEditor(self.tree, actions = {'#1': {'type': 'Entry'},
                                             '#2': {'type': 'Entry'},})

        self.tree.heading('#0', text = 'Nom')
        self.tree.heading('#1', text = 'Touche clavier')
        self.tree.heading('#2', text = 'Informations')

        self.update_tree()

    def clear(self):
        for x in self.tree.get_children():
            self.tree.delete(x)

    def update_tree(self):
        self.clear()
        for key, values in self.s.getAll():
            self.tree.insert('', 'end', text = values['name'], values = [key, values['infos']])

    def save(self):
        #for i in self.tree.get_children():
            #item = self.tree.item(i)
            #self.s.set(item['values'][0], 'name', item['text'])
            #self.s.set(item['values'][0], 'infos', item['values'][1])
        pass

class MenuBouton:
    def __init__(self, settings):
        self.s = settings
        self.errors = 0

    def show(self, parent):
        self.master = parent
        self.master.columnconfigure(0, weight = 1)
        self.master.columnconfigure(1, weight = 1)
        self.master.rowconfigure(0, weight = 1)

        scroll = ttk.Scrollbar(self.master, orient = 'vertical')
        scroll.grid(row = 0, column = 2, sticky = 'ns')

        self.tree = ttk.Treeview(self.master, columns = ('#1', '#2', '#3'), yscrollcommand = scroll.set)
        self.tree.grid(row = 0, column = 0, sticky = 'nswe', columnspan = 2)
        scroll.config(command = self.tree.yview)

        r = CellEditor(self.tree, actions = {'#0': {'type': 'Entry'},
                                             '#1': {'type': 'Entry'},
                                             '#2': {'type': 'Combo', 'values': ['ArrangerDuo', 'ExtractImages', 'ExtractPages', 'SplitFile', 'RognerFile', 'Poster', 'OrganizePages', 'RemovePages', 'ScaleFile', 'MarginFile']},
                                             '#3': {'type': 'Entry'},})

        self.tree.heading('#0', text = 'Ordre', command = self.sort_items)
        self.tree.heading('#1', text = 'Titre')
        self.tree.heading('#2', text = 'Programme')
        self.tree.heading('#3', text = 'ToolTip')
        self.tree.column('#0', width = 40)

        add = ttk.Button(self.master, text = 'Ajouter un nouvel élément', command = self.append_item)
        add.grid(row = 1, column = 0, pady = 5, sticky = 'we')

        rem = ttk.Button(self.master, text = 'Supprimer un élément', command = self.remove_item)
        rem.grid(row = 1, column = 1, pady = 5, sticky = 'we')

        self.update_tree()

    def append_item(self, evt = None):
        n = 0
        for x in self.tree.get_children():
            n = int(self.tree.item(x)['text']) // 10
        n = (n + 1)*10
        self.tree.insert('', 'end', text = str(n), values = ['Nouveau programme personnalisé', 'Programe->', 'Avant "->", mettre le nom du programme. Après, mettre le fichier de la fonction ou "main" pour afficher le panneau de configuration du programme'])

    def remove_item(self, evt = None):
        x = self.tree.selection()
        for i in x:
            l = self.tree.item(i)['values'][0]
            confirm = askyesno('Supression', 'Confirmez vous la suppression de cette ligne ? Cette action ne peut être annulée !\n' + l)
            if not confirm:
                continue

            self.tree.delete(i)

    def sort_items(self):
        items = {}
        for iid in self.tree.get_children():
            it = self.tree.item(iid)
            items[int(it['text'])] = it['values']

        keys = list(items.keys())
        keys_sorted = sorted(keys)

        self.clear()
        for key in keys_sorted:
            self.tree.insert('', 'end', text = key, values = items[key])

    def clear(self):
        for x in self.tree.get_children():
            self.tree.delete(x)

    def update_tree(self):
        self.clear()
        for i, menu in self.s.getAll():
            name = menu['name']
            tooltip = menu['tooltip']
            function = menu['function']
            self.tree.insert('', 'end', text = str(10 * i), values = [name, function, tooltip])

    def save(self):
        self.s.reset()
        j = 0
        for i in self.tree.get_children():
            item = self.tree.item(i)
            name = item['values'][0]
            tooltip = item['values'][2]
            function = item['values'][1]
            self.s.set(j, 'name', name)
            self.s.set(j, 'function', function)
            self.s.set(j, 'tooltip', tooltip)
            j += 1

class PathConfig:
    def __init__(self, settings):
        self.s = settings
        self.errors = 0
        self.file_unit = FileTypes(self.s.configwin)

    def show(self, parent):
        self.master = parent
        self.master.columnconfigure(1, weight = 1)
        self.items = {'Fenêtre de configuration': {'s': 'configwin'},
                      'Fenêtre principale': {'s': 'mainwin'},
                      'Fenêtre d\'ajout de fonction': {'s': 'newfnctwin'},
                      'Modules personnalisés': {'s': 'progreader'},
                      }

        title = ttk.Label(self.master, text = 'Configuration des chemins', style = 'Title.TLabel')
        title.grid(row = 0, column = 0, columnspan = 3, padx = 5, pady = 5, sticky = 'w')

        row = 1
        for name, data in self.items.items():
            self.items[name]['var_open'] = StringVar(value = self.s.getItem(data['s'])['open'])
            self.items[name]['var_save'] = StringVar(value = self.s.getItem(data['s'])['save'])
            self.items[name]['var_dir'] = StringVar(value = self.s.getItem(data['s'])['dir'])
            self.items[name]['var_ropen'] = StringVar(value = self.s.getItem(data['s'])['rem_open'])
            self.items[name]['var_rsave'] = StringVar(value = self.s.getItem(data['s'])['rem_save'])
            self.items[name]['var_rdir'] = StringVar(value = self.s.getItem(data['s'])['rem_dir'])

            self.items[name]['label'] = ttk.Label(self.master, text = name)
            self.items[name]['label'].grid(row = row, column = 1, padx = 5, pady = 10, sticky = 'w')

            self.items[name]['label_open'] = ttk.Label(self.master, text = "Dossier d'ouverture")
            self.items[name]['label_open'].grid(row = row+1, column = 0, padx = 5, pady = 10, sticky = 'e')
            self.items[name]['label_save'] = ttk.Label(self.master, text = "Dossier d'enregistrement")
            self.items[name]['label_save'].grid(row = row+2, column = 0, padx = 5, pady = 10, sticky = 'e')
            self.items[name]['label_dir'] = ttk.Label(self.master, text = "Dossier par défaut")
            self.items[name]['label_dir'].grid(row = row+3, column = 0, padx = 5, pady = 10, sticky = 'e')

            self.items[name]['entry_open'] = ttk.Entry(self.master, textvariable = self.items[name]['var_open'])
            self.items[name]['entry_open'].grid(row = row+1, column = 1, padx = 5, pady = 5, sticky = 'we')
            self.items[name]['entry_save'] = ttk.Entry(self.master, textvariable = self.items[name]['var_save'])
            self.items[name]['entry_save'].grid(row = row+2, column = 1, padx = 5, pady = 5, sticky = 'we')
            self.items[name]['entry_dir'] = ttk.Entry(self.master, textvariable = self.items[name]['var_dir'])
            self.items[name]['entry_dir'].grid(row = row+3, column = 1, padx = 5, pady = 5, sticky = 'we')

            self.items[name]['check_l'] = ttk.Checkbutton(self.master, variable = self.items[name]['var_ropen'], onvalue = '1', offvalue = '0', text = 'Se souvenir du dernier dossier d\'ouverture')
            self.items[name]['check_l'].grid(row = row + 4, column = 1, padx = 5, pady = 0, sticky = 'we')
            self.items[name]['check_c'] = ttk.Checkbutton(self.master, variable = self.items[name]['var_rsave'], onvalue = '1', offvalue = '0', text = 'Se souvenir du dernier dossier d\'enregistrement')
            self.items[name]['check_c'].grid(row = row + 5, column = 1, padx = 5, pady = 0, sticky = 'we')
            self.items[name]['check_d'] = ttk.Checkbutton(self.master, variable = self.items[name]['var_rdir'], onvalue = '1', offvalue = '0', text = 'Se souvenir du dernier dossier séléctionné')
            self.items[name]['check_d'].grid(row = row + 6, column = 1, padx = 5, pady = 0, sticky = 'we')

            self.items[name]['btn_open'] = ttk.Button(self.master, text = '...', width = 3)
            self.items[name]['btn_open'].grid(row = row+1, column = 2, padx = 5, pady = 5, sticky = 'w')
            self.items[name]['btn_open'].bind('<Button-1>', lambda evt: self.ask_dir(evt, 'btn_open'))
            self.items[name]['btn_save'] = ttk.Button(self.master, text = '...', width = 3)
            self.items[name]['btn_save'].grid(row = row+2, column = 2, padx = 5, pady = 5, sticky = 'w')
            self.items[name]['btn_save'].bind('<Button-1>', lambda evt: self.ask_dir(evt, 'btn_save'))
            self.items[name]['btn_dir'] = ttk.Button(self.master, text = '...', width = 3)
            self.items[name]['btn_dir'].grid(row = row+3, column = 2, padx = 5, pady = 5, sticky = 'w')
            self.items[name]['btn_dir'].bind('<Button-1>', lambda evt: self.ask_dir(evt, 'btn_dir'))
            row += 7

    def ask_dir(self, evt, btn):
        wid = evt.widget
        for name, data in self.items.items():
            if wid == data[btn]:
                if btn == 'btn_open':
                    var = data['var_open']
                elif btn == 'btn_save':
                    var = data['var_save']
                elif btn == 'btn_dir':
                    var = data['var_dir']

        a = self.file_unit.open_dir(title = 'Ouvrir un dossier', initialdir = var.get())
        if a:
            var.set(a)

    def save(self):
        for key, data in self.items.items():
            self.s.set(data['s'], 'open', data['var_open'].get())
            self.s.set(data['s'], 'save', data['var_save'].get())
            self.s.set(data['s'], 'dir', data['var_dir'].get())
            self.s.set(data['s'], 'rem_open', data['var_ropen'].get())
            self.s.set(data['s'], 'rem_save', data['var_rsave'].get())
            self.s.set(data['s'], 'rem_dir', data['var_rdir'].get())

class ParaFiles:
    def __init__(self, settings):
        self.s = settings
        self.errors = 0

    def show(self, parent):
        self.master = parent

    def save(self):
        pass

class RunSets:
    def __init__(self, pm):
        self.s = pm.run
        self.pm = pm
        self.errors = 0
        self.file_unit = FileTypes(pm.paths.configwin)

    def show(self, parent):
        self.master = parent
        self.master.columnconfigure(1, weight = 1)

        title = ttk.Label(self.master, text = 'Configuration des éxécutions', style = 'Title.TLabel')
        title.grid(row = 0, column = 0, padx = 5, pady = 10, sticky = 'w', columnspan = 2)

        self.folder = StringVar(value = self.s.general['default_folder'])
        self.file = StringVar(value = self.s.general['default_file'])
        self.all_open = StringVar(value = self.s.general['alwais_open'])
        self.show_stat = StringVar(value = self.s.general['show_stat'])
        self.replace_end = StringVar(value = self.s.general['replace_end'])
        self.alwais_open = StringVar(value = self.s.general['open_forall'])
        self.alwais_unselect = StringVar(value = self.s.general['unselect'])
        self.show_exportbox = StringVar(value = self.pm.general.general['export_box'])

        lb_file = ttk.Label(self.master, text = 'Dossier par défaut')
        lb_file.grid(row = 1, column = 0, padx = 5, pady = 5, sticky = 'e')
        fold = ttk.Entry(self.master, textvariable = self.folder)
        fold.grid(row = 1, column = 1, padx = 5, pady = 5, sticky = 'we')
        btn = ttk.Button(self.master, text = '...', width = 3, command = lambda: self.ask('folder'))
        btn.grid(row = 1, column = 2, padx = 5, pady = 5)

        lb_file = ttk.Label(self.master, text = 'Fichier par défaut')
        lb_file.grid(row = 2, column = 0, padx = 5, pady = 5, sticky = 'e')
        fold = ttk.Entry(self.master, textvariable = self.file)
        fold.grid(row = 2, column = 1, padx = 5, pady = 5, sticky = 'we')
        btn = ttk.Button(self.master, text = '...', width = 3, command = lambda: self.ask('file'))
        btn.grid(row = 2, column = 2, padx = 5, pady = 5)

        allo = ttk.Checkbutton(self.master, text = "Ouvrir le fichier de sortie", onvalue = '1', offvalue = '0', variable = self.all_open)
        allo.grid(row = 3, column = 0, columnspan = 2, padx = 5, pady = 5, sticky = 'w')
        brst = ttk.Checkbutton(self.master, text = "Afficher la barre de statut", onvalue = '1', offvalue = '0', variable = self.show_stat)
        brst.grid(row = 4, column = 0, columnspan = 2, padx = 5, pady = 5, sticky = 'w')
        repl = ttk.Checkbutton(self.master, text = "Toujours Remplacer l'arborecense par le fichier généré", onvalue = '1', offvalue = '0', variable = self.replace_end)
        repl.grid(row = 5, column = 0, columnspan = 2, padx = 5, pady = 5, sticky = 'w')

        alwopen = ttk.Checkbutton(self.master, text = 'Toujours ouvrir le fichier crée', onvalue = '1', offvalue = '0', variable = self.alwais_open)
        alwopen.grid(row = 6, column = 0, columnspan = 2, padx = 5, pady = 5, sticky = 'w')
        unselect = ttk.Checkbutton(self.master, text = 'Toujours déséléctionner les pages exportées', onvalue = '1', offvalue = '0', variable = self.alwais_unselect)
        unselect.grid(row = 7, column = 0, columnspan = 2, padx = 5, pady = 5, sticky = 'w')
        unselect = ttk.Checkbutton(self.master, text = 'Ouvrir la boite d\'exportation', onvalue = '1', offvalue = '0', variable = self.show_exportbox)
        unselect.grid(row = 8, column = 0, columnspan = 2, padx = 5, pady = 5, sticky = 'w')

    def ask(self, mode):
        a = self.file_unit.open_dir(title = 'Séléctionner un repertoire') if mode == 'folder' else asksaveasfilename(title = 'Séléctionner un fichier par défaut', initialdir = '.', filetypes = [('Fichiers PDF', '*.pdf'), ('Tous les fichiers', '*.*')])

        if a and mode == 'folder':
            self.folder.set(a)
        elif a and mode == 'file':
            self.file.set(a)

    def save(self):
        self.s.set('general', 'default_folder', self.folder.get())
        self.s.set('general', 'default_file', self.file.get())
        self.s.set('general', 'alwais_open', self.all_open.get())
        self.s.set('general', 'show_stat', self.show_stat.get())
        self.s.set('general', 'replace_end', self.replace_end.get())
        self.s.set('general', 'open_forall', self.alwais_open.get())
        self.s.set('general', 'unselect', self.alwais_unselect.get())
        self.pm.general.set('general', 'export_box', self.show_exportbox.get())

class ProgramSet:
    def __init__(self, settings):
        self.s = settings
        self.errors = 0

    def show(self, parent):
        self.master = parent

        self.items = {
            'Editer les programmes par défaut': {'variable': StringVar(value = self.s.default['aload_change']), 'mode': 'default', 'option': 'aload_change'},
            'Supprimer les programmes par défaut': {'variable': StringVar(value = self.s.default['aload_del']), 'mode': 'default', 'option': 'aload_del'},

            'Editer les programmes personnels': {'variable': StringVar(value = self.s.perso['aload_change']), 'mode': 'perso', 'option': 'aload_change'},
            'Supprimer les programmes personnels': {'variable': StringVar(value = self.s.perso['aload_del']), 'mode': 'perso', 'option': 'aload_del'},
            }

        title = ttk.Label(self.master, text = 'Autorisations de modifications', style = 'Title.TLabel')
        title.grid(row = 0, column = 0, padx = 5, pady = 10, sticky = 'w')

        row = 1
        for key, value in self.items.items():
            self.items[key]['check'] = ttk.Checkbutton(self.master, text = key, onvalue = '1', offvalue = '0', variable = self.items[key]['variable'])
            self.items[key]['check'].grid(row = row, column = 0, padx = 5, pady = 5, sticky = 'w')
            if row == 2:
                row += 1
                l = ttk.Label(self.master, text = '')
                l.grid(row = row, pady = 5)
            row += 1

    def save(self):
        for key, value in self.items.items():
            self.s.set(value['mode'], value['option'], value['variable'].get())


class Configurator:
    def __init__(self, parent, Imager):
        self.parent = parent
        self.Imager = Imager

        self.master = Toplevel(parent)
        self.master.iconbitmap(Imager.ICONS['Gear'])
        self.master.transient(parent)
        self.master.title('Préférence')
        self.master.protocol('WM_DELETE_WINDOW', self.Quitter)
        self.master.columnconfigure(3, weight = 1)
        self.master.rowconfigure(0, weight = 1)
        self.master.minsize(900, 500)

        self.settings = Settings()

        self.menus = [
            {'iid': None, 'parent': None, 'title': 'Accueil', 'content': True, 'class': AccueilPage()},
            {'iid': None, 'parent': None, 'title': 'Interface', 'content': False, 'class': None},
            {'iid': None, 'parent': 'Interface', 'title': 'Thème Général', 'content': True, 'class': ThemeGUI(self.settings.general)}, # 
            {'iid': None, 'parent': 'Interface', 'title': 'Editeurs', 'content': False, 'class': None},
            {'iid': None, 'parent': 'Editeurs', 'title': 'Editeur Python', 'content': True, 'class': ThemeEditor(self.settings.editor_python)}, #
            {'iid': None, 'parent': 'Editeurs', 'title': 'Editeur GUI', 'content': True, 'class': ThemeEditor(self.settings.editor_basic)}, #

            {'iid': None, 'parent': 'Interface', 'title': 'Raccoucris Claviers', 'content': True, 'class': KeySelection(self.settings.keys)}, # 
            {'iid': None, 'parent': 'Interface', 'title': 'Boutons de menus', 'content': True, 'class': MenuBouton(self.settings.menus)}, #

            {'iid': None, 'parent': None, 'title': 'Fichier', 'content': True, 'class': FichierPage()},
            {'iid': None, 'parent': 'Fichier', 'title': 'Chemin de fichier', 'content': True, 'class': PathConfig(self.settings.paths)}, # 
            {'iid': None, 'parent': 'Fichier', 'title': 'Paramètre des PDFSEA', 'content': True, 'class': ParaFiles(self.settings)}, # Paramètres des fichiers : extension, utiliser un viewer, ... enregistrer méta données
            {'iid': None, 'parent': 'Fichier', 'title': 'Exécution des programmes', 'content': True, 'class': RunSets(self.settings)}, # Paramètres des prog : fichier de sortie par défaut, ..., ouverture systématique, ...

            {'iid': None, 'parent': None, 'title': 'Programmes', 'content': True, 'class': ProgramSet(self.settings.prog)}, #
            #{'iid': None, 'parent': None, 'title': '', 'content': True, 'class': None},
            ]

        self.scroll = ttk.Scrollbar(self.master, orient = 'vertical')
        self.scroll.grid(row = 0, column = 2, sticky = 'ns')
        self.items = ttk.Treeview(self.master, yscrollcommand = self.scroll.set, selectmode = 'browse')
        self.scroll.config(command = self.items.yview)
        self.items.grid(row = 0, column = 0, columnspan = 2, sticky = 'nswe')
        self.items.heading('#0', text = 'Elément')

        self.frame = ttk.Frame(self.master)
        self.frame.grid(row = 0, column = 3, sticky = 'nswe')

        self.insert()
        self.module = AccueilPage()
        self.module.show(self.frame)

        self.items.bind('<<TreeviewSelect>>', self.selected)

        label_warn = ttk.Label(self.master, text = '', image = self.Imager.Errors.default)
        label_warn.grid(row = 1, column = 0, padx = 5, pady = 5, sticky = 'e')

        self.nb_errors = StringVar(value = '0')
        errors = ttk.Label(self.master, textvariable = self.nb_errors)
        errors.grid(row= 1, column = 1, padx = 5, pady = 5, sticky = 'w')

        ok_btn = ttk.Button(self.master, text = 'Valider les changements', command = self.ok)
        ok_btn.grid(row = 1, column = 3, padx = 5, pady = 5, sticky = 'nswe')

    def insert(self):
        for i, menu in enumerate(self.menus):
            txt = menu['title']
            parent = ''
            if menu['parent'] != None:
                index = menu['parent']
                for m in self.menus:
                    if m['title'] == index:
                        parent = m['iid']

            self.menus[i]['iid'] = self.items.insert(parent, 'end', text = txt, open = True)

    def selected(self, evt):
        it = self.items.selection()
        if len(it) != 1:
            return

        item = self.items.item(it[0])
        err = 0
        for m in self.menus:
            if item['text'] == m['title'] and m['content']:
                self.module.save()
                self.frame.destroy()
                self.frame = ttk.Frame(self.master)
                self.frame.grid(row = 0, column = 3, sticky = 'nswe')
                self.module = m['class']
                self.module.show(self.frame)

            if m['class']:
                print(m['class'].errors)
                err += m['class'].errors

        self.nb_errors.set(str(err))

    def Generate(self):
        self.master.wait_window()

    def Quitter(self):
        self.cancel()

    def cancel(self):
        self.master.destroy()

    def ok(self):
        self.module.save()
        self.settings.reload_updates()
        self.cancel()


if __name__ == '__main__':
    from test import *
    e = Tester(['show_config'])
