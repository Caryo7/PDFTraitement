from tkinter import *
from tkinter import ttk
from tkinter.messagebox import *
from tkinter.filedialog import *
from tkinter.simpledialog import *
import os

from pagecount import *
from extract import *

class PageFunctions:
    def open_file(self):
        if self.locker.open_function(self.open_file): return
        iids = self.tree_files.selection()
        for iid in iids:
            file = self.tree_files.item(iid)['text']
            path = str(self.file_infos[file]['path'])
            os.popen(path)
        self.locker.close_function(self.open_file)

    def remove(self, evt, mode):
        if self.locker.open_function(self.remove): return
        if mode == 'this':
            pages = [evt.widget.cget('text')]
        elif mode == 'selected':
            pages = []
            for label in self.names_pages:
                if label.cget('text')[0] == self.CASE_ON:
                    pages.append(label.cget('text'))

        perfile = {}
        for p in pages:
            page = p[2:]
            file, page = page.split(' - Page ')
            page = int(page) - 1
            path = self.file_infos[file]['path']
            if file not in perfile:
                perfile[file] = [page]
            else:
                perfile[file].append(page)

        for file, todel in perfile.items():
            for x in self.tree_files.get_children():
                item = self.tree_files.item(x)
                if item['text'] == file:
                    _, _, reverse, utils = self.tree_files.item(x)['values'] # Ligne du tableau
                    if reverse == 'OUI':
                        reverse = True
                    else:
                        reverse = False

                    pages_utils = getPagesNumber(utils, reverse, getCompleteList = True) # Page demandées et en nombre
                    for p in todel:
                        pages_utils.pop(p)
                    self.tree_files.set(x, '#4', getPageSet(pages_utils))

        self.update_infos()
        self.update_tree()
        self.draw_pages()
        self.unsave()
        self.locker.close_function(self.remove)

    def extract(self, evt, mode):
        if self.locker.open_function(self.extract): return
        if mode == 'this':
            pages = [evt.widget.cget('text')]
        elif mode == 'selected':
            pages = []
            for label in self.names_pages:
                if label.cget('text')[0] == self.CASE_ON:
                    pages.append(label.cget('text'))

        extraction = []
        for p in pages:
            page = p[2:]
            file, page = page.split(' - Page ')
            page = int(page) - 1
            path = self.file_infos[file]['path']
            extraction.append([path, page])

        output = self.file_unit.save_file(title = 'Enregistrer sous', initialdir = path.parent)
        if output:
            e = SimpleExtractor(extraction, output)
            for i in e.run():
                pass

            e.close()
            if self.pm.run.general['unselect'] == '1':
                self.selectall(None, False)
            if self.pm.run.general['open_forall'] == '1':
                os.popen(output)
        self.locker.close_function(self.extract)

    def next_name(self, name):
        if name[-1] == ')' and '(' in name:
            n = len(name) - 1
            while name[n] != '(':
                n -= 1
            bloc = int(name[n+1:-1])
            bloc += 1
            while bloc in self.bloc_used:
                bloc += 1
            self.bloc_used.append(bloc)
            bloc = '(' + str(bloc) + ')'
            name = name[:n] + bloc
            return name
        else:
            n = 2
            while n in self.bloc_used:
                n += 1
            self.bloc_used.append(n)
            return name + ' (' + str(n) + ')'

    def duplicate_file(self, evt = None):
        if self.locker.open_function(self.duplicate_file): return
        for x in self.tree_files.selection():
            item = self.tree_files.item(x)
            name = self.next_name(item['text'])
            self.file_infos[name] = self.file_infos[item['text']]
            self.images_list[name] = self.images_list[item['text']]

        self.update_tree()
        self.draw_pages()
        self.unsave()
        self.locker.close_function(self.duplicate_file)

    def rename_file(self, evt = None):
        if self.locker.open_function(self.rename_file): return
        for x in self.tree_files.selection():
            item = self.tree_files.item(x)
            old_name = item['text']
            new_name = askstring('Renommer', 'Nouveau nom', initialvalue = old_name)
            if (not new_name) or (new_name == old_name):
                self.locker.close_function(self.rename_file)
                return

            self.file_infos[new_name] = self.file_infos[old_name]
            del self.file_infos[old_name]
            self.images_list[new_name] = self.images_list[old_name]
            del self.images_list[old_name]
            break

        self.update_tree()
        self.draw_pages()
        self.unsave()
        self.locker.close_function(self.rename_file)

    def split_page(self, evt = None):
        if self.locker.open_function(self.split_page): return
        if evt == None:
            selection = self.tree_files.selection()
            if len(selection) != 1:
                self.locker.close_function(self.split_page)
                return

            iid = selection[0]
            item = self.tree_files.item(iid)
            file = item['text']
            reverse = item['values'][2]
            pages = item['values'][3]
            pages = getPagesNumber(pages, reverse = reverse == 'OUI', getCompleteList = True)
            page = askinteger('Sépération', 'A quelle page souhaitez vous séparer votre fichier ?\n(La page indiqué sera la première de la deuxième motiée)')

        else:
            file, page = evt.widget.cget('text')[2:].split(' - Page ')
            page = int(page)
            pages = self.file_infos[file]['group']
            reverse = self.file_infos[file]['reverse']
            pages = getPagesNumber(pages, reverse = reverse == 'OUI', getCompleteList = True)

        fl1 = []
        fl2 = []
        for i in range(len(pages)):
            if i+1 < page:
                fl1.append(pages[i])
            else:
                fl2.append(pages[i])

        fl1 = getPageSet(fl1)
        fl2 = getPageSet(fl2)

        copy = {}
        for k, v in self.file_infos.items():
            if k == file:
                vp1, vp2 = v.copy(), v.copy()
                vp1['group'] = str(fl1)
                vp2['group'] = str(fl2)
                copy[k] = vp1
                name = self.next_name(k)
                copy[name] = vp2
                self.images_list[name] = self.images_list[k]
                continue
            
            copy[k] = v

        self.file_infos = copy
        self.update_tree()
        self.draw_pages()
        self.unsave()
        self.locker.close_function(self.split_page)

    def remove_file(self, evt):
        if self.locker.open_function(self.remove_file): return
        info = evt.widget.cget('text')[2:]
        file, _ = info.split(' - Page ')
        for x in self.tree_files.get_children():
            item = self.tree_files.item(x)
            if item['text'] == file:
                self.tree_files.delete(x)
                del self.file_infos[file]
                del self.images_list[file]
                self.draw_pages()
                self.unsave()
                self.locker.close_function(self.remove_file)
                return

    def delete_file(self):
        if self.locker.open_function(self.delete_file): return
        selection = self.tree_files.selection()
        for iid in selection:
            file = self.tree_files.item(iid)['text']
            self.tree_files.delete(iid)

        self.unsave()
        self.update_infos()
        self.locker.close_function(self.delete_file)

    def select_image(self, evt):
        label = evt.widget
        text = label.cget('text')
        if text[0] == self.CASE_ON:
            text = self.CASE_OFF + text[1:]
        else:
            text = self.CASE_ON + text[1:]

        label.config(text = text)

    def selectall(self, evt = None, output = True):
        for label in self.names_pages:
            txt = label.cget('text')
            char = self.CASE_ON if output else self.CASE_OFF
            label.config(text = char + txt[1:])

    def move(self, direction = 'up'):
        if self.locker.open_function(self.move): return
        leaves = self.tree_files.selection()
        dest = []
        if direction == 'up':
            if len(leaves) > 1 and self.tree_files.index(leaves[0]) == 0:
                self.locker.close_function(self.move)
                return
            for i in leaves:
                self.tree_files.move(i, self.tree_files.parent(i), self.tree_files.index(i)-1)
                #dest.append(self.tree_files.get_children()[self.tree_files.index(i)])

        elif direction == 'down':
            if len(leaves) > 1 and self.tree_files.index(leaves[-1]) == len(self.tree_files.get_children())-1:
                self.locker.close_function(self.move)
                return
            for i in reversed(leaves):
                self.tree_files.move(i, self.tree_files.parent(i), self.tree_files.index(i)+1)
                #dest.append(self.tree_files.get_children()[self.tree_files.index(i)+1])

        self.update_infos()
        self.tree_files.selection_set(tuple(dest))
        self.unsave()
        self.locker.close_function(self.move)

    def sort_files(self):
        if self.locker.open_function(self.sort_files): return
        self.n_filter += 1
        reverse = True if self.n_filter % 2 == 0 else False
        copy = {}
        keys = list(self.file_infos.keys())
        table = {}
        for i in range(len(keys)):
            table[keys[i].lower()] = keys[i]
            keys[i] = keys[i].lower()
        sorted_keys = sorted(keys)
        if reverse:
            sorted_keys = sorted_keys[::-1]
        for key in sorted_keys:
            copy[table[key]] = self.file_infos[table[key]]
        self.file_infos = copy
        del copy

        copy = {}
        keys = list(self.images_list.keys())
        table = {}
        for i in range(len(keys)):
            table[keys[i].lower()] = keys[i]
            keys[i] = keys[i].lower()
        sorted_keys = sorted(keys)
        if reverse:
            sorted_keys = sorted_keys[::-1]
        for key in sorted_keys:
            copy[table[key]] = self.images_list[table[key]]
        self.images_list = copy
        del copy

        self.update_tree()
        self.update_infos()
        self.unsave()
        self.locker.close_function(self.sort_files)

    def move_insert(self, to, evt = None):
        selected = self.tree_insert.selection()
        if not selected:
            return

        if to == 'create':
            s = self.tree_insert.index(selected[0])
            it = self.tree_insert.item(selected[0])
            values = it['values'].copy()
            values[0] = ''
            iid = self.tree_insert.insert('', s, text = 'Nouveau Groupe', values = values, open = True)
            self.move_insert('right', evt)

        if to == 'right':
            iid = self.tree_insert.index(selected[0])
            iid -= 1
            parent = self.tree_insert.get_children()[iid]

            path = self.tree_insert.item(parent)['values'][0]
            if path:
                self.move_insert('create', evt)
                return

            for s in selected:
                self.tree_insert.move(s, parent = parent, index = self.tree_insert.index(s))

        elif to == 'left':
            for s in selected:
                self.tree_insert.move(s, parent = '', index = self.tree_insert.index(s))

        if to == 'up':
            if len(selected) > 1 and self.tree_insert.index(selected[0]) == 0:
                return
            for i in selected:
                self.tree_insert.move(i, self.tree_insert.parent(i), self.tree_insert.index(i)-1)

        if to == 'down':
            if len(selected) > 1 and self.tree_insert.index(selected[-1]) == len(self.tree_insert.get_children())-1:
                return
            for i in reversed(selected):
                self.tree_insert.move(i, self.tree_insert.parent(i), self.tree_insert.index(i)+1)

if __name__ == '__main__':
    from test import *
    e = Tester()
