from tkinter import *
from tkinter import ttk
from tkinter.ttk import *
from tkinter.messagebox import *
from tkinter.filedialog import *
from PIL import Image, ImageTk
import os
import time

from confr import *


class HTML(Frame):
    CMD_URL = 'start'
    css = {'default': [False, {'font': ('Courier', 10)}],
           'bold': [False, {'font': ('Courier', 10, 'bold')}],
           'italic': [False, {'font': ('Courier', 10, 'italic')}],
           'underline': [False, {'font': ('Courier', 10, 'underline')}],
           'center': [False, {'font': ('Courier', 10), 'justify': 'center'}],
           'link': [False, {'foreground': 'blue', 'font': ('Courier', 10, 'underline')}],}

    def __init__(self, parent, view, *args, **kwargs):
        super().__init__(parent)
        super().columnconfigure(2, weight = 9)
        super().rowconfigure(0, weight = 1)
        view = view.lower()
        if view.count('.') == 1:
            self.view, use_scroll = view.split('.')
            smp = ''
        elif view.count('.') == 2:
            self.view, use_scroll, smp = view.split('.')

        use_scroll = True if use_scroll == 'scroll' else False
        self.summup = 'summ' in smp

        if self.view == 'table':
            super().columnconfigure(0, weight = 1)
            self.tree = ttk.Treeview(self, selectmode = 'browse', columns = ('#1', '#2'))
            self.tree['displaycolumns'] = ()
            self.tree.grid(row = 0, column = 0, sticky = 'nswe')
            self.tree.bind('<<TreeviewSelect>>', self.move_to)
            if use_scroll:
                self.scroll = ttk.Scrollbar(self, orient = 'vertical')
                self.scroll.grid(row = 0, column = 1, sticky = 'ns')
                self.scroll.config(command = self.tree.yview)
                self.tree.config(yscrollcommand = self.scroll.set)

        self.text = Text(self, wrap = 'word', *args, **kwargs)
        self.text.grid(row = 0, column = 2, sticky = 'nswe')
        self.text.bind('<Button-1>', self.remove_tag_moved)

        if use_scroll:
            self.scrolly = ttk.Scrollbar(self, orient = 'vertical')
            self.scrolly.grid(row = 0, column = 3, sticky = 'ns')
            self.scrolly.config(command = self.text.yview)
            self.text.config(yscrollcommand = self.scrolly.set)

    def remove_tag_moved(self, evt):
        self.text.tag_delete('moved')

    def move_to(self, evt, selection = None):
        if not selection:
            selection = self.tree.selection()
        else:
            self.tree.selection_set(selection)
            return

        self.remove_tag_moved(evt)
        for s in selection:
            item = self.tree.item(s)
            from_ = item['values'][0]
            to = item['values'][1]
            self.text.see(from_)
            self.text.tag_add('moved', from_, to)
        self.text.tag_configure('moved', background = 'yellow')

    def clear(self):
        self.text.config(stat = 'normal')
        for t in self.text.tag_names():
            self.text.tag_delete(t)
        self.text.delete('0.0', 'end')
        if self.view == 'table':
            for i in self.tree.get_children():
                self.tree.delete(i)

    def add_content(self, html):
        self.clear()
        self.text.config(stat = 'normal')
        tm = '''<p></p><p></p><p><h1>Table des matières</h1></p><p></p>'''
        html = html.replace('\n', '')
        html = html.replace('\r', '')
        index = 0
        if self.summup:
            html = html + tm
            index = html.index(tm)

        self.paras = []
        self.styles = []
        in_styles = []
        self.images = []
        buffer = ''
        iid = 0
        ligne = 0
        notin_table = True
        cnts = []
        for c in self.css:
            if c[0]:
                cnts.append(0)

        i = -1
        while i <= len(html)-1:
            if i >= index:
                notin_table = False

            sqizz = False
            if html[iid:iid + 4] == '</p>':
                iid += 4
                self.paras.append(buffer)
                buffer = ''
            if html[iid:iid + 3] == '<p>':
                iid += 2
                ligne += 1
                sqizz = True

            if html[iid:iid+4] == '<br>':
                iid += 4
                self.paras.append(buffer)
                buffer = ''
                ligne += 1

            if html[iid:iid + 2] == '<h':
                to = iid + 2
                while html[to] != '>':
                    to += 1
                in_styles.append({'from': str(ligne) + '.' + str(len(buffer)), 'to': None, 'style': html[iid+2:to], 'ligne': ligne, 'iid_dep': to+1, 'iid_end': None, 'content': ''})
                iid = to + 1
            elif html[iid:iid + 3] == '</h':
                to = iid + 3
                while html[to] != '>':
                    to += 1
                in_styles[-1]['to'] = str(ligne) + '.' + str(len(buffer))
                in_styles[-1]['iid_end'] = iid
                in_styles[-1]['print'] = notin_table
                in_styles[-1]['content'] = html[in_styles[-1]['iid_dep']:in_styles[-1]['iid_end']]
                sty = in_styles[-1]['style']
                if notin_table and self.css[sty][0]:
                    n = int(sty)-1
                    cnts[n] += 1
                    vnb = cnts[:n+1]
                    for j in range(n+1, len(cnts)):
                        cnts[j] = 0
                    r = '.'.join([str(j) for j in vnb])
                    html += '<p>{0}{1} <a href="this.{2}">{2}</a></p>'.format(' ' * n * 6, r, in_styles[-1]['content'], in_styles[-1]['content'])

                self.styles.append(in_styles.pop(-1))
                iid = to
                sqizz = True

            if html[iid:iid + 2] == '<a':
                to = iid + 2
                while html[to] != '>':
                    to += 1
                to += 1
                balise = html[iid:to]
                j = 0
                while balise[j] != '"':
                    j += 1
                k = j+1
                while balise[k] != '"':
                    k += 1
                link = balise[j+1:k]
                iid = to
                in_styles.append({'from': str(ligne) + '.' + str(len(buffer)), 'to': None, 'style': 'link', 'ligne': ligne, 'iid_dep': iid, 'iid_end': None, 'content': link})

            if html[iid:iid+3] == '</a':
                in_styles[-1]['to'] = str(ligne) + '.' + str(len(buffer))
                in_styles[-1]['iid_end'] = iid
                in_styles[-1]['print'] = True
                self.styles.append(in_styles.pop(-1))
                iid += 3
                sqizz = True

            if html[iid:iid+6] == '<image':
                ## Format de l'image :
                ## <image href="./fichier.png" size="WIDTHxHEIGHT">
                to = iid+1
                while html[to] != '>':
                    to += 1
                para = html[iid+7:to]
                para = para.split('"')
                infos = {'href': None, 'size': [30, 30], 'anchor': 'center'}
                for i in range(int(len(para)/2)):
                    para[2*i] = para[2*i].replace(' ', '')
                    para[2*i] = para[2*i].replace('=', '')
                    if 'x' in para[2*i+1]:
                        para[2*i+1] = list(map(int, para[2*i+1].split('x')))
                    infos[para[2*i]] = para[2*i+1]

                self.images.append({'index': str(ligne) + '.' + str(len(buffer)), 'file': infos['href'], 'size': infos['size'], 'anchor': infos['anchor']})
                iid = to
                sqizz = True

            if html[iid:iid+2] == '<b':
                iid += 2
                in_styles.append({'from': str(ligne) + '.' + str(len(buffer)), 'to': None, 'style': 'bold', 'ligne': ligne, 'iid_dep': iid, 'iid_end': None, 'content': ''})
                sqizz = True

            if html[iid:iid+3] == '</b':
                in_styles[-1]['to'] = str(ligne) + '.' + str(len(buffer))
                in_styles[-1]['iid_end'] = len(buffer)
                in_styles[-1]['content'] = html[in_styles[-1]['iid_dep']:in_styles[-1]['iid_end']]
                in_styles[-1]['print'] = True
                self.styles.append(in_styles.pop(-1))
                iid += 3
                sqizz = True

            if html[iid:iid+2] == '<i':
                iid += 2
                in_styles.append({'from': str(ligne) + '.' + str(len(buffer)), 'to': None, 'style': 'italic', 'ligne': ligne, 'iid_dep': iid, 'iid_end': None, 'content': ''})
                sqizz = True

            if html[iid:iid+3] == '</i':
                in_styles[-1]['to'] = str(ligne) + '.' + str(len(buffer))
                in_styles[-1]['iid_end'] = len(buffer)
                in_styles[-1]['content'] = html[in_styles[-1]['iid_dep']:in_styles[-1]['iid_end']]
                in_styles[-1]['print'] = True
                self.styles.append(in_styles.pop(-1))
                iid += 3
                sqizz = True

            if html[iid:iid+2] == '<u':
                iid += 2
                in_styles.append({'from': str(ligne) + '.' + str(len(buffer)), 'to': None, 'style': 'underline', 'ligne': ligne, 'iid_dep': iid, 'iid_end': None, 'content': ''})
                sqizz = True

            if html[iid:iid+3] == '</u':
                in_styles[-1]['to'] = str(ligne) + '.' + str(len(buffer))
                in_styles[-1]['iid_end'] = len(buffer)
                in_styles[-1]['content'] = html[in_styles[-1]['iid_dep']:in_styles[-1]['iid_end']]
                in_styles[-1]['print'] = True
                self.styles.append(in_styles.pop(-1))
                iid += 3
                sqizz = True

            if html[iid:iid+7] == '<center':
                iid += 7
                in_styles.append({'from': str(ligne) + '.' + str(len(buffer)), 'to': None, 'style': 'center', 'ligne': ligne, 'iid_dep': iid, 'iid_end': None, 'content': ''})
                sqizz = True

            if html[iid:iid+8] == '</center':
                in_styles[-1]['to'] = str(ligne) + '.' + str(len(buffer))
                in_styles[-1]['iid_end'] = len(buffer)
                in_styles[-1]['content'] = html[in_styles[-1]['iid_dep']:in_styles[-1]['iid_end']]
                in_styles[-1]['print'] = True
                self.styles.append(in_styles.pop(-1))
                iid += 8
                sqizz = True

            if iid >= len(html):
                break

            if not sqizz:
                buffer += html[iid]
            iid += 1

        self.text.insert('end', '\n'.join(self.paras))
        for i in range(len(self.images)):
            self.images[i]['PIL'] = Image.open(self.images[i]['file'])
            self.images[i]['PIL'] = self.images[i]['PIL'].resize(self.images[i]['size'])
            self.images[i]['tk'] = ImageTk.PhotoImage(self.images[i]['PIL'])
            self.text.image_create(self.images[i]['index'], image = self.images[i]['tk'])

        for style in self.styles:
            self.text.tag_add(style['style'], style['from'], style['to'])

        self.config_styles()
        self.update_tree()
        self.text.config(stat = 'disabled')

    def load_css(self, file = None, content = None):
        if file != None and content == None:
            f = open(file, 'r', encoding = 'utf-8')
            r = f.read()
            f.close()
        elif file == None and content != None:
            r = content
        else:
            return

        fonts = {}
        css = self.css.copy()
        dest = None

        for line in r.split('\n'):
            if not line:
                continue

            if line == '##FONTS':
                dest = 'fonts'
                continue
            if line == '##STYLES':
                dest = 'styles'
                continue

            if dest == 'fonts':
                name, args = line.split(': ')
                args = args.split(', ')
                args[1] = int(args[1])
                args = tuple(args)
                fonts[name] = args
            elif dest == 'styles':
                style, args = line.split(': ')
                args = args.split(', ')
                tree = bool(int(args.pop(0)))
                a = {}
                for arg in args:
                    name, value = arg.split('/')
                    if name != 'font':
                        a[name] = value
                    else:
                        a[name] = fonts[value]

                css[style] = [tree, a]

        self.css = css

    def config_styles(self):
        for style, data in self.css.items():
            if style == 'default':
                self.text.config(**data[1])
            else:
                self.text.tag_configure(style, **data[1])

            if data[0]:
                self.text.tag_bind(style, '<Button-1>', self.select_tree)

            if 'link' in style:
                self.text.tag_bind(style, '<Enter>', self.select_cursor)
                self.text.tag_bind(style, '<Leave>', self.unselect_cursor)
                self.text.tag_bind(style, '<Button-1>', self.open_link)

    def search_iid(self, parent, line, col):
        for iid in self.tree.get_children(parent):
            item = self.tree.item(iid)
            from_, to = item['values']
            line_from, col_from = map(int, from_.split('.'))
            line_to, col_to = map(int, to.split('.'))
            if line_from <= line <= line_to and col_from <= col <= col_to:
                return iid
            else:
                a = self.search_iid(iid, line, col)
                if a:
                    return a

    def select_tree(self, evt):
        if self.view == 'table':
            line, col = map(int, self.text.index('current').split('.'))
            parent = ''
            iid = self.search_iid(parent, line, col)
            self.tree.selection_set(iid)
            self.tree.see(iid)

    def select_cursor(self, evt):
        self.text.config(cursor = 'hand2')

    def unselect_cursor(self, evt):
        self.text.config(cursor = '')

    def open_link(self, evt):
        line, col = map(int, self.text.index('current').split('.'))
        for style in self.styles:
            line_from, col_from = map(int, style['from'].split('.'))
            line_to, col_to = map(int, style['to'].split('.'))
            if line_from <= line <= line_to and col_from <= col <= col_to and 'link' in style['style']:
                if 'this.' in style['content']:
                    dest = style['content'].split('.')
                    dest = '.'.join(dest[1:])
                    for sty in self.styles:
                        if sty['content'] == dest:
                            self.move_to(evt = None, selection = [sty['item']])
                else:
                    os.system(self.CMD_URL + ' ' + style['content'])

    def update_tree(self):
        if self.view == 'text':
            return

        parents = [{'txt': None, 'sty': '', 'item': ''}]
        for j, style in enumerate(self.styles):
            sty = style['style']
            from_ = style['from']
            to = style['to']
            aload = style['print']
            if not aload:
                continue

            txt = self.text.get(from_, to)
            show = self.css[sty][0]
            if show:
                if parents[-1]['sty'] == sty:
                    p = parents[-1]['p']
                elif parents[-1]['sty'] != sty:
                    r = None
                    for i, info in enumerate(parents):
                        if info['sty'] == sty:
                            p = info['p']
                            r = i
                    if r == None:
                        p = parents[-1]['item']
                    else:
                        for i in range(r, len(parents)):
                            parents.pop(r)
                item = self.tree.insert(p, 'end', text = txt, values = [from_, to], open = True)
                self.styles[j]['item'] = item
                parents.append({'p': p, 'sty': sty, 'item': item})


