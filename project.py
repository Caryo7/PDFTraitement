from tkinter import *
from tkinter.simpledialog import *
import os, humanize

from infosfiles import *
from customwidgets import *
from confr import *
from separationwin import *
from progresswin import *
from newfnct import *
from proglister import *
from thumbailer import *
from extract import *
from userform import *
from pagecount import *
from managedef import *
from progreader import *
from printwin import *
from exportwin import *

class PDFPRO:
    def __init__(self, file, mode = 'auto'):
        self.mode = mode
        self.file = file

        self.userforms = {}
        self.tree = []
        self.programs = {}

        if mode in ('auto', 'r'):
            self.load_userforms()
            self.load_list()
            self.load_programs()
        elif mode == 'w':
            pass

    def load_userforms(self):
        z = zp.ZipFile(self.file, 'r')
        for f in z.namelist():
            if 'userforms/' not in f:
                continue
            if not z.read(f):
                continue

            self.userforms[f.replace('userforms/', '')] = z.read(f).decode('utf-8')

        z.close()

    def load_list(self):
        z = zp.ZipFile(self.file, 'r')
        tree = ''
        for f in z.namelist():
            if f != 'liste.csv':
                continue
            if not z.read(f):
                continue

            tree = z.read(f).decode('utf-8')

        tree = tree.split('\n')
        self.tree = []
        for i in range(len(tree)):
            if not tree[i]:
                continue

            name, file, invert, pages = tree[i].split(';')
            self.tree.append({'name': name,
                              'file': file,
                              'inversion': True if invert.lower() == 'oui' else False,
                              'pages': pages})

        z.close()

    def load_programs(self):
        z = zp.ZipFile(self.file, 'r')
        for f in z.namelist():
            if 'programs/' not in f:
                continue
            if not z.read(f):
                continue

            self.programs[f.replace('programs/', '')] = z.read(f).decode('utf-8')

        z.close()

    def write(self):
        if self.mode == 'r':
            raise IOError()

        z = zp.ZipFile(self.file, 'w')
        for file, content in self.userforms.items():
            f = z.open('userforms/' + file, 'w')
            f.write(content.encode('utf-8'))
            f.close()

        for file, content in self.programs.items():
            f = z.open('programs/' + file, 'w')
            f.write(content.encode('utf-8'))
            f.close()

        f = z.open('liste.csv', 'w')
        txt = ''
        for p in self.tree:
            txt += str(p['name']) + ';'
            txt += str(p['file']) + ';'
            txt += 'OUI' if p['inversion'] else 'NON'
            txt += ';' + str(p['pages']) + '\n'
        f.write(txt.encode('utf-8'))
        f.close()

        z.close()

    def close(self):
        del self.programs
        del self.userforms
        del self.tree

