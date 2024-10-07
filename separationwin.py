from tkinter import *
from tkinter import ttk
from tkinter.ttk import *
from tkinter.messagebox import *
import openpyxl as xl

class SeparationWin:
    def __init__(self, parent, csv):
        self.file = csv
        self.liste = []

        self.master = Toplevel(parent)
        self.master.transient(parent)
        self.master.title('Traitement de la liste')
        self.master.rowconfigure(0, weight = 1)
        self.master.columnconfigure(1, weight = 3)
        self.master.columnconfigure(3, weight = 3)

        scroll1 = ttk.Scrollbar(self.master, orient = 'vertical')
        scroll1.grid(row = 0, column = 2, sticky = 'ns')

        frame_radio = ttk.Frame(self.master)
        frame_radio.grid(row = 0, column = 0, sticky = 'nswe')
        frame_radio.columnconfigure(0, weight = 1)

        self.text = Text(self.master, width = 40, yscrollcommand = scroll1.set)
        self.text.grid(row = 0, column = 1, sticky = 'nswe')

        frame_list = ttk.Frame(self.master)
        frame_list.grid(row = 0, column = 3, sticky = 'nswe')
        frame_list.rowconfigure(0, weight = 1)
        frame_list.rowconfigure(1, weight = 1)
        frame_list.rowconfigure(2, weight = 1)
        frame_list.columnconfigure(0, weight = 1)

        self.tree_file = Listbox(frame_list, selectmode = None, width = 30)
        self.tree_file.grid(row = 0, column = 0, sticky = 'nswe')
        self.tree_rev = Listbox(frame_list, selectmode = None, width = 30)
        self.tree_rev.grid(row = 1, column = 0, sticky = 'nswe')
        self.tree_pag = Listbox(frame_list, selectmode = None, width = 30)
        self.tree_pag.grid(row = 2, column = 0, sticky = 'nswe')

        self.use_invert = IntVar(value = 1)
        self.use_pages = IntVar(value = 1)
        self.use_invert.trace('w', lambda *args: self.update())
        self.use_pages.trace('w', lambda *args: self.update())

        label_col = ttk.Label(frame_radio, text = 'Sépératateur des colonnes')
        label_col.grid(row = 0, column = 0, padx = 5, pady = 5, sticky = 'w')
        label_row = ttk.Label(frame_radio, text = 'Sépératateur des lignes')
        label_row.grid(row = 2, column = 0, padx = 5, pady = 5, sticky = 'w')
        label_keep_file = ttk.Label(frame_radio, text = 'Colonne fichier')
        label_keep_file.grid(row = 4, column = 0, padx = 5, pady = 5, sticky = 'w')
        label_keep_rev = ttk.Checkbutton(frame_radio, text = 'Colonne inverser', onvalue = 1, offvalue = 0, variable = self.use_invert)
        label_keep_rev.grid(row = 6, column = 0, padx = 5, pady = 5, sticky = 'w')
        label_keep_pag = ttk.Checkbutton(frame_radio, text = 'Colonne pages', onvalue = 1, offvalue = 0, variable = self.use_pages)
        label_keep_pag.grid(row = 8, column = 0, padx = 5, pady = 5, sticky = 'w')
        label_first = ttk.Label(frame_radio, text = 'Première ligne')
        label_first.grid(row = 10, column = 0, padx = 5, pady = 5, sticky = 'w')

        self.split_col = StringVar(value = ';')
        self.split_row = StringVar(value = '¶')
        self.split_col.trace('w', lambda *args: self.update())
        self.split_row.trace('w', lambda *args: self.update())
        spliter_col = ttk.Entry(frame_radio, textvariable = self.split_col)
        spliter_col.grid(row = 1, column = 0, padx = 5, pady = 5, sticky = 'we')
        spliter_row = ttk.Entry(frame_radio, textvariable = self.split_row)
        spliter_row.grid(row = 3, column = 0, padx = 5, pady = 5, sticky = 'we')
        self.keep_file = ttk.Spinbox(frame_radio, from_ = 1, to = 999, command = self.update)
        self.keep_file.grid(row = 5, column = 0, padx = 5, pady = 5, sticky = 'we')
        self.keep_file.set(1)
        self.keep_rev = ttk.Spinbox(frame_radio, from_ = 1, to = 999, command = self.update)
        self.keep_rev.grid(row = 7, column = 0, padx = 5, pady = 5, sticky = 'we')
        self.keep_rev.set(2)
        self.keep_pag = ttk.Spinbox(frame_radio, from_ = 1, to = 999, command = self.update)
        self.keep_pag.grid(row = 9, column = 0, padx = 5, pady = 5, sticky = 'we')
        self.keep_pag.set(3)
        self.first_line = ttk.Spinbox(frame_radio, from_ = 1, to = 999, command = self.update)
        self.first_line.grid(row = 11, column = 0, padx = 5, pady = 5, sticky = 'we')
        self.first_line.set(1)

        btn = ttk.Button(self.master, text = 'Importer ces fichiers', command = self.validate)
        btn.grid(row = 1, column = 0, columnspan = 5, padx = 10, pady = 10, sticky = 'we')

        self.data = self.insertData()

    def insertData(self):
        n = 0
        digit = ''
        while self.file[-n] != '.':
            n += 1
            digit = self.file[-n] + digit

        if digit == '.csv':
            f = open(self.file, 'r', encoding = 'utf-8')
            r = f.read()
            r = r.replace('\n\n', '')
            f.close()
        elif digit in ('.xlsx', '.xlsm'):
            wb = xl.load_workbook(self.file, read_only = True)
            sh = wb.active
            r = ''
            for row in sh.values:
                if None in row:
                    continue
                for value in row:
                    r += str(value) + ';'
                r = r[:-1]
                r = r + '\n'

            wb.close()
        else:
            return False

        self.content = r.replace('\n', '¶')
        r = r.replace('\n', '¶\n')
        self.text.insert('end', r)
        self.text.config(stat = 'disabled')
        self.update()

        return True

    def clear(self):
        self.tree_file.delete(0, 'end')
        self.tree_rev.delete(0, 'end')
        self.tree_pag.delete(0, 'end')

    def validate(self):
        liste_file = list(self.tree_file.get(0, 'end'))
        liste_invt = list(self.tree_rev.get(0, 'end'))
        liste_page = list(self.tree_pag.get(0, 'end'))
        self.liste = []
        for i in range(len(liste_file)):
            if not liste_file[i]:
                continue

            self.liste.append({'file': liste_file[i]})
            if self.use_invert.get():
                self.liste[-1]['reverse'] = liste_invt[i]
            if self.use_pages.get():
                self.liste[-1]['pages'] = liste_page[i]
            
        self.master.destroy()

    def update(self):
        if self.keep_file.get() == '' or self.split_row.get() == '' or self.split_col.get() == '':
            return

        self.clear()
        lignes = self.content.split(self.split_row.get())
        index_file = self.keep_file.get()
        index_rev = self.keep_rev.get()
        index_pag = self.keep_pag.get()
        try:
            index_file = int(index_file)-1
            index_rev = int(index_rev)-1
            index_pag = int(index_pag)-1
        except:
            return

        line_output = []
        for i in range(len(lignes)):
            if i < int(self.first_line.get())-1:
                continue

            ln = lignes[i].split(self.split_col.get())
            line_output.append({})
            if index_file >= len(ln):
                return
            else:
                line_output[-1]['file'] = ln[index_file]

            if index_rev >= len(ln):
                pass
            else:
                line_output[-1]['revs'] = ln[index_rev]
            if index_pag >= len(ln):
                pass
            else:
                line_output[-1]['page'] = ln[index_pag]

        for line in line_output:
            self.tree_file.insert('end', line['file'])
            if 'revs' in list(line.keys()) and self.use_invert.get():
                self.tree_rev.insert('end', line['revs'])
            if 'page' in list(line.keys()) and self.use_pages.get():
                self.tree_pag.insert('end', line['page'])

    def launch(self):
        if not self.data:
            showerror('Fichier', "Ce format de fichier n'est pas compatible ou obsolète. Assurez vous d'ouvrir un fichier .csv ou .xlsx (ou .xlsm). Les versions précédentes de Excel ne sont pas prise en charge")
            self.master.destroy()
            return self.liste

        self.master.wait_window()
        return self.liste

if __name__ == '__main__':
    root = Tk()
    s = SeparationWin(root, 'liste.xlsx')
    print(s.launch())
    root.mainloop()