class ToolTip(object):
    id = None
    tw = None

    def __init__(self, widget, text='widget info', mode_HTML = False):
        self.relief = 'solid'
        self.borderwidth = 1
        self.justify = 'left'
        self.color = '#FFFFEA'
        self.widget = widget
        self.text = text
        self.waittime = 500 if not mode_HTML else 1000
        self.wraplength = 270
        self.mode_HTML = mode_HTML
        self.opened = False
        if not self.mode_HTML:
            self.widget.bind("<Leave>", self.leave)
        else:
            self.widget.bind("<Leave>", self.wait_leave)
        self.widget.bind("<ButtonPress>", self.leave)
        self.widget.bind("<Enter>", self.enter)

    def enter(self, event=None):
        self.schedule()

    def leave(self, event=None):
        self.unschedule()
        self.hidetip()

    def wait_leave(self, event = None):
        if not self.opened:
            self.leave()
            return
        self.widget.after(self.waittime, self.wait_leave)

    def schedule(self):
        self.unschedule()
        self.id = self.widget.after(self.waittime, self.showtip)

    def unschedule(self):
        id = self.id
        self.id = None
        if id:
            self.widget.after_cancel(id)

    def showtip(self, event=None):
        if self.opened:
            return
        self.opened = True
        x = y = 0
        x, y, cx, cy = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 20
        self.tw = Toplevel(self.widget)
        self.tw.wm_overrideredirect(True)
        self.tw.wm_geometry("+%d+%d" % (x, y))
        if not self.mode_HTML:
            label = Label(self.tw, text=self.text, justify=self.justify, background=self.color, relief=self.relief, borderwidth=self.borderwidth, wraplength = self.wraplength)
            label.pack(ipadx=1)
        else:
            label = HTML(self.tw, view = 'noscroll.notable', background=self.color, relief=self.relief, borderwidth=self.borderwidth, width = int(self.wraplength/12), height = int(len(self.text)/int(self.wraplength/12)))
            label.pack(ipadx=1)
            label.add_content(self.text)
            self.tw.bind('<Leave>', self.sortir)

    def sortir(self, event = None):
        self.opened = False

    def hidetip(self):
        tw = self.tw
        self.tw= None
        if tw:
            self.opened = False
            tw.destroy()

    def change(self, text):
        self.text = text

