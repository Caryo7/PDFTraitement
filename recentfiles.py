from tkinter import *
from tkinter import ttk
from tkinter.ttk import *
import os

class MenuRecent(Menu):
    def __init__(self, reopen, pm, *args, **kwargs):
        super().__init__(tearoff = 0, *args, **kwargs)
        self.reopen = reopen
        self.pm = pm

    def load_story(self, new_file = None):
        rf_list = []
        file_path = 'history.log'
        if file_path and os.path.exists(file_path):
            with open(file_path,
                      encoding='utf_8', errors='replace') as rf_list_file:
                rf_list = rf_list_file.readlines()

        if new_file:
            new_file = os.path.abspath(new_file) + '\n'
            if new_file in rf_list:
                rf_list.remove(new_file)  # move to top
            rf_list.insert(0, new_file)
        # clean and save the recent files list
        bad_paths = []
        for path in rf_list:
            if '\0' in path or not os.path.exists(path[0:-1]) or not path:
                bad_paths.append(path)
        rf_list = [path for path in rf_list if path not in bad_paths]
        ulchars = "1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        rf_list = rf_list[0:len(ulchars)]
        if file_path:
            try:
                with open(file_path, 'w',
                          encoding='utf_8', errors='replace') as rf_file:
                    rf_file.writelines(rf_list)
            except OSError:
                pass

        self.delete(0, END)  # clear, and rebuild:
        for i, file_name in enumerate(rf_list):
            if i == int(self.pm.general.general['recent_files']):
                break

            file_name = file_name.rstrip()  # zap \n
            callback = self.__recent_file_callback(file_name)
            self.add_command(label=ulchars[i] + ' ' + file_name,
                             command=callback,
                             underline=0)

    def __recent_file_callback(self, file_name):
        def open_recent_file(fn_closure=file_name):
            self.reopen(file_name)
        return open_recent_file

if __name__ == '__main__':
    from mainwin import *
    mw = MainWindow()
    mw.Generate()
