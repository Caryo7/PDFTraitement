from tkinter import *
from tkinter import ttk
from tkinter.ttk import *
from tkinter.messagebox import *
from PyPDF2 import PdfReader

class ShowText:
    def __init__(self, parent, text, page, index, l):
        self.master = Toplevel(parent)
        self.master.title('Position du résultat - Page ' + str(page))
        self.master.columnconfigure(0, weight = 1)
        self.master.rowconfigure(0, weight = 1)

        scroll = ttk.Scrollbar(self.master, orient = 'vertical')
        scroll.grid(row = 0, column = 1, sticky = 'ns')
        self.txt = Text(self.master, width = 60, height = 20, yscrollcommand = scroll.set)
        scroll.config(command = self.txt.yview)
        self.txt.grid(row = 0, column = 0, sticky = 'nswe')

        lng = 0
        lines = text.split('\n')
        for i in range(len(lines)):
            self.txt.insert('end', lines[i] + '\n')
            if index >= lng and index <= lng + len(lines[i]):
                line = i + 1
                col_from = index - lng
                col_to = index - lng + l
                from_ = str(line) + '.' + str(col_from)
                to = str(line) + '.' + str(col_to)
                self.txt.tag_add('color', from_, to)

            lng += len(lines[i]) + 1
        self.txt.tag_configure('color', foreground = 'red')
        self.txt.see(from_)
        self.txt.tag_add(SEL, from_, to)
        self.txt.mark_set(INSERT, from_)
        self.txt.focus()

    def show(self):
        self.master.wait_window()

class SearchWin:
    AUTO_OPEN = False

    def __init__(self, parent, file, Imager):
        self.parent = parent
        self.file = file
        self.pdf = PdfReader(self.file)
        self.pages = self.pdf.pages
        pos = 6
        self.opened = False
        l = 10

        self.master = Toplevel(parent)
        self.master.iconbitmap(Imager.ICONS['Search'])
        self.master.transient(parent)
        self.master.title('Rechercher')
        self.master.columnconfigure(0, weight = 1)
        self.master.rowconfigure(l, weight = 1)
        self.master.minsize(600, 400)

        title = ttk.Label(self.master, text = 'Recherche dans le fichier', style = 'Title.TLabel')
        title.grid(row = 0, column = 0, padx = 10, pady = 10, sticky = 'w', columnspan = 2)

        self.kws = Text(self.master, height = 3, width = 30, wrap = 'word')
        self.kws.grid(row = 1, rowspan = l-1, column = 0, padx = 5, pady = 5, sticky = 'nswe')

        btn = ttk.Button(self.master, text = 'Rechercher', command = self.search)
        btn.grid(row = pos, column = 1, padx = 5, pady = 5, sticky = 'nswe')

        opt_or = ttk.Label(self.master, text = 'La recherche marche sur un des mots clef au moins\nSéparez les par un retour à la ligne')
        opt_or.grid(row = 1, column = 1, padx = 5, pady = 5, sticky = 'w')

        self.orient = StringVar(value = 'horizontal')
        opt_or = ttk.Radiobutton(self.master, text = 'Seulement les textes horizontal', value = 'horizontal', variable = self.orient)
        opt_or.grid(row = 2, column = 1, padx = 5, pady = 5, sticky = 'w')

        opt_and = ttk.Radiobutton(self.master, text = 'Toutes les orientations', value = 'all', variable = self.orient)
        opt_and.grid(row = 3, column = 1, padx = 5, pady = 5, sticky = 'w')

        self.cass = IntVar(value = 0)
        cas_box = ttk.Checkbutton(self.master, text = 'Respecter la casse', onvalue = 1, offvalue = 0, variable = self.cass)
        cas_box.grid(row = 4, column = 1, padx = 5, pady = 5, sticky = 'w')

        frame = ttk.Frame(self.master)
        frame.grid(row = l, column = 0, columnspan = 2, padx = 5, pady = 5, sticky = 'nswe')
        frame.columnconfigure(0, weight = 1)
        frame.rowconfigure(0, weight = 1)

        scroll = ttk.Scrollbar(frame, orient = 'vertical')
        scroll.grid(row = 0, column = 1, sticky = 'ns')

        self.tree = ttk.Treeview(frame, columns = ('#1', '#2', '#3'), selectmode = 'browse', height = 7, yscrollcommand = scroll.set)
        scroll.config(command = self.tree.yview)
        self.tree.grid(row = 0, column = 0, sticky = 'nswe')
        self.tree.heading('#0', text = 'Page')
        self.tree.heading('#1', text = 'Résultats')
        self.tree.heading('#3', text = 'Mot clef')
        self.tree['displaycolumns'] = ('#1', '#3')
        self.tree.column('#1', width = 390)
        self.tree.column('#0', width = 100)
        self.tree.bind('<Double-Button-1>', self.show)

    def show(self, evt = None):
        if self.opened:
            return

        self.opened = True
        selection = self.tree.selection()
        orientation = (0, 90, 180, 270) if self.orient.get() == 'all' else (0)
        for s in selection:
            item = self.tree.item(s)
            page_id = int(item['text'].replace('Page ', '')) - 1
            page = self.pages[page_id]
            txt = page.extract_text(orientation)
            extrait, i, kw = item['values']
            if kw == '':
                continue

            show = ShowText(self.parent, txt, page_id + 1, i, len(kw))
            show.show()
            self.kws.focus()

        self.opened = False

    def compare_text(self, page, text, kwo):
        txt = text
        kw = kwo
        if not self.cass.get():
            text = text.lower()
            kwo = kwo.lower()

        r = []
        i = 0
        while i < len(text):
            if text[i: i+len(kwo)] == kwo:
                if i - 10 < 0:
                    fr = 0
                else:
                    fr = i - 10

                extrait = txt[fr:i+len(kwo)+20]
                r.append([page, extrait, i, kw])

                i += len(kwo)
            else:
                i += 1

        return r

    def clear(self):
        for x in self.tree.get_children():
            self.tree.delete(x)

    def search(self):
        self.clear()
        keywords = self.kws.get('0.0', 'end')
        keywords = keywords.replace('\r', '')
        keywords = keywords.split('\n')
        results = False
        self.tree.config(selectmode = 'browse')
        if not ''.join(keywords):
            return

        orientation = (0, 90, 180, 270) if self.orient.get() == 'all' else (0)
        for i, page in enumerate(self.pages):
            text = page.extract_text(orientation)
            rs = []
            for keyword in keywords:
                if not keyword:
                    continue

                rs += self.compare_text(i+1, text, keyword)

            if rs:
                parent = self.tree.insert('', 'end', text = 'Page ' + str(i+1), values = [str(len(rs)) + ' résultats', '', ''], open = self.AUTO_OPEN)
            else:
                continue

            for result in rs:
                t = result[1]
                t = t.replace('\n', '')
                t = t.replace('\r', '')
                self.tree.insert(parent, 'end', text = 'Page ' + str(i+1), values = [t, result[2], result[3]])
                results = True

        if not results:
            self.tree.insert('', 'end', text = '', values = ['Aucun résultats !'])
            self.tree.config(selectmode = 'none')

    def Generate(self):
        self.kws.focus()
        self.master.wait_window()

if __name__ == '__main__':
    from test import *
    e = Tester(['show_search'])