class Python: # Couleurs pour le langage python :
    colors = {'keywords1':['await', 'async', 'nonlocal', 'and', 'as', 'assert', 'break',
                         'class', 'continue', 'def', 'del', 'elif', 'else', 'except',
                         'exec', 'finally', 'for', 'from', 'global', 'if', 'import',
                         'in', 'is', 'lambda', 'not', 'or', 'pass', 'raise', 'return',
                         'try', 'while', 'with', 'yield', 'None', 'True', 'False'], # Mots clefs

              'keywords2':['open', 'isinstance', 'range', 'len', 'str', 'int', 'bool',
                         'float', 'char', 'method', 'type', 'print', 'input', 'eval',
                         'list', 'set', 'bin', 'bytes', 'exit', 'quit', 'Exception'], # Mots clefs 2
              }

    chains = {'"""': 'strings',
              "'''": "strings",
              '"': 'strings',
              "'": "strings"} # Chaines de caractères

    names = {'class': ('classname', ':'),
             'def': ('classname', '(')} # Couleurs des noms de fonctions/classes

    commentaires = {'SingleLine': ('commentaires', '#', '\n'),} # Couleurs des commentaires ('couleur', 'caractère de début', 'caractère de fin')

class Basic: # Couleurs pour le langage python :
    colors = {'keywords2':['text', 'title', 'command', 'transient', 'tooltip', 'show'], # Mots clefs des arguments
              'keywords1':['row', 'col', 'sticky', 'transient', 'column', 'rowspan', 'colspan', 'minsize', 'resize'], # Mots clefs des placement
              'keywords3': ['$BUTTON', '$LABEL', '$ENTRY', '$$MASTER'], # Mots clefs des widgets
              'keywords4': ['/EXIT', '/SAVE', '/OPENFILE', '/SAVEFILE', '/STORE', '/INSERT', '/SET', '/PUT', '/GET', '/DEL',
                            '/ArrangerDuo', '/RognerPages', '/ExtractImages', 'ExtractPages', '/SplitFile', '/OrganizePages', '/MarginFile', '/RemovePages', '/ScaleFile'], # Fonctions par défaut
              }

    chains = {}

    names = {'-': ('widget-id', '\n'),
             ':': ('arg', '\n'),
             '*': ('cmd', '\n')} # Couleurs des noms de fonctions/classes

    commentaires = {'CommandCall': ('caller', '/', '\n'),
                    'SingleLine': ('commentaires', ';', '\n'),
                    } # Couleurs des commentaires ('couleur', 'caractère de début', 'caractère de fin')

