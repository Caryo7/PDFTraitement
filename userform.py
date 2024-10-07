from tkinter import *
from tkinter import ttk
from tkinter.ttk import *
from tkinter.messagebox import *
from tkinter.filedialog import *
from customwidgets import *
from filesetting import *
from confr import *

class Utility:
    def isadigit(self, value):
        rest = 0
        for char in list(value):
            if not char.isdigit():
                rest += 1

        if rest == 0:
            return True
        else:
            return False

    def typeOf(self, value):
        if isinstance(value, list):
            for i in range(len(value)):
                value[i] = self.typeOf(value[i])
            return value
        else:
            if len(value) == 1 and value.isdigit():
                return int(value)
            elif len(value) == 1:
                return str(value)
            elif len(value) == 0:
                return ''
            elif self.isadigit(value):
                return int(value)
            else:
                return str(value)

    def widget_infos(self, line):
        line = line.split(':')
        arg = line[0].replace(' ', '')
        values = ':'.join(line[1:])
        if values == '':
            return arg.lower(), values
        while values[0] == ' ':
            values = values[1:]
            if values == '':
                break
        return arg.lower(), values

class UserFormDrawer(Utility):
    def __init__(self, parent, content):
        pm = Settings()
        self.file_unit = FileTypes(pm.paths.userformwin)

        self.parent = parent
        self.widgets = {}
        self.window = {}
        self.buffer = None
        self.commands = {}
        self.base_cmd = {}
        self.variables = {}
        self.cmd_init = []
        self.result = None

        self.load_content(content)
        self.draw_window()
        self.update_base_cmd()
        self.run_init()

    def storeVar(self, var):
        self.variables[var] = self.buffer
        return self.buffer

    def putBuffer(self, value):
        self.buffer = value
        return value

    def insertWidget(self, widget, var, mode):
        wid = widget.split('-')
        kind = wid[0]
        if var not in list(self.variables.keys()):
            showerror('Erreur', 'Erreur sur la mémoire\nLa variable ' + var + " n'est pas définie")
            return
        if not var:
            return

        if kind == 'ENTRY' and mode == 'add':
            self.widgets[widget]['widget'].insert('end', self.variables[var])
        elif kind == 'ENTRY' and mode == 'replace':
            self.widgets[widget]['widget'].delete('0', 'end')
            self.widgets[widget]['widget'].insert('end', self.variables[var])
        elif kind in ('LABEL', 'BUTTON') and mode == 'add':
            txt = self.widgets[widget]['widget'].cget('text')
            self.widgets[widget]['widget'].config(text = txt + self.variables[var])
        elif kind in ('LABEL', 'BUTTON') and mode == 'replace':
            self.widgets[widget]['widget'].config(text = self.variables[var])

        return self.buffer

    def getWidgetContent(self, wid):
        item = self.widgets[wid]
        widget = item['widget']
        if item['type'] == 'ENTRY':
            return widget.get('0', 'end')
        elif item['type'] in ('LABEL', 'BUTTON'):
            return widget.cget('text')

    def removeVar(self, var):
        del self.variables[var]
        return self.buffer

    def askopen(self, file_type):
        file = self.file_unit.open_file(title = 'Ouvrir un fichier', filetype = file_type)
        if not file:
            return ''

        return file

    def asksave(self, file_type):
        file = self.file_unit.save_file(title = 'Enregistrer un fichier', filetype = file_type)
        if not file:
            return ''

        return file

    def update_base_cmd(self):
        self.base_cmd = {
            'EXIT': lambda: self.master.destroy(),
            'SAVE': lambda: self.validate(),
            'OPENFILE': lambda name: self.askopen(name),
            'SAVEFILE': lambda name: self.asksave(name),
            'STORE': lambda var: self.storeVar(var),
            'INSERT': lambda widget, var: self.insertWidget(widget, var, 'add'),
            'SET': lambda widget, var: self.insertWidget(widget, var, 'replace'),
            'PUT': lambda value: self.putBuffer(value),
            'GET': lambda widget: self.getWidgetContent(widget),
            'DEL': lambda var: self.removeVar(var),
            }

    def load_content(self, content):
        lines = content.split('\n')
        section = ''
        for line in lines:
            if not line:
                continue

            if line[0] == ';': # Commentaire
                continue

            if ';' in line:
                i = 0
                while line[i] != ';':
                    i += 1
                line = line[:i]
                i -= 1
                while line[-1] == ' ':
                    line = line[:-1]

            if line[:2] == '$$':
                mode = 'window'
                section = ''
                continue

            elif line[:2] == '**':
                section = line[2:]
                self.commands[section] = []
                self.cmd_init.append(section)
                mode = 'command'
                continue

            elif line[0] == '$':
                lne = line[1:].split('-')
                kind = lne[0]
                section = '-'.join(lne)
                self.widgets[section] = {'type': kind}
                mode = 'widget'
                continue

            elif line[0] == '*':
                section = line[1:]
                self.commands[section] = []
                mode = 'command'
                continue

            if mode == 'widget':
                arg, values = self.widget_infos(line)
                self.widgets[section][arg] = self.typeOf(values)
            elif mode == 'window':
                arg, values = self.widget_infos(line)
                self.window[arg] = self.typeOf(values)
            elif mode == 'command':
                self.commands[section].append(line)

    def runCommand(self, widget = None, cmd = None):
        if cmd == None:
            for name, wid in self.widgets.items():
                if wid['widget'] == widget and 'command' in list(wid.keys()):
                    cmd = wid['command']

        if not cmd:
            return

        cmd = cmd[1:]
        cmd = cmd.split('+')
        cmd_name = cmd[0]
        args = self.typeOf(cmd[1:])
        if cmd_name in list(self.base_cmd.keys()):
            self.buffer = self.base_cmd[cmd_name](*args)
        elif cmd_name in list(self.commands.keys()):
            for command in self.commands[cmd_name]:
                self.runCommand(cmd = command)
        else:
            showerror('Erreur', "Erreur sur l'appel de fonction\nLa fonction " + cmd_name + " n'est pas définie, ni sur les fonctions intégrées, ni sur les fonctions personnelles")

    def draw_window(self):
        self.master = Toplevel(self.parent)
        for key, value in self.window.items():
            if key == 'transient' and value == 1:
                self.master.transient(self.parent)
            elif key == 'title':
                self.master.title(value)
            elif key == 'column':
                col, weight = self.typeOf(value.split('+'))
                self.master.columnconfigure(col, weight = weight)
            elif key == 'row':
                row, weight = self.typeOf(value.split('+'))
                self.master.rowconfigure(row, weight = weight)
            elif key == 'resize':
                w, h = self.typeOf(value.split('+'))
                self.master.resizable(bool(w), bool(h))
            elif key == 'minsize':
                w, h = self.typeOf(value.split('+'))
                self.master.minsize(w, h)

        for name, widget in self.widgets.items():
            kind = widget['type']
            if kind == 'LABEL':
                self.widgets[name]['widget'] = ttk.Label(self.master)
                self.widgets[name]['widget'].grid(sticky = 'w')
            elif kind == 'BUTTON':
                self.widgets[name]['widget'] = ttk.Button(self.master)
                self.widgets[name]['widget'].grid(sticky = 'we')
            elif kind == 'ENTRY':
                self.widgets[name]['widget'] = ttk.Entry(self.master)
                self.widgets[name]['widget'].grid(sticky = 'we')

            for key, value in widget.items():
                if key == 'widget':
                    continue

                if key == 'text' and kind in ('LABEL', 'BUTTON'):
                    self.widgets[name]['widget'].config(text = value)
                elif key == 'text' and kind == 'ENTRY':
                    self.widgets[name]['widget'].insert('end', value)
                elif key == 'row':
                    self.widgets[name]['widget'].grid(row = value)
                elif key == 'col':
                    self.widgets[name]['widget'].grid(column = value)
                elif key == 'rowspan':
                    self.widgets[name]['widget'].grid(rowspan = value)
                elif key == 'colspan':
                    self.widgets[name]['widget'].grid(columnspan = value)
                elif key == 'sticky':
                    self.widgets[name]['widget'].grid(sticky = value)
                elif key == 'command' and kind == 'BUTTON':
                    self.widgets[name]['widget'].bind('<Button-1>', lambda evt: self.runCommand(evt.widget))
                elif key == 'tooltip':
                    ToolTip(self.widgets[name]['widget'], value)
                elif key == 'show' and kind == 'ENTRY':
                    self.widgets[name]['widget'].config(show = value)

            self.widgets[name]['widget'].grid(padx = 5, pady = 5)

    def run_init(self):
        for cmd in self.cmd_init:
            self.runCommand(cmd = '*' + cmd)

    def validate(self):
        self.result = self.variables
        for name, widget in self.widgets.items():
            if widget['type'] == 'LABEL':
                self.result[name] = widget['widget'].cget('text')
            elif widget['type'] == 'ENTRY':
                self.result[name] = widget['widget'].get()

    def show(self):
        self.master.wait_window()
        return self.result