class Project:
    USERFORMS = {}
    PROGRAMS = {}
    SAVED = True
    PATH = None

    def open_project(self, evt = None, path = None):
        if self.locker.open_function(self.open_project, path): return

        if path == None:
            path = self.file_unit.open_file(title = 'Ouvrir un projet', filetype = 'PRO')

        if path:
            progress = ProgressWindow(self.master, barres = ['Ouverture...', 'Fichiers traités', 'Images traités'])
            progress.config(bar = 0, maxi = 3)

            self.locker.aload(self.close_project)
            self.close_project()

            f = PDFPRO(path)
            self.USERFORMS = f.userforms
            self.PROGRAMS = f.programs
            TREE = f.tree
            progress.step(0)
            f.close()
            # Lire le programme et préparer le menu avec les commandes
            progress.config(1, maxi = len(TREE))
            for data in TREE:
                file = data['file']
                pages = data['pages']
                invert = data['inversion']
                name = data['name']
                self.locker.aload(self.import_file)
                self.import_file(file, progress, 2, pages = pages, invert = invert, name = name)
                progress.step(bar = 1)

            progress.step(0)
            for name, content in self.PROGRAMS.items():
                self.PR.load(name, content)
                for lb, cmd in self.PR.getMenu():
                    self.menu_projet.add_command(label = lb, command = cmd)

            progress.step(0)
            self.save_ok()
            self.add_story(path)
            self.PATH = path

            progress.finish()

        self.locker.close_function(self.open_project)

    def import_project(self, evt = None, paths = None):
        if self.locker.open_function(self.import_project): return

        if paths == None:
            paths = self.file_unit.open_file(title = 'Importer des projets', filetype = 'PRO', multiple = True)

        progress = ProgressWindow(self.master, barres = ['Projets ouverts', 'Ouverture', 'Fichiers traités', 'Images traitées'])
        progress.config(bar = 0, maxi = len(paths))
        for path in paths:
            progress.config(bar = 1, maxi = 3)
            f = PDFPRO(path)
            prog_more = f.programs
            uf_more = f.userforms
            for name, content in f.userforms.items():
                self.USERFORMS[name] = content
            for name, content in f.programs.items():
                self.PROGRAMS[name] = content
            TREE = f.tree
            progress.step(1)
            f.close()
            progress.config(2, maxi = len(TREE))
            for data in TREE:
                file = data['file']
                pages = data['pages']
                invert = data['inversion']
                name = data['name']
                self.locker.aload(self.import_file)
                self.import_file(file, progress, 3, pages = pages, invert = invert, name = name)
                progress.step(bar = 2)
            progress.step(1)
            for name, content in prog_more.items():
                self.PR.load(name, content)
                for lb, cmd in self.PR.getMenu():
                    self.menu_projet.add_command(label = lb, command = cmd)

            progress.step(1)
            progress.step(0)

        self.unsave()
        progress.finish()

        self.locker.close_function(self.import_project)

    def unsave(self):
        self.SAVED = False
        p = str(self.PATH) if self.PATH else 'untitled.pdfpro'
        self.master.title('* ' + self.TITLE + ' - ' + p + ' *')

    def save_ok(self):
        self.SAVED = True
        p = str(self.PATH) if self.PATH else 'untitled.pdfpro'
        self.master.title(self.TITLE + ' - ' + p)

    def close_project(self, evt = None):
        if self.locker.open_function(self.close_project): return
        if not self.SAVED:
            ask = askyesnocancel('Fermeture', 'Voulez vous enregistrer avant de fermer ?')
            if ask == True:
                self.locker.aload(self.save_project)
                self.save_project()
            elif ask == None:
                self.locker.close_function(self.close_project)
                return

        self.clear_files()
        self.clear_menuprojet()
        self.USERFORMS = {}
        self.PROGRAMS = {}
        self.PATH = None
        self.save_ok()
        self.PR.close()
        self.locker.close_function(self.close_project)

    def add_story(self, file):
        self.menu_recent.load_story(file)

    def saveas_project(self, evt = None, path = None):
        if self.locker.open_function(self.saveas_project): return
        if not path:
            path = self.file_unit.save_file(filetype = 'PRO', title = 'Enretistrer le projet sous')

        if path:
            f = PDFPRO(path, 'w')
            f.userforms = self.USERFORMS
            f.tree = []
            for fp, data in self.file_infos.items():
                f.tree.append({'name': fp,
                               'file': str(os.path.abspath(data['path'])),
                               'inversion': True if data['reverse'] == 'OUI' else False,
                               'pages': data['group'],})
            f.programs = self.PROGRAMS
            f.write()
            self.save_ok()
            self.PATH = path
            self.add_story(self.PATH)

        self.locker.close_function(self.saveas_project)

    def save_project(self, evt = None):
        if self.locker.open_function(self.save_project): return

        if not self.PATH:
            self.locker.aload(self.saveas_project)
            self.saveas_project()
        else:
            f = PDFPRO(self.PATH)
            f.userforms = self.USERFORMS
            f.tree = []
            for fp, data in self.file_infos.items():
                f.tree.append({'name': fp,
                               'file': str(os.path.abspath(data['path'])),
                               'inversion': True if data['reverse'] == 'OUI' else False,
                               'pages': data['group'],})
            f.programs = self.PROGRAMS
            f.write()
            self.save_ok()

        self.locker.close_function(self.save_project)

    def saveascopy_project(self, evt = None, path = None):
        if self.locker.open_function(self.saveascopy_project): return

        if not path:
            path = self.file_unit.save_file(filetype = 'PRO', title = 'Enretistrer une copie du projet sous')

        if path:
            f = PDFPRO(path)
            f.userforms = self.USERFORMS
            f.tree = []
            for fp, data in self.file_infos.items():
                f.tree.append({'name': fp,
                               'file': str(os.path.abspath(data['path'])),
                               'inversion': data['reverse'],
                               'pages': data['group'],})
            f.programs = self.PROGRAMS
            f.write()

        self.locker.close_function(self.saveascopy_project)

    def config_def(self, evt = None, mode = 0):
        if self.locker.open_function(self.config_def): return

        m = Manager(self.master, mode, self.PROGRAMS, self.USERFORMS)
        self.PRORGAMS, self.USERFORMS = m.Generate()

        self.locker.close_function(self.config_def)

    def open_PDFfile(self, evt = None, path = None):
        if self.locker.open_function(self.open_PDFfile, evt, path): return

        if path == None:
            path = self.file_unit.open_file(title = 'Ouvrir un fichier', multiple = True)

        if path:
            self.import_files(path)
            self.unsave()

        self.locker.close_function(self.open_PDFfile)

    def open_CSVfile(self, evt = None, csv = None, progress = None, bar = None):
        if self.locker.open_function(self.open_CSVfile, evt, csv): return

        mode = True if progress != None else False

        if csv == None:
            csv = self.file_unit.open_file(title = 'Ouvrir une liste de fichiers', filetype = 'CSV')

        if csv:
            if progress == None:
                progress = ProgressWindow(self.master, barres = ['Fichiers traités', 'Images traités'])
            self.ask_sep = SeparationWin(self.master, csv)
            infos = self.ask_sep.launch()

            progress.config(bar = 0, maxi = progress.bars[0]['maxi'] + len(infos))

            for data in infos:
                file = data['file']
                pages = 'all'
                reverse = False
                if 'reverse' in list(data.keys()):
                    reverse = True if data['reverse'].lower() == 'oui' else False
                if 'pages' in list(data.keys()):
                    pages = data['pages']

                self.locker.aload(self.import_file)
                self.import_file(file, progress, 1, pages = pages, invert = reverse)
                progress.step(bar = 0)

            if not mode:
                progress.finish()

            self.add_story(csv)
            self.unsave()

        self.locker.close_function(self.open_CSVfile)

    def export_fusion(self, path = None):
        if self.locker.open_function(self.export_fusion): return

        if not path:
            path = self.file_unit.save_file(title = 'Enregistrer sous')

        if path:
            para = {}
            if self.pm.general.general['export_box'] == '1':
                eb = ExportWindow(self.master)
                para = eb.show()
                if para == {}:
                    self.locker.close_function(self.export_fusion)
                    return

            pages = self.get_pages()
            file = self.Runner.export_fusion({'pages': pages}, para)
            fin = open(file, mode = 'rb')
            fout = open(path, mode = 'wb')
            fout.write(fin.read())
            fin.close()
            fout.close()

            if self.pm.run.general['open_forall'] == '1':
                os.popen(path)

        self.locker.close_function(self.export_fusion)

    def export_list(self, name = None):
        if self.locker.open_function(self.export_list): return

        col_spliter = ';'
        row_spliter = '\n'
        if not name:
            name = self.file_unit.save_file(title = 'Enregistrer la liste sous', filetype = 'CSV')

        if not name:
            self.locker.close_function(self.export_list)
            return

        f = open(name, 'w', encoding = 'utf-8')
        f.write(col_spliter.join(['Fichier', 'Inverser', 'Pages']) + row_spliter)
        for file, data in self.file_infos.items():
            f.write(str(os.path.abspath(data['path'])))
            f.write(col_spliter)
            f.write(data['reverse'])
            f.write(col_spliter)
            f.write(data['group'].replace(';', ','))
            f.write(row_spliter)

        f.close()

        if self.pm.run.general['open_forall'] == '1':
            os.popen(name)

        self.locker.close_function(self.export_list)

    def add_function(self, event = None, name = None):
        if self.locker.open_function(self.add_function, event, name): return

        if name == None:
            name = self.file_unit.open_file(title = 'Ajouter une fonction', filetype = 'SEA')

        if name:
            fnct = NewFunction(self.master, name)
            r = fnct.show()
            if r:
                file, cat, name = r
                self.pl = ProgLister()
                self.pl.new(cat, file, 0, 0, name)

        self.locker.close_function(self.add_function)

    def drop_file(self, event):
        if self.locker.open_function(self.drop_file): return

        file = event.data
        files = file.split('} {')
        paths = []

        for file in files:
            file = file.replace('{', '')
            file = file.replace('}', '')
            paths.append(file)

        self.import_files(paths)
        self.locker.close_function(self.drop_file)

    def drop_insert(self, event):
        if self.locker.open_function(self.drop_insert): return

        file = event.data
        files = file.split('} {')
        paths = []

        for file in files:
            file = file.replace('{', '')
            file = file.replace('}', '')
            paths.append(file)

        self.import_insert(paths)
        self.locker.close_function(self.drop_insert)

    def import_insert(self, paths):
        for path in paths:
            path = Path(path)
            p = str(os.path.abspath(path))
            file = str(path.name)
            pdf = PdfReader(p)
            pages = len(pdf.pages)
            keep = '1-' + str(pages)
            self.tree_insert.insert('', 'end', text = file, values = [p, pages, keep, '1', '1', 'i = i'])

    def open_recent(self, path):
        if self.locker.open_function(self.open_recent): return
        kind = self.file_unit.identify(path)
        if kind == 'PDF':
            self.locker.aload(self.import_file)
            self.import_file(path)
        elif kind == 'CSV':
            self.locker.aload(self.open_CSVfile)
            self.open_CSVfile(csv = path)
        elif kind == 'PRO':
            self.locker.aload(self.open_project)
            self.open_project(path = path)
        elif kind == 'IMG':
            self.locker.aload(self.import_image)
            self.import_image(file = [path])

        self.locker.close_function(self.open_recent)

    def import_files(self, paths):
        progress = ProgressWindow(self.master, barres = ['Fichier traités', 'Images traités'])
        progress.config(bar = 0, maxi = len(paths))

        for i, path in enumerate(paths):
            kind = self.file_unit.identify(path)
            if kind == 'PDF':
                self.locker.aload(self.import_file)
                self.import_file(path, progress, 1)
            elif kind == 'CSV':
                self.locker.aload(self.open_CSVfile)
                self.open_CSVfile(csv = path, progress=progress, bar=1)
            elif kind == 'PRO':
                self.locker.aload(self.open_project)
                self.open_project(path = path)
            elif kind == 'IMG':
                self.locker.aload(self.import_images)
                self.import_images(file = [path], id_from = i)

            self.add_story(path)
            progress.step(bar = 0)

        progress.finish()
        self.unsave()

    def import_images(self, event = None, file = None, id_from = 0):
        if self.locker.open_function(self.import_images, event, file): return

        if file == None:
            file = self.file_unit.open_file(title = 'Ouvrir des images', filetype = 'IMG', multiple = True)

        if file:
            for i, fp in enumerate(file):
                output = './temp_files/image2pdf-{}.pdf'.format(str(id_from + i+1))
                GeneratePDFfromImage(fp, output)
                self.locker.aload(self.import_file)
                self.import_file(output)
                self.add_story(fp)

        self.unsave()

        self.locker.close_function(self.import_images)

    def export_images(self, event = None, folder = None):
        if self.locker.open_function(self.epxport_images, event, folder): return

        if folder == None:
            folder = self.file_unit.open_dir(title = 'Dossier de sortie des images')

        if folder:
            progress = ProgressWindow(self.master, barres = ['Préparation', 'Exportation'])
            progress.config(bar = 0, maxi = 5)

            progress.step(bar = 0)
            pages = self.get_pages()
            progress.step(bar = 0)
            file = self.Runner.export_fusion({'pages': pages})
            progress.step(bar = 0)
            def all_pages(i, l):
                return (True, 330)

            e = ExtractImages(file, all_pages, None, folder)
            progress.step(bar = 0)
            e.dpi = askinteger('DPI', 'Quelle résolution souhaitez vous ? (en DPI)')
            progress.step(bar = 0)
            progress.config(bar = 1, maxi = e.nb_iter)
            for i in e.run():
                progress.step(bar = 1)

            progress.finish()

            if self.pm.run.general['open_forall']:
                os.popen('start ' + folder)

        self.locker.close_function(self.export_images)

    def import_file(self, file, progress = None, bar = None, pages = 'all', invert = False, name = None):
        if self.locker.open_function(self.import_file, file, progress, bar, pages, invert): return

        if progress == None:
            progress = ProgressWindow(self.master, barres = ['Images traités'])
            bar = 0
            finish = True
        else:
            finish = False

        file = Path(file)
        try:
            pdf = PdfReader(file)
        except Exception:
            progress.step(bar = bar)
            self.locker.close_function(self.import_file)
            return

        size = os.path.getsize(file)
        size = humanize.naturalsize(size)

        if pages == 'all':
            pages = '1-' + str(len(pdf.pages))
        if invert:
            reverse = 'OUI'
        else:
            reverse = 'NON'

        if name == None:
            name = file.name

        self.file_infos[name] = {'path': file,
                                 'size': size,
                                 'nb_pages': len(pdf.pages),
                                 'reverse': reverse,
                                 'group': pages,}

        th = Thumbail(file)
        self.images_list[name] = {}
        progress.config(bar = bar, maxi = th.nb_pages)
        i = 0
        for img in th.run():
            progress.step(bar = bar)
            self.images_list[name][i] = img
            i += 1

        self.tree_files.insert('', 'end', values = [size, len(pdf.pages), reverse, pages], text = name)

        if finish:
            progress.finish()
        self.unsave()

        self.draw_pages()
        self.locker.close_function(self.import_file)

    def new_userForm(self, event = None):
        if self.locker.open_function(self.new_userForm, event): return
        self.locker.aload(self.aide_doc, False)

        u = UserFormGenerator(self.master, 'Nouveau UserForm', '')
        code = u.show()
        self.USERFORMS['untitled.uf'] = code
        self.locker.close_function(self.new_userForm)

    def print_files(self, event = None):
        if self.locker.open_function(self.print_files): return

        ps = PrintSettings(self.master, '')
        ps.show()

        self.locker.close_function(self.print_files)

    def show_infos(self, evt = None):
        if self.locker.open_function(self.show_infos): return

        files = {}
        e = False
        for x in self.tree_files.selection():
            fp = self.tree_files.item(x)['text']
            file_info = self.file_infos[fp].copy()
            files[fp] = file_info
            e = True

        if e:
            ish = InfosShower(self.master, files)
            ish.show()

        self.locker.close_function(self.show_infos)

if __name__ == '__main__':
    from test import *
    e = Tester()