class Colorator: # Permet de retrouver les couleurs selon le langage
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'é', 'è', 'ç', 'à', '~', '#', '`', '^', '@', '$', '£', '¤', '*', 'µ', '%', 'ù', '_']
    def __init__(self, lang):
        if lang == 'python':
            self.lang = Python
        elif lang == 'basic':
            self.lang = Basic

    def get_colors(self):
        return self.lang.colors

    def get_strings(self):
        return self.lang.chains

    def get_names(self):
        return self.lang.names

    def get_comm(self):
        return self.lang.commentaires

class ProgramText(Frame):
    def __init__(self, parent, data = '', lang = 'python', *args, **kwargs):
        super().__init__(parent)
        super().columnconfigure(1, weight = 1)
        super().rowconfigure(0, weight = 1)
        self.wrap = 'none'
        self.old_i = None

        self.scrolly = ttk.Scrollbar(self, orient = 'vertical')
        self.scrolly.grid(row = 0, column = 2, sticky = 'ns')
        self.scrollx = ttk.Scrollbar(self, orient = 'horizontal')
        self.scrollx.grid(row = 1, column = 1, sticky = 'we')
        self.text = Text(self, yscrollcommand = self.scroll_y, xscrollcommand = self.scrollx.set, wrap = 'none', *args, **kwargs)
        self.text.grid(row = 0, column = 1, sticky = 'nswe')
        self.scrolly.config(command = self.move_y)
        self.scrollx.config(command = self.text.xview)
        self.text.insert('end', data)
        self.btn = ttk.Button(self, text = '', command = self.switch, width = 0)
        self.btn.grid(row = 1, column = 2, sticky = 'nswe')
        self.tt = ToolTip(self.btn, text = 'Mode d\'affichage\nTout sur une seule ligne')
        self.line_numbers_canvas = Canvas(self, width = 40, bg = '#555555', highlightbackground = '#555555', highlightthickness = 0)
        self.line_numbers_canvas.grid(row = 0, column = 0, sticky = 'ns')

        self.colorator = Colorator(lang)
        if lang == 'python':
            self.s = Settings().editor_python
        elif lang == 'basic':
            self.s = Settings().editor_basic
        self.TABSIZE = int(self.s.keys['spaces'])
        self.tab = ' ' * (int(self.s.keys['spaces']))

        self.control = False
        self.text.bind('<KeyRelease>', self.keyrelease)
        self.keyrelease()

    def update_num(self):
        self.line_numbers_canvas.delete('all')
        i = self.text.index('@0,0')
        if i == self.old_i:
            return

        self.old_i = i
        self.text.update()
        fnt = self.text.cget('font')
        while True:
            dline = self.text.dlineinfo(i)
            if dline:
                y = dline[1]
                linenum = str(int(float(i.replace('.0', ''))%10000))
                self.line_numbers_canvas.create_text(1, y, anchor='nw', text=linenum, fill='#ffffff', font=fnt)
                i = self.text.index('{0}+1line'.format(i))
            else:
                break

    def scroll_y(self, *args, **kwargs):
        self.scrolly.set(*args, **kwargs)
        self.update_num()

    def move_y(self, *args, **kwargs):
        self.text.yview(*args, **kwargs)
        self.update_num()

    def switch(self):
        if self.wrap == 'none':
            self.wrap = 'word'
            self.text.config(wrap = 'word')
            self.tt.change(text = 'Mode d\'affichage\nDécoupage au mot')
        elif self.wrap == 'word':
            self.wrap = 'char'
            self.text.config(wrap = 'char')
            self.tt.change(text = 'Mode d\'affichage\nDécoupage en fin de ligne sur le caractère')
        else:
            self.wrap = 'none'
            self.text.config(wrap = 'none')
            self.tt.change(text = 'Mode d\'affichage\nTout sur une seule ligne')

    def keyrelease(self, evt = None):
        if evt != None:
            if evt.keysym == 'Return' and self.s.keys['auto_tab'] == '1':
                l, c = self.text.index('insert').split('.')
                l = int(l)
                begin_line = self.text.index(str(l-1) + '.0')
                end_line = self.text.index(str(l) + '.0')
                line = self.text.get(begin_line, end_line)
                n = 0
                while line[0] == ' ':
                    n += 1
                    line = line[1:]
                n //= self.TABSIZE

                if ':\n' in line:
                    self.text.insert('insert', self.tab * (n + 1))

                elif 'break' in line or 'continue' in line or 'return' in line:
                    self.text.insert('insert', self.tab * (n - 1))

                else:
                    self.text.insert('insert', self.tab * n)

            elif evt.keysym == 'Tab' and self.s.keys['auto_tab'] == '1':
                self.text.delete('insert-1c')
                self.text.insert('insert', self.tab)
            elif evt.keysym == 'BackSpace' and self.s.keys['auto_backspace'] == '1':
                ind = self.text.index('insert')
                n = 1
                while n != self.TABSIZE and self.text.get(ind + '-1c') == ' ':
                    self.text.delete('insert-1c')
                    ind = self.text.index('insert')
                    n += 1

        mots_reserves = self.colorator.get_colors() # Reprend les couleurs et mots
        chains = self.colorator.get_strings()
        names = self.colorator.get_names()
        comm = self.colorator.get_comm()

        for tag in self.text.tag_names(): # Supprime toutes les anciennes couleurs
            self.text.tag_delete(tag)

        for color, mots in mots_reserves.items(): # Met les mots clef en couleurs
            if color == 'keywords4':
                continue

            for mot in mots:
                start = "1.0"
                while True:
                    start = self.text.search(mot, start, END)
                    if not start:
                        break

                    end = "{0}+{1}c".format(start, len(mot))

                    prev_false = self.text.get("{}-1c".format(start)).lower() in self.colorator.letters
                    index_0 = self.text.index('{}'.format(start)) == '1.0'
                    next_false = self.text.get('{}'.format(end)) in self.colorator.letters

                    if index_0:
                        prev_false = False

                    if prev_false or next_false:
                        start = "{0}+{1}c".format(start, len(mot))
                        continue

                    self.text.tag_add(mot, start, end)
                    self.text.tag_configure(mot, foreground=self.s.getItem(color)['fg'])
                    start = end

        for gui, color in chains.items(): # Met les chaines de caractères en couleur
            start = '1.0'
            dep = start
            mode = False
            while True:
                if ' ' in gui:
                    index = self.text.search(gui[0] if not mode else gui[-1], dep, END) # Trouve les guillemets
                else:
                    index = self.text.search(gui, dep, END) # Trouve les guillemets

                if not index:
                    break # Si plus de guillemets, casse la boucle

                if not mode: # Si mode ouverture
                    start = index # Index du début du guillemet (inclu)
                    dep = '{0}+{1}c'.format(start, len(gui))
                    mode = True # Passage en mode fermeture de guillemet
                else: # Si mode fermeture
                    end = '{0}+{1}c'.format(index, len(gui))
                    self.text.tag_add(gui, start, end)
                    self.text.tag_configure(gui, foreground=self.s.getItem(color)['fg'])
                    mode = False # Repasse en mode ouverture
                    dep = '{0}+1c'.format(end) # Décalle d'index de départ de la recherche (évite while True)

        for kw, (color, close) in names.items(): # Met les noms de fonctions/classes en couleurs
            start = '1.0'
            dep = start
            mode = False
            while True:
                if not mode:
                    index = self.text.search(kw, dep, END)
                else:
                    index = self.text.search(close, dep, END)

                if not index:
                    break

                if not mode:
                    start = self.text.index('{0}+{1}c'.format(index, len(kw)))
                    dep = start
                    mode = True
                else:
                    end = index
                    self.text.tag_add('_' + kw, start, end)
                    self.text.tag_configure('_' + kw, foreground = self.s.getItem(color)['fg'])
                    dep = self.text.index('{0}+1c'.format(end))
                    mode = False

        for kw, (color, opener, closer) in comm.items():
            start = '1.0'
            dep = start
            mode = False
            while True:
                if not mode:
                    index = self.text.search(opener, dep, END)
                else:
                    index = self.text.search(closer, dep, END)

                if not index:
                    break

                if not mode:
                    start = self.text.index('{0}+{1}c'.format(index, 0))
                    dep = start
                    mode = True
                else:
                    end = index
                    self.text.tag_add('_' + kw, start, end)
                    self.text.tag_configure('_' + kw, foreground = self.s.getItem(color)['fg'])
                    dep = self.text.index('{0}+1c'.format(end))
                    mode = False

        for color, mots in mots_reserves.items(): # Met les mots clef en couleurs
            if color != 'keywords4':
                continue

            for mot in mots:
                start = "1.0"
                while True:
                    start = self.text.search(mot, start, END)
                    if not start:
                        break

                    end = "{0}+{1}c".format(start, len(mot))

                    prev_false = self.text.get("{}-1c".format(start)).lower() in self.colorator.letters
                    index_0 = self.text.index('{}'.format(start)) == '1.0'
                    next_false = self.text.get('{}'.format(end)) in self.colorator.letters

                    if index_0:
                        prev_false = False

                    if prev_false or next_false:
                        start = "{0}+{1}c".format(start, len(mot))
                        continue

                    self.text.tag_add(mot, start, end)
                    self.text.tag_configure(mot, foreground=self.s.getItem(color)['fg'])
                    start = end

        self.update_num()

    def get(self, *args, **kwargs):
        return self.text.get(*args, **kwargs)