class UserFormGenerator(Utility):
    def __init__(self, parent, name, content):
        self.old_content = content
        self.output = self.old_content

        self.parent = parent
        self.root = Toplevel(parent)
        self.root.protocol('WM_DELETE_WINDOW', lambda: None)
        self.root.title('UserForm - ' + str(name))
        self.root.columnconfigure(0, weight = 1)
        self.root.columnconfigure(1, weight = 1)
        self.root.rowconfigure(0, weight = 1)

        self.note = ttk.Notebook(self.root)
        self.note.grid(row = 0, column = 0, padx = 5, pady = 5, sticky = 'nswe', columnspan = 2)

        self.master = ttk.Frame(self.note)
        self.note.add(text = 'Aperçu', child = self.master)

        frtxt = ttk.Frame(self.note)
        frtxt.columnconfigure(0, weight = 1)
        frtxt.columnconfigure(1, weight = 1)
        frtxt.rowconfigure(1, weight = 1)
        self.note.add(text = 'Programme', child = frtxt)

        self.text = ProgramText(frtxt, data = content, lang = 'basic')
        self.text.grid(row = 1, column = 0, sticky = 'nswe', columnspan = 2)

        btn_upd = ttk.Button(frtxt, text = 'Rafraichir l\'aperçu', command = self.refraish)
        btn_upd.grid(row = 0, column = 0, padx = 5, pady = 5, sticky = 'we')

        btn_lnc = ttk.Button(frtxt, text = 'Lancer la fenêtre', command = self.launch)
        btn_lnc.grid(row = 0, column = 1, padx = 5, pady = 5, sticky = 'we')

        close = ttk.Button(self.root, text = 'Valider', command = self.valide)
        close.grid(row = 1, column = 0, padx = 5, pady = 5, sticky = 'we')

        cancel = ttk.Button(self.root, text = 'Annuler', command = self.root.destroy)
        cancel.grid(row = 1, column = 1, padx = 5, pady = 5, sticky = 'we')

        self.widgets = {}
        self.window = {}
        self.columnconfigured = []
        self.rowconfigured = []
        self.content = content
        self.load_content()
        self.draw_window()

    def launch(self):
        self.refraish(False)
        uf = UserFormDrawer(self.root, self.content)
        results = uf.show()
        if results:
            txt = ''
            for k, v in results.items():
                txt += k + ' : ' + v + '\n'
            showinfo('Retour', 'La fenêtre a retourné les paramètres suivants\n' + txt)
        else:
            showinfo('Retour', 'La fenêtre n\'a rien retourné')

        self.root.focus()
        self.text.focus()

    def refraish(self, move = True):
        for k in list(self.widgets.keys()):
            del self.widgets[k]
        for k in list(self.window.keys()):
            del self.window[k]

        self.content = self.text.get('0.0', 'end')
        self.load_content()
        self.draw_window()
        if move:
            self.note.select(0)

    def load_content(self):
        lines = self.content.split('\n')
        section = ''
        try:
            for i, line in enumerate(lines):
                if not line:
                    continue

                if line[0] == ';': # Commentaire
                    continue

                if ';' in line:
                    i = 0
                    while line[i] != ';':
                        i += 1
                    line = line[:i]
                    i -= 1
                    while line[-1] == ' ':
                        line = line[:-1]

                if line[:2] == '$$':
                    mode = 'window'
                    section = ''
                    continue

                elif line[0] == '$':
                    lne = line[1:].split('-')
                    kind = lne[0]
                    section = '-'.join(lne)
                    self.widgets[section] = {'type': kind}
                    mode = 'widget'
                    continue

                if mode == 'widget':
                    arg, values = self.widget_infos(line)
                    self.widgets[section][arg] = self.typeOf(values)
                elif mode == 'window':
                    arg, values = self.widget_infos(line)
                    self.window[arg] = self.typeOf(values)

        except Exception:
            showerror('Syntaxe', "Erreur de syntaxe, ligne " + str(i+1))

    def clear_window(self):
        for widget in self.master.winfo_children():
            widget.destroy()
        for col in self.columnconfigured:
            self.master.columnconfigure(col, weight = 0)
        for row in self.rowconfigured:
            self.master.rowconfigure(row, weight = 0)

        self.columnconfigured = []
        self.rowconfigured = []

    def draw_window(self):
        self.clear_window()
        for key, value in self.window.items():
            if key == 'title':
                self.root.title('UserForm - ' + value)
            elif key == 'column':
                col, weight = self.typeOf(value.split('+'))
                self.columnconfigured.append(col)
                self.master.columnconfigure(col, weight = weight)
            elif key == 'row':
                row, weight = self.typeOf(value.split('+'))
                self.rowconfigured.append(row)
                self.master.rowconfigure(row, weight = weight)

        for name, widget in self.widgets.items():
            kind = widget['type']
            if kind == 'LABEL':
                self.widgets[name]['widget'] = ttk.Label(self.master)
                self.widgets[name]['widget'].grid(sticky = 'w')
            elif kind == 'BUTTON':
                self.widgets[name]['widget'] = ttk.Button(self.master)
                self.widgets[name]['widget'].grid(sticky = 'we')
            elif kind == 'ENTRY':
                self.widgets[name]['widget'] = ttk.Entry(self.master)
                self.widgets[name]['widget'].grid(sticky = 'we')

            for key, value in widget.items():
                if key == 'widget':
                    continue

                if key == 'text' and kind in ('LABEL', 'BUTTON'):
                    self.widgets[name]['widget'].config(text = value)
                elif key == 'text' and kind == 'ENTRY':
                    self.widgets[name]['widget'].insert('end', value)
                elif key == 'row':
                    self.widgets[name]['widget'].grid(row = value)
                elif key == 'col':
                    self.widgets[name]['widget'].grid(column = value)
                elif key == 'rowspan':
                    self.widgets[name]['widget'].grid(rowspan = value)
                elif key == 'colspan':
                    self.widgets[name]['widget'].grid(columnspan = value)
                elif key == 'sticky':
                    self.widgets[name]['widget'].grid(sticky = value)
                elif key == 'tooltip':
                    ToolTip(self.widgets[name]['widget'], value)
                elif key == 'show' and kind == 'ENTRY':
                    self.widgets[name]['widget'].config(show = value)

            self.widgets[name]['widget'].grid(padx = 5, pady = 5)

    def valide(self):
        self.output = self.text.get('0.0', 'end')
        self.root.destroy()

    def show(self):
        self.root.wait_window()
        return self.output

