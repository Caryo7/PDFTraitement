from userform import *
from tkinter import *
from filesetting import *

class ProgReader(Utility):
    def __init__(self, master, userforms, function_start, wid_folder, wid_file, wid_reinsert, wid_open):
        self.master = master
        self.USERFORMS = userforms
        self.wid_folder = wid_folder
        self.wid_file = wid_file
        self.wid_reinsert = wid_reinsert
        self.wid_open = wid_open
        self.cmd = function_start

        pm = Settings()

        self.file_unit = FileTypes(pm.paths.progreader)
        self.commands = {}
        self.variables = {}
        self.cmd_init = []
        self.base_cmd = {
            'EXIT': lambda: self.master.destroy(),
            'SAVE': lambda: self.validate(),
            'OPENFILE': lambda name: self.askopen(name),
            'SAVEFILE': lambda name: self.asksave(name),
            'STORE': lambda var: self.storeVar(var),
            'SET': lambda widget, var: self.insertWidget(widget, var),
            'PUT': lambda value: self.putBuffer(value),
            'GET': lambda widget: self.getWidgetContent(widget),
            'DEL': lambda var: self.removeVar(var),
            'RUN': lambda module, prog: self.runProgram(module_var, prog_var, var_mode = True),
            'SHOW': lambda uf: self.launchUserForm(uf),
            }
        self.default = ['ArrangerDuo', 'SplitFile', 'MarginFile', 'ExtractPages', 'ExtractImages', 'RognerFile']
        for d in self.default:
            self.base_cmd[d] = lambda module, prog: self.runProgram(module, prog)

    def launchUserForm(self, file):
        uf = UserFormDrawer(self.master, self.USERFORMS[file])

    def runProgram(self, module, prog, var_mode = False):
        if var_mode:
            module = self.variables[module]
            prog = self.variables[prog]

        self.cmd(module, prog)

    def close(self):
        self.commands = {}
        self.cmd_init = []
        self.content = ''

    def storeVar(self, var):
        self.variables[var] = self.buffer
        return self.buffer

    def putBuffer(self, value):
        self.buffer = value
        return value

    def insertWidget(self, widget, var):
        if var not in list(self.variables.keys()):
            showerror('Erreur', 'Erreur sur la mémoire\nLa variable ' + str(var) + " n'est pas définie")
            return
        if not var:
            return

        value = self.variables[var]
        if widget == 'FOLDER':
            self.wid_folder.set(value)
        elif widget == 'FILE':
            self.wid_file.set(value)
        elif widget == 'OPEN':
            self.wid_open.set(value)
        elif widget == 'REINSERT':
            self.wid_reinsert.set(value)

        return self.buffer

    def getWidgetContent(self, wid):
        if widget == 'FOLDER':
            return self.wid_folder.get()
        elif widget == 'FILE':
            return self.wid_file.get()
        elif widget == 'OPEN':
            return self.wid_open.get()
        elif widget == 'REINSERT':
            return self.wid_reinsert.get()

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

    def load(self, name, content):
        content = content.replace('\r', '')
        self.content += content

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

            if line[:2] == '**':
                section = line[2:]
                self.commands[section] = []
                self.cmd_init.append(section)
                mode = 'command'
                continue

            elif line[0] == '*':
                section = line[1:]
                self.commands[section] = []
                mode = 'command'
                continue

            if mode == 'command':
                self.commands[section].append(line)

    def getMenu(self):
        for c in self.cmd_init:
            yield c, lambda: self.run_cmd(c)

    def run_cmd(self, cmd):
        if cmd[0] == '/':
            cmd = cmd[1:]
        cmd = cmd.split('+')
        cmd_name = cmd[0]
        args = self.typeOf(cmd[1:])
        if cmd_name in self.default:
            args.insert(0, cmd_name)
        print('Execution de:', cmd_name, 'avec:', args)
        if cmd_name in list(self.base_cmd.keys()):
            self.buffer = self.base_cmd[cmd_name](*args)
        elif cmd_name in list(self.commands.keys()):
            for command in self.commands[cmd_name]:
                self.run_cmd(cmd = command)
        else:
            showerror('Erreur', "Erreur sur l'appel de fonction\nLa fonction " + str(cmd_name) + " n'est pas définie, ni sur les fonctions intégrées, ni sur les fonctions personnelles")

if __name__ == '__main__':
    from mainwin import *
    mw = MainWindow()
    mw.Generate()
