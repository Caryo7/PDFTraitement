from tkinter import *
from tkinter import ttk
from tkinter.ttk import *
from PyPDF2 import *

from customwidgets import *

class InfosShower:
    def __init__(self, parent, files):
        self.master = Toplevel(parent)
        self.master.transient(parent)
        self.master.title('Propriétés')
        self.master.columnconfigure(0, weight = 1)
        self.master.rowconfigure(0, weight = 1)

        self.note = ttk.Notebook(self.master)
        self.note.grid(row = 0, column = 0, padx = 10, pady = 10, sticky = 'nswe')

        for file, content in files.items():
            files[file]['_frame'] = ttk.Frame(self.note)
            files[file]['_frame'].columnconfigure(0, weight = 1)
            files[file]['_frame'].rowconfigure(0, weight = 1)
            files[file]['_scroll'] = ttk.Scrollbar(files[file]['_frame'], orient = 'vertical')
            files[file]['_scroll'].grid(row = 0, column = 1, sticky = 'ns')
            self.note.add(text = file, child = files[file]['_frame'])
            files[file]['_tree'] = ttk.Treeview(files[file]['_frame'], columns = ('#1'), selectmode = 'none', yscrollcommand = files[file]['_scroll'])
            files[file]['_tree'].grid(row = 0, column = 0, sticky = 'nswe')
            files[file]['_tree'].heading('#0', text = 'Paramètre')
            files[file]['_tree'].heading('#1', text = 'Valeur')
            files[file]['_scroll'].config(command = files[file]['_tree'].yview)

            path = content['path']
            pdf = PdfReader(path)
            meta = pdf.metadata
            files[file]['_tree'].insert('', 'end', text = 'Auteur', values = [meta.author])
            files[file]['_tree'].insert('', 'end', text = 'Créateur', values = [meta.creator])
            files[file]['_tree'].insert('', 'end', text = 'Producteur', values = [meta.producer])
            files[file]['_tree'].insert('', 'end', text = 'Sujet', values = [meta.subject])
            files[file]['_tree'].insert('', 'end', text = 'Titre', values = [meta.title])
            files[file]['_tree'].insert('', 'end', text = 'Création', values = [meta.creation_date])
            files[file]['_tree'].insert('', 'end', text = 'Dernière modification', values = [meta.modification_date])
            meta2 = pdf.xmp_metadata # https://pypdf2.readthedocs.io/en/3.0.0/modules/XmpInformation.html
            if not meta2:
                continue
            files[file]['_tree'].insert('', 'end', text = 'Contributeurs', values = [', '.join(meta2.dc_contributor)])
            files[file]['_tree'].insert('', 'end', text = 'Descrpition', values = [meta2.dc_description])
            files[file]['_tree'].insert('', 'end', text = 'Version du PDF', values = [meta2.pdf_pdfversion])
            files[file]['_tree'].insert('', 'end', text = 'Logiciel de création', values = [meta2.pdf_producer])
            files[file]['_tree'].insert('', 'end', text = 'Premier logiciel de création', values = [meta2.xmp_creator_tool])
            files[file]['_tree'].insert('', 'end', text = 'Date de création', values = [meta2.xmp_create_date])
            files[file]['_tree'].insert('', 'end', text = 'Dernier enregistrement des informations', values = [meta2.xmp_metadata_date])
            files[file]['_tree'].insert('', 'end', text = 'Version de ce PDF', values = [meta2.xmpmm_instance_id])

        clo = ttk.Button(self.master, text = 'Fermer', command = self.master.destroy)
        clo.grid(row = 1, column = 0, padx = 10, pady = 10, sticky = 'nswe')

    def show(self):
        self.master.wait_window()

if __name__ == '__main__':
    from mainwin import *
    mw = MainWindow()
    mw.open_project(path = 'test_dépliant.pdfpro')
    mw.Generate()