if __name__ == '__main__':
    root = Tk()
    txt = """$$MASTER
title: Choix du fichier de sortie
column: 1+1

$LABEL-Titre
text: Dossier de sortie ; Titre de la fenêtre de configuration
row: 0
col: 0
sticky: e

$ENTRY-File
row: 0
col: 1
sticky: we
tooltip: Nom du fichier à enregistrer !

$BUTTON-askdir
text: ...
command: /ouvrir_fichier
row: 0
col: 2
tooltip: Ouvre une boîte de Dialogue pour choisir un fichier

$BUTTON-ok; Bouton pour valider
text: Valider
command: /valider
row: 1
col: 0
colspan: 3
tooltip: Ferme la fenêtre et retourne le fichier choisi

*ouvrir_fichier
/OPENFILE+Fichiers PDF+*.pdf
/STORE+fichier
/SET+ENTRY-File+fichier

*valider
/SAVE
/EXIT
"""
    """; Structure des programmes :

; $$MASTER indique les paramètres pour la fenêtre, à ne mettre qu'une seule et unique fois
$$MASTER
title : Ma première fenêtre : je suis trop bon !!!   ; Petit test !
transient:1     ; Ceci est un commentaire sur une seule ligne !
column:0+1

; Définition des widgets par un simple $, suivit du type de widget. Séparé d'un tiret sans espaces, le numéro (ou nom) du widget. Très important !!!
$LABEL-1
text : Ceci est mon premier texte de Label, je suis tellement doué !
row:1
col:0
; Paramètres des label : text
$LABEL-2
text : Ceci est mon second texte de label, mais en troisième position !
row : 3
col: 0
$LABEL-3
text : Ceci est mon dernier (troisième) label, en seconde position !
row: 2

; Paramètres des boutons : text, command
$BUTTON-1
text: Fermer
col: 1
row: 1
sticky: nswe
command:/close

$BUTTON-2
text: Valider
col:1
row:2
sticky: nswe
command: /valider

$BUTTON-4
text: Inverser les lignes
col:1
row:3
sticky:nswe
command:/move

; Paramètres des Entry : text
$ENTRY-1
col:0
row:8
text: Benoit fait l'andouille !

$BUTTON-3
col:1
row:8
text: ...
command: /askopen

; Pour créer une fonction définition par une étoile. Ensuite, les différentes instructions
*close
/EXIT

*askopen
/OPENFILE+Fichier PDF+*.pdf
/STORE+file
/SET+ENTRY-1+file

*valider
/SAVE
/EXIT

; Fonction en double étoile : elles sont éxécutées au démarrage de la fenêtre (initialisation)
**init
/PUT+C:\\Benoit Data\\Programmes\\Python\\Projects\\Traitement PDF\\output.pdf
/STORE+file
/SET+ENTRY-1+file

*move
/GET+LABEL-1
/STORE+test_1
/GET+LABEL-3
/STORE+test_3
/SET+LABEL-3+test_1
/SET+LABEL-1+test_3
/DEL+test_1
/DEL+test_3

; Liste des commandes par défaut :
; /PUT+data : place "data" dans le buffer
; /STORE+var : place le contenu du buffer dans la variable "var"
; /SET+widget+var : remplace le contenu du texte du widget "widget" par le contenu de la variable "var"
; /INSERT+widget+var : comme au dessus, sans enlever le texte d'avant
; /SAVE : enregistre les paramètres pour qu'ils soient retournée à la fermeture de la fenêtre
; /EXIT : ferme la fenêtre et retourne les paramètres enresigtrés
; /OPENFILE+name+extension : Demande l'ouverture d'un fichier de format "name" et d'extension "extension"
; /SAVEFILE+name+extension : Demande l'enregistrement d'un fichier de format "name" et d'extension "extension"
; /GET+widget : met dans le buffer le texte du widget "widget"
; /DEL+var : supprime la variable "var" de la table
"""
    #u = UserFormDrawer(root, txt)
    u = UserFormGenerator(root, 'Nouveau userform', txt)
    print(u.show())
    root.mainloop()
