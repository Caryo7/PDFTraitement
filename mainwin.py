from configparser import ConfigParser
from tkinter import *
from tkinter import ttk
from tkinter.ttk import *
from tkinter.simpledialog import *
from tkinter.messagebox import *
from tkinterdnd2 import *
from pathlib import Path
from PyPDF2 import *
from PIL import ImageTk
from customwidgets import *
from progwin import *
from thumbailer import *
from pagecount import *
from progresswin import *
from executer import *
import os, humanize
from confr import *
from menubar import *
from images import *
from project import *
from filesetting import *
from pagesfncts import *
from winlocker import *
from tips import *

####################################################################### problème sur la suppression de pages dans le fichier !!! def remove(self, evt, mode):

def CLEAR_TEMP(): # Pour vider le dossier temporaire
    p = Path('./temp_files/')
    for i in list(p.glob('**/*.*')):
        os.remove(i)

class StartupWidget:
    def __init__(self, master):
        image = PhotoImage(file = './images/startup.png')
        image = image.subsample(2)
        master.resizable(False, False)
        master.overrideredirect(1)
        label = ttk.Label(master, image = image)
        label.grid(row = 0, column = 0, sticky = 'nswe')
        width, height = image.width(), image.height()
        w, h = master.winfo_screenwidth(), master.winfo_screenheight()
        x, y = int(w/2 - width/2), int(h/2 - height/2)
        master.geometry(str(width) + 'x' + str(height) + '+' + str(x) + '+' + str(y))
        master.update()