class ComboPopup(ttk.Combobox):
    def __init__(self, parent, iid, col, cmd_begin, cmd, **kw):
        super().__init__(parent, **kw)
        self.tv = parent
        self.iid = iid
        self.col = col
        self.cmd = cmd
        self.old_text = self.tv.set(iid, col)
        self.set(self.old_text)
        cmd_begin()
        ToolTip(self, self.old_text)

        self.focus()
        self.bind("<Escape>", self.on_escape)
        self.bind("<<ComboboxSelected>>", self.new_selection)
        self.bind("<Return>", self.on_return)

    def new_selection(self, event=None):
        self.tv.set(self.iid, self.col, self.get())
        self.close(True)

    def on_return(self, event):
        self.close()

    def on_escape(self, event):
        self.tv.set(self.iid, self.col, self.old_text)
        self.close(True)

    def close(self, force = False):
        if not force:
            self.new_selection()
        self.destroy()
        for c in self.cmd:
            c()

class EntryPopup(ttk.Entry):
    def __init__(self, parent, iid, col, text, cmd_begin, cmd, **kw):
        super().__init__(parent, **kw)
        self.tv = parent
        self.iid = iid
        self.col = col
        self.cmd = cmd
        cmd_begin()

        self.insert(0, text)
        self.select_range(0, END)
        ToolTip(self, text)

        self.focus_force()
        self.bind("<Return>", self.on_return)
        self.bind("<Escape>", self.on_escape)

    def on_return(self, event):
        self.close()

    def on_escape(self, event):
        self.destroy()
        for c in self.cmd:
            c()

    def close(self):
        if self.col == '#0':
            self.tv.item(self.iid, text=self.get())
        else:
            self.tv.set(self.iid, self.col, self.get())
        self.destroy()
        for c in self.cmd:
            c()

