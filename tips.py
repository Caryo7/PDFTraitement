from tkinter import *
from tkinter import ttk
from tkinter.ttk import *
from customwidgets import *
from pathlib import Path
import os

class TipsWin:
    def __init__(self, parent, images, title, nb, total, text, next_cmd, prev_cmd, dam_cmd):
        self.next_cmd, self.prev_cmd, self.dam_cmd = next_cmd, prev_cmd, dam_cmd
        self.total = total

        self.root = Toplevel(parent)
        self.root.transient(parent)
        self.root.protocol('WM_DELETE_WINDOW', self.destroy)
        self.root.iconbitmap(images.ICONS['Tips'])
        self.root.columnconfigure(3, weight=1)
        self.root.rowconfigure(1, weight = 1)

        self.root.title(str(nb+1) + '/' + str(self.total) + ' ' + title)

        self.next_img = images.Right.medium
        self.close_img = images.Close.medium
        self.prev_img = images.Left.medium

        lb_ico = ttk.Label(self.root, image = images.Astuces.big, text = '')
        lb_ico.grid(row = 0, column = 4, padx = 3, pady = 3, sticky = 'nswe')

        self.label = HTML(self.root, view = 'notable.noscroll', width = 30, height = 7)
        self.label.grid(row = 1, column = 0, padx = 3, pady = 5, columnspan = 5, sticky = 'nswe')
        #self.label.load_css('')
        self.label.add_content(text)
        b1 = ttk.Button(self.root, image = self.next_img, command = self.up)
        b1.grid(row = 0, column = 1, padx = 3, pady = 3, sticky = 'nswe')
        b3 = ttk.Button(self.root, image = self.prev_img, command = self.down)
        b3.grid(row = 0, column = 0, padx = 3, pady = 3, sticky = 'nswe')
        b2 = ttk.Button(self.root, image = self.close_img, command = self.destroy)
        b2.grid(row = 0, column = 2, padx = 3, pady = 3, sticky = 'nswe')
        ToolTip(b1, text = 'Conseil suivant')
        ToolTip(b2, text = 'Fermer')
        ToolTip(b3, text = 'Conseil précédent')

        self.print_tips = IntVar(value = 0)
        b4 = ttk.Checkbutton(self.root, text = 'Ne plus afficher', onvalue = 1, offvalue = 0, variable = self.print_tips)
        b4.grid(row = 2, column = 0, columnspan = 5, padx = 5, pady = 5, sticky = 'nswe')
        ToolTip(b4, text = 'Ne plus afficher les conseils aux démarrages.\nCette option peut être changée dans le menu Edition -> Préférence -> Générales -> Conseils au démarrage')

    def up(self):
        self.next_cmd()

    def down(self):
        self.prev_cmd()

    def destroy(self):
        if not self.print_tips.get():
            self.dam_cmd()
        self.root.destroy()

    def change(self, value, title, nb):
        self.label.add_content(value)
        self.root.title(str(nb+1) + '/' + str(self.total) + ' ' + title)


class JSon:
    def __init__(self, path, encoding = 'utf-8'):
        self.file = open(path, mode = 'r', encoding = encoding)
        self.data = json.load(self.file)

    def close(self):
        self.file.close()

    def tips_list(self):
        return list(self.data.keys())

    def infos(self, name):
        return self.data[name]


def OpenTips():
    advices = []
    p = Path('./tips/')
    for f in list(p.glob('**/*.html')):
        fp = open(f, 'r', encoding = 'utf-8')
        r = fp.read()
        fp.close()
        name = str(f).replace('.html', '')
        while name[0] != '-':
            name = name[1:]
        advices.append([name, r])

    return advices


class Tips:
    tips_index = 0
    def __init__(self, master, images, pm):
        self.master = master
        self.images = images
        self.pm = pm

    def start_tips(self):
        self.advices = OpenTips()

        if self.pm.general.general['tips'] == '0':
            return

        self.start_tips_index(0)

    def start_tips_index(self, index):
        title, text = self.advices[index]
        nb = self.tips_index
        next_cmd = lambda: self.next_tip()
        prev_cmd = lambda: self.prev_tip()
        dam_cmd = lambda: self.donotaskagain_tip()

        self.tip_window = TipsWin(self.master, self.images, title, index, len(self.advices), text, next_cmd, prev_cmd, dam_cmd)

    def tip_update(self, index):
        title, text = self.advices[index]
        self.tip_window.change(text, title, index)

    def next_tip(self):
        self.tips_index += 1
        self.tips_index %= len(self.advices)
        self.tip_update(self.tips_index)

    def prev_tip(self):
        if self.tips_index < 0:
            self.tips_index = len(self.advices) - 1

        self.tips_index -= 1
        self.tip_update(self.tips_index)

    def donotaskagain_tip(self):
        self.pm.general.set('general', 'tips', '0')
        self.pm.reload_updates()

if __name__ == '__main__':
    from test import *
    e = Tester(['tips'])
