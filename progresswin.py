from tkinter import *
from tkinter import ttk
from tkinter.ttk import *


class ProgressWindow:
    def __init__(self, parent, barres):
        self.master = Toplevel(parent)
        self.master.transient(parent)
        self.master.title('Progression...')
        self.master.protocol('WM_DELETE_WINDOW', lambda: None)
        self.master.columnconfigure(0, weight = 1)
        self.master.resizable(True, False)
        self.master.minsize(400, 200)

        self.bars = []
        for mode in barres:
            self.bars.append({
                'name': mode,
                'label_title': None,
                'label_value': None,
                'value': StringVar(value = '0 %'),
                'progressbar': None,
                'maxi': 0,
                '%': 0.0,
                'iter': 0,
                })

        self.draw()

    def draw(self):
        k = 1
        for bar in self.bars:
            bar['label_title'] = ttk.Label(self.master, text = bar['name'])
            bar['label_title'].grid(row = 2*k + 0, column = 0, padx = 5, pady = 5, sticky = 'w')
            bar['label_value'] = ttk.Label(self.master, textvariable = bar['value'])
            bar['label_value'].grid(row = 2*k + 0, column = 1, padx = 5, pady = 5, sticky = 'e')
            bar['progressbar'] = ttk.Progressbar(self.master, length = 100)
            bar['progressbar'].grid(row = 2*k + 1, column = 0, columnspan = 2, padx = 5, pady = 5, sticky = 'we')
            k += 1

    def update(self):
        for bar in self.bars:
            bar['value'].set(str(int(bar['%'])) + ' %')
            bar['progressbar']['value'] = bar['%']

        self.master.update()

    def config(self, bar, maxi):
        self.bars[bar]['maxi'] = maxi
        self.bars[bar]['iter'] = 0

    def step(self, bar):
        self.bars[bar]['iter'] += 1
        self.bars[bar]['%'] = 100 * (self.bars[bar]['iter'] / self.bars[bar]['maxi'])

        self.update()

    def finish(self):
        self.master.destroy()


if __name__ == '__main__':
    import time
    root = Tk()

    p = ProgressWindow(root, barres = ['Test n°2', 'Test n°3'])
    p.config(0, 10)
    for i in range(10):
        p.config(1, 15)
        for j in range(15):
            p.step(1)
            time.sleep(0.1)
        p.step(0)
    p.finish()