class CellEditor:
    FAVORI_ON  = '★'
    FAVORI_OFF = '☆'

    def __init__(self, widget, actions, command = lambda: None, beg_cmd = lambda: None):
        self.widget = widget
        self.able_tooltip = IntVar(value = 1)
        self.popup_ready = False
        self.widget.bind('<Double-Button-1>', self.edit)
        self.widget.bind('<Button-1>', self.button_pressed)
        self.actions = actions
        self.command = command
        self.beg_cmd = beg_cmd

    def edit(self, event):
        if not self.able_tooltip.get():
            return

        self.popup_ready = False
        self.able_tooltip.set(0)
        rowid = self.widget.identify_row(event.y)
        column = self.widget.identify_column(event.x)
        try:
            x, y, width, height = self.widget.bbox(rowid, column)
        except:
            self.able_tooltip.set(1)
            return

        pady = height / 2

        skip = False
        for col, cmd in self.actions.items():
            if col == column:
                if cmd['type'] == 'Entry':
                    if column != '#0':
                        text = self.widget.item(rowid)['values'][int(column.replace('#', ''))-1]
                    else:
                        text = self.widget.item(rowid)['text']
                    self.entryPopup = EntryPopup(self.widget, rowid, column, text, cmd_begin = self.beg_cmd, cmd = [lambda: self.able_tooltip.set(1), self.command])
                    skip = True
                    break
                elif cmd['type'] == 'Combo':
                    self.entryPopup = ComboPopup(self.widget, rowid, column, cmd_begin = self.beg_cmd, cmd = [lambda: self.able_tooltip.set(1), self.command], values=cmd['values'])
                    skip = True
                    break

        if not skip:
            self.able_tooltip.set(1)
            self.popup_ready = False
            return

        self.entryPopup.place(x=x, y=y + pady, width=width, height=1.25 * height, anchor='w')
        self.popup_ready = True

    def button_pressed(self, evt = None):
        if self.popup_ready:
            self.entryPopup.destroy()
            self.able_tooltip.set(1)
            self.popup_ready = False
        else:
            rowid = self.widget.identify_row(evt.y)
            column = self.widget.identify_column(evt.x)
            for col, cmd in self.actions.items():
                if col == column and cmd['type'] == 'switch':
                    old = self.widget.item(rowid)['values'][int(column.replace('#', ''))-1]
                    if old == self.FAVORI_ON:
                        new = self.FAVORI_OFF
                    else:
                        new = self.FAVORI_ON

                    if column == '#0':
                        self.widget.item(rowid, text=new)
                    else:
                        self.widget.set(rowid, column, new)


