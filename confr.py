import sqlite3
from configparser import ConfigParser

class GetSettings:
    def __init__(self, values):
        self.values = values

    def getAll(self):
        for key, data in self.values.items():
            yield key, data

    def getItem(self, item):
        return self.values[item]

    def __getattr__(self, index):
        return self.getItem(index)

    def reset(self):
        self.values = {}

    def set(self, index, option, value):
        if index not in list(self.values.keys()):
            self.values[index] = {}

        self.values[index][option] = value


class Settings:
    def __init__(self):
        self.config_files = {
            'menus':         {'section_inst': lambda a: int(a), 'file': './config/menus.ini'},
            'programs':      {'section_inst': lambda a: str(a), 'file': './config/programs.ini'},
            'keys':          {'section_inst': lambda a: str(a), 'file': './config/keys.ini'},
            'editor_python': {'section_inst': lambda a: str(a), 'file': './config/editor_python.ini'},
            'editor_basic':  {'section_inst': lambda a: str(a), 'file': './config/editor_basic.ini'},
            'general':       {'section_inst': lambda a: str(a), 'file': './config/global.ini'},
            'paths':         {'section_inst': lambda a: str(a), 'file': './config/paths.ini'},
            'prog':          {'section_inst': lambda a: str(a), 'file': './config/progwin.ini'},
            'run':           {'section_inst': lambda a: str(a), 'file': './config/running.ini'},
            'work':          {'section_inst': lambda a: str(a), 'file': './config/work.ini'},
            #'': {'section_inst': lambda a: str(a), 'file': './config/.ini'},
            }

        for function, infos in self.config_files.items():
            parser = ConfigParser()
            parser.read(infos['file'], encoding = 'utf-8')
            cmd = infos['section_inst']
            values = {}
            for sect in parser.sections():
                if cmd(sect) not in list(values.keys()):
                    values[cmd(sect)] = {}

                for opt in parser.options(sect):
                    values[cmd(sect)][opt] = parser.get(sect, opt)

            self.config_files[function]['settings'] = GetSettings(values)

    def reload_updates(self):
        for index, data in self.config_files.items():
            parser = ConfigParser()
            settings = data['settings']
            for sect, options in settings.getAll():
                sect = str(sect)
                parser.add_section(sect)
                for opt, value in options.items():
                    parser.set(str(sect), str(opt), str(value))

            f = open(data['file'], mode = 'w', encoding = 'utf-8')
            parser.write(f)
            f.close()

    def __getattr__(self, index):
        if index in list(self.config_files.keys()):
            return self.config_files[index]['settings']
        else:
            return None

if __name__ == '__main__':
    from test import *
    e = Tester()