class MainWindow(MenuBar, Project, PageFunctions):
    PADING = 15
    PAGE_SIZE = 250
    CASE_ON = '☑'
    CASE_OFF = '☐'

    def config_win(self, evt):
        if evt.widget == self.master:
            w = self.master.winfo_width()
            h = self.master.winfo_height()

            self.win_width, self.win_height = w, h

    def __init__(self, args = None):
        self.master = TkinterDnD.Tk()
        s = StartupWidget(self.master)

        CLEAR_TEMP()
        self.args = args
        self.TITLE = 'Utilitaire de PDF'

        self.Runner = Runner()
        self.pm = Settings()
        self.Imager = Images(self.pm)
        self.Imager.load_images()
        self.master.iconbitmap(self.Imager.ICONS['Logo'])

        self.LEN_COL = int(self.pm.general.general['buttons_col'])
        self.load_menus()

        style = ttk.Style()
        style.theme_use(self.pm.general.general['style'])
        style.configure('TNotebook', tabposition='sw')
        style.configure('TButton', tabposition='sw')
        style.configure('Title.TLabel', font = ('Calibri', 13, 'bold'))

        self.locker = WinLocker()
        self.file_unit = FileTypes(self.pm.paths.mainwin)

        self.images_list = {}
        self.images_draw = []
        self.names_pages = []
        self.file_infos = {}
        self.selection = {}
        self.bloc_used = []
        self.n_filter = 0

        ## 3 zones : bandeau haut avec boutons pour les programmes
        ##           onglets au centre :
        ##              Soit liste de fichiers (Treeview)
        ##              Soit liste de pages (Canvas)
        ##              Soit liste des fichiers à insérer (Treeview)
        ##           bandeau bas : boutons de lancement

        self.frame_prog = ttk.Frame(self.master)
        self.frame_prog.grid(row = 0, column = 0, padx = self.PADING, pady = self.PADING, sticky = 'nswe')
        for i in range(self.LEN_COL): self.frame_prog.columnconfigure(i, weight=1)

        self.onglets = ttk.Notebook(self.master)
        self.onglets.grid(row = 1, column = 0, padx = self.PADING, pady = self.PADING, sticky = 'nswe')

        self.frame_run = ttk.Frame(self.master)
        self.frame_run.grid(row = 2, column = 0, padx = self.PADING, pady = self.PADING, sticky = 'nswe')

        self.createOnglets()
        self.createPrograms()
        self.createOutput()

        self.Runner.start_load(self.launch_running, self.end_running, self.progress, self.stat, self.master)
        self.PR = ProgReader(self.master, self.USERFORMS, self.execute, self.output_folder, self.output_file, self.replace_output, self.open_end)

        self.master.overrideredirect(0)
        self.master.title(self.TITLE)
        self.master.protocol('WM_DELETE_WINDOW', self.Quitter)
        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(1, weight = 1)
        self.master.resizable(True, True)
        self.win_width, self.win_height = 0, 0
        self.master.bind('<Configure>', self.config_win)

        if self.pm.general.general['zomed'] == '1':
            self.master.wm_state('zoomed')

        self.master.update()
        self.master.geometry('1100x800')
        self.master.geometry('+50+50')

        self.tips = Tips(self.master, self.Imager, self.pm)
        self.tips.start_tips()

        self.run_launch(args)

    def run_launch(self, args):
        if not args:
            return False

        pro = args.project if args.project else []
        pdfs = args.PDF if args.PDF else []
        imgs = args.IMG if args.IMG else []
        seas = args.SEA if args.SEA else []
        csvs = args.CSV if args.CSV else []
        run = args.runing
        exe = args.execute
        output = args.output
        exit_end = args.exit_on_end
        save_end = args.save_on_end
        fichiers = args.files if args.files else []

        for fichier in fichiers:
            ext = self.file_unit.identify(fichier)
            if ext == 'PRO':
                pro.append(fichier)
            elif ext == 'IMG':
                imgs.append(fichier)
            elif ext == 'CSV':
                csvs.append(fichier)
            elif ext == 'SEA':
                seas.append(fichier)
            elif ext == 'PDF':
                pdfs.append(fichier)

        project = False
        if pro == None:
            pass
        elif len(pro) == 1:
            self.open_project(path = pro[0])
            project = True
        elif len(pro) > 1:
            project = True
            self.open_project(path = pro[0])
            self.import_project(paths = pro[1:])

        if pdfs:
            self.open_PDFfile(pdfs)
        if csvs:
            for csv in csvs:
                self.open_CSVfile(csv)

        if imgs:
            self.import_images(imgs)

        if seas:
            for sea in seas:
                self.add_function(sea)

        if output:
            p = Path(output)
            if p.is_file():
                self.output_file.set(value = str(os.path.abspath(p)))
                self.output_folder.set(value = str(os.path.abspath(p.parent)))
            else:
                self.output_folder.set(value = str(os.path.abspath(p)))

        if run == "FUSION":
            self.export_fusion(path = self.output_file.get())
        elif run == "IMAGES":
            self.export_images(folder = self.output_folder.get())
        elif run == "CSV":
            self.export_list(name = self.output_file.get())
        elif exe:
            self.execute(*tuple(exe))

        if save_end and project:
            self.save_project()

        if exit_end:
            self.Quitter()

    def createOnglets(self):
        self.frame_files = ttk.Frame(self.onglets)
        self.onglets.add(text = 'Fichiers de base', child = self.frame_files)

        self.frame_pages = ttk.Frame(self.onglets)
        self.onglets.add(text = 'Aperçu des pages de base', child = self.frame_pages)

        self.frame_insert = ttk.Frame(self.onglets)
        self.onglets.add(text = 'Fichiers à insérer', child = self.frame_insert)

        self.frame_files.columnconfigure(0, weight = 1)
        self.frame_files.rowconfigure(0, weight = 1)
        self.frame_pages.columnconfigure(0, weight = 1)
        self.frame_pages.rowconfigure(0, weight = 1)
        self.frame_insert.columnconfigure(0, weight = 1)
        self.frame_insert.rowconfigure(0, weight = 1)

        self.scrolly = ttk.Scrollbar(self.frame_files, orient = 'vertical')
        self.scrolly.grid(row = 0, column = 1, sticky = 'ns')
        self.tree_files = ttk.Treeview(self.frame_files, columns = ('#1', '#2', '#3', '#4'), yscrollcommand = self.scrolly.set)
        self.scrolly.config(command = self.tree_files.yview)
        self.tree_files.grid(row = 0, column = 0, sticky = 'nswe')
        self.tree_files.heading('#0', text = 'Fichier', command = self.sort_files)
        self.tree_files.heading('#1', text = 'Taille')
        self.tree_files.heading('#2', text = 'Nombre de Pages')
        self.tree_files.heading('#3', text = 'Inverser')
        self.tree_files.heading('#4', text = 'Pages à conserver')
        self.tree_files.column('#0', width = 250)
        self.tree_files.column('#1', width = 100)
        self.tree_files.column('#2', width = 150)
        self.tree_files.column('#3', width = 75)
        self.tree_files.column('#4', width = 150)
        self.tree_files.drop_target_register(DND_FILES)
        self.tree_files.dnd_bind('<<Drop>>', self.drop_file)
        self.tree_files.bind('<Button-3>', self.clkright_files)
        rf = CellEditor(self.tree_files, {'#4': {'type': 'Entry'}, '#3': {'type': 'Combo', 'values': ['NON', 'OUI']}}, self.update_infos)

        self.frame_move = ttk.Frame(self.frame_files)
        self.frame_move.grid(row = 0, column = 2, sticky = 'ns')
        for i in range(3): self.frame_move.rowconfigure(i, weight = 1)

        btn_up = ttk.Button(self.frame_move, width = 3, command = lambda : self.move('up'), image = self.Imager.Up.default)
        btn_up.grid(row = 0, column = 0, sticky = 'nswe')
        btn_up = ttk.Button(self.frame_move, width = 3, command = lambda : self.move('down'), image = self.Imager.Down.default)
        btn_up.grid(row = 1, column = 0, sticky = 'nswe')
        btn_up = ttk.Button(self.frame_move, text = 'Tri', width = 3, command = self.sort_files)
        btn_up.grid(row = 2, column = 0, sticky = 'nswe')

        self.scrollcy = ttk.Scrollbar(self.frame_pages, orient = 'vertical')
        self.scrollcy.grid(row = 0, column = 1, sticky = 'ns')
        self.scrollcx = ttk.Scrollbar(self.frame_pages, orient = 'horizontal')
        self.scrollcx.grid(row = 1, column = 0, sticky = 'we')
        self.pages_draw = Canvas(self.frame_pages, yscrollcommand = self.scrollcy.set, xscrollcommand = self.scrollcx.set)
        self.scrollcy.config(command = self.pages_draw.yview)
        self.scrollcx.config(command = self.pages_draw.xview)
        self.pages_draw.grid(row = 0, column = 0, sticky = 'nswe')
        self.pages_draw.drop_target_register(DND_FILES)
        self.pages_draw.dnd_bind('<<Drop>>', self.drop_file)
        self.pages_draw.bind('<Control-a>', lambda evt: self.selectall(evt, True))
        self.pages_draw.bind('<Control-A>', lambda evt: self.selectall(evt, False))

        self.pages_draw.bind('<Enter>', self._bound_to_mousewheel)
        self.pages_draw.bind('<Leave>', self._unbound_to_mousewheel)

        self.scrolli = ttk.Scrollbar(self.frame_insert, orient = 'vertical')
        self.scrolli.grid(row = 0, column = 1, sticky = 'ns')
        self.tree_insert = ttk.Treeview(self.frame_insert, columns = ('#1', '#2', '#3', '#4', '#5', '#6'), yscrollcommand = self.scrolli.set)
        self.scrolli.config(command = self.tree_insert.yview)
        self.tree_insert.grid(row = 0, column = 0, sticky = 'nswe')
        self.tree_insert.heading('#0', text = 'Fichier')
        self.tree_insert.heading('#2', text = 'Nombre de pages')
        self.tree_insert.heading('#3', text = 'Pages à conserver')
        self.tree_insert.heading('#4', text = 'Première page')
        self.tree_insert.heading('#5', text = 'Dernière page')
        self.tree_insert.heading('#6', text = 'Formule')
        self.tree_insert['displaycolumns'] = ('#2', '#3', '#4', '#5', '#6')
        self.tree_insert.drop_target_register(DND_FILES)
        self.tree_insert.dnd_bind('<<Drop>>', self.drop_insert)
        ri = CellEditor(self.tree_insert, {'#3': {'type': 'Entry'}, '#4': {'type': 'Entry'}, '#5': {'type': 'Entry'}, '#6': {'type': 'Entry'}})
        self.tree_insert.bind('<Button-3>', self.clkright_insert)

        frame_ibtn = ttk.Frame(self.frame_insert)
        frame_ibtn.grid(row = 0, column = 2, sticky = 'ns')
        for i in range(4): frame_ibtn.rowconfigure(i, weight = 1)

        ibtn_up = ttk.Button(frame_ibtn, width = 3, command = lambda : self.move_insert('up'), image = self.Imager.Up.default)
        ibtn_up.grid(row = 0, column = 0, padx = 5, pady = 5, sticky = 'nswe')
        ibtn_down = ttk.Button(frame_ibtn, width = 3, command = lambda : self.move_insert('down'), image = self.Imager.Down.default)
        ibtn_down.grid(row = 1, column = 0, padx = 5, pady = 5, sticky = 'nswe')
        ibtn_left = ttk.Button(frame_ibtn, width = 3, command = lambda : self.move_insert('left'), image = self.Imager.Left.default)
        ibtn_left.grid(row = 2, column = 0, padx = 5, pady = 5, sticky = 'nswe')
        ibtn_right = ttk.Button(frame_ibtn, width = 3, command = lambda : self.move_insert('right'), image = self.Imager.Right.default)
        ibtn_right.grid(row = 3, column = 0, padx = 5, pady = 5, sticky = 'nswe')

        ibtn_sort = ttk.Button(frame_ibtn, width = 3, text = 'Tri', command = lambda : self.move_insert('sort'))
        ibtn_sort.grid(row = 0, column = 1, padx = 5, pady = 5, sticky = 'nswe')
        ibtn_create = ttk.Button(frame_ibtn, width = 3, command = lambda : self.move_insert('create'), image = self.Imager.Add.default)
        ibtn_create.grid(row = 1, column = 1, padx = 5, pady = 5, sticky = 'nswe')

        if self.pm.general.general['menu'] == '1':
            self.draw_menu()
        else:
            self.master.bind('<Double-Button-1>', lambda _: self.draw_menu())

    def _bound_to_mousewheel(self, event):
        self.pages_draw.bind_all("<MouseWheel>", self._on_mousewheel)

    def _unbound_to_mousewheel(self, event):
        self.pages_draw.unbind_all("<MouseWheel>")

    def _on_mousewheel(self, event):
        self.pages_draw.yview_scroll(int(-1*(event.delta/120)), "units")

    def draw_pages(self):
        self.update_tree()
        self.update_pages()
        self.pages_draw.delete('all')
        offset_x, offset_y = 10, 10
        x, y = 0, 0
        X_MAX = self.win_width - self.PADING - self.PADING
        height_max = 0
        self.names_pages = []
        for i in range(len(self.images_draw)):
            image, page, file = self.images_draw[i]
            label = ttk.Label(self.pages_draw, text = self.CASE_OFF + ' ' + file + ' - Page ' + str(page), image = image, compound = 'top')
            label.bind('<Button-1>', self.select_image)
            label.bind('<Button-3>', self.clkright_pages)
            self.names_pages.append(label)
            a = self.pages_draw.create_window(x + offset_x, y + offset_y, window = label, anchor = 'nw')
            h = label.winfo_reqheight()
            if h > height_max:
                height_max = h

            x += self.PAGE_SIZE + offset_x
            if x + self.PAGE_SIZE > X_MAX:
                x = 0
                y += height_max + offset_y
                height_max = 0

        region = self.pages_draw.bbox('all')
        self.pages_draw.config(scrollregion = region)

    def reload_file(self):
        iids = self.tree_files.selection()
        progress = ProgressWindow(self.master, barres = ['Fichier rechargés', 'Images traités'])
        progress.config(bar = 0, maxi = len(iids))
        for iid in iids:
            item = self.tree_files.item(iid)
            file = item['text']
            path = self.file_infos[file]['path']
            size = os.path.getsize(path)
            size = humanize.naturalsize(size)
            th = Thumbail(path)
            self.images_list[file] = {}
            progress.config(bar = 1, maxi = th.nb_pages)
            i = 0
            for img in th.run():
                progress.step(bar = 1)
                self.images_list[file][i] = img
                i += 1

            pages = len(self.images_list[file])

            self.tree_files.set(iid, '#1', size)
            self.tree_files.set(iid, '#2', pages)
            progress.step(bar = 0)

        progress.finish()
        self.update_infos()

    def update_tree(self):
        for x in self.tree_files.get_children():
            self.tree_files.delete(x)

        for k, v in self.file_infos.items():
            self.tree_files.insert('', 'end', values = [v['size'], v['nb_pages'], v['reverse'], v['group']], text = k)

    def update_infos(self):
        copy = {}
        for i in self.tree_files.get_children():
            item = self.tree_files.item(i)
            file = item['text']
            size = item['values'][0]
            nb_pages = item['values'][1]
            reverse = item['values'][2]
            group = item['values'][3]
            copy[file] = {}
            copy[file]['path'] = self.file_infos[file]['path']
            copy[file]['size'] = size
            copy[file]['nb_pages'] = nb_pages
            copy[file]['reverse'] = reverse
            copy[file]['group'] = group

        if copy != self.file_infos:
            self.unsave()

        del self.file_infos
        self.file_infos = copy
        del copy
        self.draw_pages()

    def clear_files(self):
        for x in self.tree_files.get_children():
            self.tree_files.delete(x)

        self.unsave()
        self.update_infos()

    def update_pages(self):
        self.images_draw.clear()
        for x in self.tree_files.get_children():
            item = self.tree_files.item(x) # Récupération des données
            file = item['text'] # Nom du fichier
            infos = self.file_infos[file] # Informations du fichier
            _, _, reverse, utils = item['values'] # Ligne du tableau
            if reverse == 'OUI':
                reverse = True
            else:
                reverse = False

            pages_utils = getPagesNumber(utils, reverse, getCompleteList = True) # Page demandées et en nombre

            images_file = self.images_list[file]
            for i in pages_utils:
                if i - 1 not in list(images_file.keys()):
                    continue
                image = images_file[i - 1] # On récupère l'image de la liste brutte

                width = self.PAGE_SIZE
                rap = image.height / image.width
                height = width * rap
                image = image.resize((int(width), int(height))) # Traitement et redimensionnement
                self.images_draw.append([ImageTk.PhotoImage(image), i, file]) # On ajoute l'image (Tk) à la liste des images à afficher

    def createOutput(self):
        self.prog_selected = StringVar()
        self.output_folder = StringVar(value = str(os.path.abspath(self.pm.run.general['default_folder'])))
        self.output_file = StringVar(value = str(os.path.abspath(self.pm.run.general['default_file'])))
        self.frame_run.columnconfigure(1, weight = 1)
        self.stat = StringVar(value = 'Aucune éxécution en cours...')
        self.open_end = IntVar(value = int(self.pm.run.general['alwais_open']))
        self.replace_output = IntVar(value = int(self.pm.run.general['replace_end']))

        self.prog_label = ttk.Label(self.frame_run, text = 'Programme choisi')
        self.prog_label.grid(row = 0, column = 0, padx =5, pady = 5, sticky = 'e')

        self.entry_selected = ttk.Entry(self.frame_run, textvariable = self.prog_selected)
        self.entry_selected.grid(row = 0, column = 1, padx = 5, pady = 5, sticky = 'nswe', columnspan = 2)

        self.folder_label = ttk.Label(self.frame_run, text = 'Dossier de sortie')
        self.folder_label.grid(row = 1, column = 0, padx = 5, pady = 5, sticky = 'e')
        self.fichier_label = ttk.Label(self.frame_run, text = 'Fichier de sortie')
        self.fichier_label.grid(row = 2, column = 0, padx = 5, pady = 5, sticky = 'e')

        self.entry_folder = ttk.Entry(self.frame_run, textvariable = self.output_folder)
        self.entry_folder.grid(row = 1, column = 1, padx = 5, pady = 5, sticky = 'nswe')
        self.entry_fichier = ttk.Entry(self.frame_run, textvariable = self.output_file)
        self.entry_fichier.grid(row = 2, column = 1, padx = 5, pady = 5, sticky = 'nswe')

        btfolder = ttk.Button(self.frame_run, text = '...', width = 3, command = lambda: self.ask_file('dir'))
        btfolder.grid(row = 1, column = 2, padx = 5, pady = 5)
        btfile = ttk.Button(self.frame_run, text = '...', width = 3, command = lambda: self.ask_file('file'))
        btfile.grid(row = 2, column = 2, padx = 5, pady = 5)

        frame = ttk.Frame(self.frame_run)
        frame.grid(row = 3, column = 1, columnspan = 2, sticky = 'nswe')

        self.open_label = ttk.Checkbutton(frame, text = 'Ouvrir à la fin de l\'éxécution', onvalue = 1, offvalue = 0, variable = self.open_end)
        self.open_label.grid(row = 0, column = 0, padx = 5, pady = 5, sticky = 'w')
        self.open_label = ttk.Checkbutton(frame, text = 'Remplacer l\'arborecense par le fichier généré', onvalue = 1, offvalue = 0, variable = self.replace_output)
        self.open_label.grid(row = 0, column = 1, padx = 5, pady = 5, sticky = 'w')

        self.start = ttk.Button(self.frame_run, text = 'Lancer le programme', command = self.start_runner)
        self.start.grid(row = 4, column = 0, padx = 5, pady = 5, sticky = 'we')

        self.progress = ttk.Progressbar(self.frame_run, orient = 'horizontal', length = 100)
        self.progress.grid(row = 4, column = 1, padx = 5, pady = 5, sticky = 'nswe', columnspan = 2)

        if self.pm.run.general['show_stat'] == '1':
            self.st_label = ttk.Label(self.frame_run, text = 'Etat de l\'éxécution')
            self.st_label.grid(row = 5, column = 0, padx = 5, pady = 5, sticky = 'e')

            self.stat_label = ttk.Label(self.frame_run, textvariable = self.stat)
            self.stat_label.grid(row = 5, column = 1, padx = 5, pady = 5, sticky = 'w')

    def ask_file(self, kind):
        if kind == 'dir':
            a = self.file_unit.open_dir(title = 'Ouvrir un répertoire')
        elif kind == 'file':
            a = self.file_unit.save_file(title = 'Enregistrer sous')
        else:
            a = None

        if a and kind == 'dir':
            self.output_folder.set(a)
        elif a and kind == 'file':
            self.output_file.set(a)
            p = Path(a)
            self.output_folder.set(str(p.parent))

    def settingsProg(self, prog_name, pdfsea):
        if self.locker.open_function(self.settingsProg): return

        infos = self.Runner.TABLE_MOD[prog_name]
        title = infos['name']
        conf = ProgWindow(self.master, prog_name, title, infos)
        prog = conf.Generate()
        if prog:
            self.prog_selected.set(prog_name + '->' + str(os.path.abspath(prog)))

        self.locker.close_function(self.settingsProg)

    def execute(self, name, prog):
        if self.locker.open_function(self.execute, name, prog): return
        self.Runner.execute(name, prog)
        self.locker.close_function(self.execute)

    def getCommand(self, name):
        name, prog = name.split('->')
        cmd = None
        if prog == 'main':
            cmd = self.settingsProg
        else:
            cmd = self.execute

        command = lambda : cmd(name, prog)
        return command

    def start_runner(self):
        if self.locker.open_function(self.start_runner): return

        ps = self.prog_selected.get()
        if not ps:
            showerror('Programme', 'Vous devez séléctionner un fichier programme et un module d\'éxécution pour pouvoir lancer la génération')
            self.locker.close_function(self.start_runner)
            self.entry_selected.focus()
            return

        module, prog = ps.split('->')
        self.Runner.execute(module, prog)
        self.locker.close_function(self.start_runner)

    def launch_running(self, cmd):
        self.prog_selected.set(cmd)
        output_file = self.output_file.get()
        output_folder = self.output_folder.get()
        fs = self.tree_files.get_children()
        if not output_file:
            showerror('Paramétrage', 'Vous devez impérativement séléctionner un fichier de destination')
            self.entry_fichier.focus()
            return False
        if not output_folder:
            showerror('Paramétrage', 'Vous devez impérativement séléctionner un dossier de sortie. Il se met automatiquement à la séléction d\'un fichier de sortie')
            self.entry_folder.focus()
            return False
        if len(fs) == 0:
            showerror('Fichiers', 'Vous devez avoir au moins un fichier à traiter')
            return False

        pages = self.get_pages()

        return {
            'output_file': output_file,
            'output_folder': output_folder,
            'pages': pages,
            'open_end': self.open_end.get(),
            }

    def end_running(self):
        if self.replace_output.get():
            self.clear_files()
            self.import_file(self.output_file.get())

    def get_pages(self):
        fs = self.tree_files.get_children()
        pages = []
        for f in fs:
            item = self.tree_files.item(f)
            file = item['text'] # Nom du fichier
            infos = self.file_infos[file] # Informations du fichier
            _, _, reverse, utils = item['values'] # Ligne du tableau
            if reverse == 'OUI':
                reverse = True
            else:
                reverse = False

            pages_utils = getPagesNumber(utils, reverse, getCompleteList = True) # Page demandées et en nombre
            for p in pages_utils:
                pages.append({'page': p-1, 'path': infos['path']})

        return pages

    def createPrograms(self):
        self.commands = {}
        i = 0
        for index, item in self.pm.menus.getAll():
            text = item['name']
            tooltip = item['tooltip']
            cmd = item['function']

            self.commands[i] = {}
            self.commands[i]['name'] = text
            self.commands[i]['tooltip'] = tooltip
            self.commands[i]['function'] = cmd
            
            self.commands[i]['button'] = ttk.Button(self.frame_prog, text = text, command = self.getCommand(cmd))
            self.commands[i]['button'].grid(row = i // self.LEN_COL, column = i % self.LEN_COL, padx = 15, pady = 15, sticky = 'nswe')
            if tooltip:
                entete = '<p><b>Information sur le programme</b></p><p>'
                queue = '</p><p><i>La fenêtre suivante s\'ouvrira alors</i></p><p><image href="./images/progwin.png" size="200x155"></p>'
                e = ToolTip(self.commands[i]['button'], entete + tooltip + queue, mode_HTML = True)
                e.wraplength = 400
            i += 1

    def Quitter(self):
        if self.locker.open_function(self.Quitter): return
        self.locker.aload(self.close_project)
        self.close_project()

        self.master.destroy()

    def Generate(self):
        try:
            self.master.mainloop()
        except: # Si pas de fenêtre car ligne de commande
            pass


if __name__ == '__main__':
    from test import *
    e = Tester()
