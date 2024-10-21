from tkinter import *
from PIL import *

class IconGetter:
    def __init__(self, image=None, big = None, medium = None, small = None, default = 'medium', default_menu = 'small'):
        self.image = image
        self.big = big
        self.medium = medium
        self.small = small

        if default_menu == 'small':
            self.menu = self.small
        elif default_menu == 'medium':
            self.menu = self.medium
        elif default_menu == 'big':
            self.menu = self.big

        if default == 'small':
            self.default = self.small
        elif default == 'medium':
            self.default = self.medium
        elif default == 'big':
            self.default = self.big

    def __getattr__(self, index):
        s = index.replace('size', '')
        s = int(s)
        if s < self.image.width():
            ratiox = int(self.image.width()/s)
            ratioy = int(self.image.height()/s)
            newimage = self.image.subsample(ratiox, ratioy)
        else:
            ratiox = int(s/self.image.width())
            ratioy = int(s/self.image.height())
            newimage = self.image.zoom(ratiox, ratioy)

        return newimage

class Images:
    def __init__(self, pm):
        self.pm = pm

    def load_images(self):
        files = {
            'Save': './images/SaveIcon.png',
            'SaveAs': './images/SaveAsIcon.png',
            'SaveCopyAs': './images/SaveCopyAsIcon.png',
            'Open': './images/OpenIcon.png',
            'Close': './images/CloseIcon.png',
            'Exit': './images/ShutIcon.png',
            'Doc': './images/DocIcon.png',
            'Import': './images/OpenIcon.png',
            'Export': './images/SaveIcon.png',
            'Print': './images/PrinterIcon.png',
            'Search': './images/SearchIcon.png',
            'Add': './images/AddIcon.png',
            'Help': './images/HelpIcon.png',
            'Redo': './images/RedoIcon.png',
            'Undo': './images/UndoIcon.png',
            'Upgrade': './images/Upgrade.png',
            'Down': './images/DownArrowIcon.png',
            'Up': './images/UpArrowIcon.png',
            'Left': './images/LeftArrowIcon.png',
            'Right': './images/RightArrowIcon.png',
            'Copy': './images/CopyIcon.png',
            'Logo': './images/LogoIcon.png',
            'Errors': './images/ErrorsIcon.png',
            'Astuces': './images/TipsIcon.png',
            'Gear': './images/GearIcon.png',
            }

        self.ICONS = {
            'Logo': './images/logo.ico',
            'Tips': './images/tips.ico',
            'Help': './images/HelpIcon.ico',
            'Search': './images/SearchIcon.ico',
            'Gear': './images/GearIcon.ico',
            }

        self.icons = {}
        for name, file in files.items():
            big = PhotoImage(file = file)
            medium = PhotoImage(file = file)
            small = PhotoImage(file = file)
            image = PhotoImage(file = file)

            big = big.subsample(10, 10)
            medium = medium.subsample(16, 16)
            small = small.subsample(32, 32)

            self.icons[name] = IconGetter(image, big, medium, small, default = self.pm.general.general['icon_size'])

    def __getattr__(self, index):
        if index in list(self.icons.keys()):
            return self.icons[index]
        else:
            return IconGetter()

if __name__ == '__main__':
    from mainwin import *
    mw = MainWindow()
    mw.Generate()