if __name__ == '__main__':
    root = Tk()
    root.columnconfigure(0, weight = 1)
    root.rowconfigure(0, weight = 1)
    root.rowconfigure(1, weight = 1)
    root.geometry('700x500')
    t = ProgramText(root, lang = 'basic')
    t.text.config(font = ('Courier', 12))
    '''t.text.insert('end', """from tkinter import *\n
class App:
    def __init__(self):
        if __name__ == '__name__':
            print('Au revoir !')
        else:
            self.master = Tk()

# Ceci est un commentaire sur une seule et unique ligne !"""'''
    t.text.insert('end', """; Structure des programmes :
    
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
""")
    t.keyrelease()
    t.grid(row = 0, column = 0, sticky = 'nswe')
    h = HTML(root, view = 'table.scroll.summ')
    h.grid(row = 1, column = 0, sticky = 'nswe')
    h.load_css('./docs/style.css')

    f = open('./docs/01- index.html', 'r', encoding = 'utf-8')
    h.add_content(f.read())
    f.close()

    b = Button(root, text = 'Ceci est un petit test...')
    b.grid(row = 2, column = 0, padx = 5, pady = 5, sticky = 'nswe')
    t = ToolTip(b, text = '<p><a href="www.python.org">Bonjour</a>, <b>comment</b> allez vous ?</p><p><center>Ceci est mon texte centré !</center></p><p><u>Et celui ci est souligné !</u></p><p>Et avec une image :</p><p><image href="./images/startup.png" size="100x100"></p>', mode_HTML = True)
    b2 = Button(root, text = 'Ceci est un petit test...')
    b2.grid(row = 3, column = 0, padx = 5, pady = 5, sticky = 'nswe')
    t = ToolTip(b2, text = '<p><a href="python.org">Bonjour</a>, comment allez vous ?</p>', mode_HTML = False)

    root.mainloop()
