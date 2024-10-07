from PyPDF2 import *
from configparser import ConfigParser
from tkinter import *
from tkinter.messagebox import *

from extract import *
from merge import *
from posters import *
from proglister import *
from confr import *

class Equation:
    operators = {
        '-': {'priority': 2, 'bi': True, 'cmd': lambda a, b: a - b},
        '+': {'priority': 2, 'bi': True, 'cmd': lambda a, b: a + b},
        '%': {'priority': 0, 'bi': True, 'cmd': lambda a, b: a % b},
        '*': {'priority': 1, 'bi': True, 'cmd': lambda a, b: a * b},
        '/': {'priority': 1, 'bi': True, 'cmd': lambda a, b: a / b},
        }

    condition = {
        '=':  lambda a, b: a == b,
        '!': lambda a, b: a != b,
        '<': lambda a, b: a <= b,
        '>': lambda a, b: a >= b,
        }

    def __init__(self, formula, replacement):
        for k, v in replacement.items():
            formula = formula.replace(str(k), str(v))
        formula = formula.replace(' ', '')

        self.zone_left = ''
        self.zone_right = ''
        i = 0
        j = 1
        self.cond = '='
        if '=' not in formula:
            self.zone_left = '(' + formula + ')'
            self.zone_right = ''
        else:
            while formula[i] != '=':
                i += 1
                j += 1
            if formula[i-1] in list(self.condition.keys()):
                self.cond = formula[i - 1]
                i -= 1

            self.zone_left = '(' + formula[:i] + ')'
            self.zone_right = '(' + formula[j:] + ')'

        #print(self.zone_left, '=', self.zone_right)

    def test(self):
        result_left = self.compute('left')
        result_right = self.compute('right')
        #print(result_left, '=', result_right, '?')
        if self.condition[self.cond](result_left, result_right):
            #print('Oui')
            return True
        else:
            #print('Non')
            return False

    def compute(self, zone):
        if zone == 'left':
            zone = self.zone_left
        else:
            zone = self.zone_right

        calculs = []
        in_cal = []
        for i, char in enumerate(zone):
            #print(char, in_cal, calculs)
            if char == '(':
                #print('Ouverture d\'une section')
                calculs.append({'begin': i, 'end': None, 'value': False})
                in_cal.append(len(calculs)-1)
            elif char == ')':
                #print('Fermeture d\'une section')
                calculs[in_cal[-1]]['end'] = i+1
                in_cal.pop(-1)

        result = int(self.calcule(zone, calculs))
        return result

    def layout(self, digit, begin, end):
        digit = str(digit)
        length = end - begin
        while len(digit) != length:
            if digit[0] == '-':
                digit = '-0' + digit[1:]
            else:
                digit = '0' + digit
        return digit

    def testFinish(self, expression):
        a = 0
        for i in expression:
            if not i['value']:
                a += 1

        if a == 0:
            return True
        else:
            return False

    def calcule(self, zone, expression):
        n = 1
        while expression[-n]['value']:
            n += 1
        n = -n
        exp = expression[n]
        buffer = zone[exp['begin']:exp['end']]
        buffer = buffer.replace('(', '')
        buffer = buffer.replace(')', '')
        op = None
        #print('Etat du buffer:', buffer)
        for operator in list(self.operators.keys()):
            if operator in buffer:
                op = operator

        if op == None:
            return buffer
        #print('Opérateur:', op)

        infos_op = self.operators[op]
        if infos_op['bi']:
            buffer = buffer.split(op)
            for i in range(len(buffer)):
                buffer[i] = int(buffer[i])
            buffer = tuple(buffer)

        result = int(infos_op['cmd'](*buffer))
        expression[n]['value'] = True
        result = self.layout(result, exp['begin'], exp['end'])
        z = list(zone)
        #print('Resultat:', result)
        #print('Ancienne zone:', zone)
        for i in range(exp['end'] - exp['begin']):
            z[i + exp['begin']] = result[i]
        zone = ''.join(z)
        #print('Nouvelle zone:', zone)
        
        if self.testFinish(expression):
            return zone
        else:
            return self.calcule(zone, expression)

class Condition:
    def __init__(self, equation, output):
        self.equation = equation
        self.output = output.split(';')

    def function(self, i, l):
        e = Equation(self.equation, {'i': i, 'l': l})
        if e.test():
            #print('Test réussi, calcul de la sortie')
            self.Result = []
            for op in self.output:
                #print('Equation de sortie:', op)
                r = Equation(op, {'i': i, 'l': l})
                self.Result.append(r.compute('left'))
                #print('Résultat de sortie:', self.Result[-1])
            return [True, self.Result]

        return [False, None]


class Runner:
    TABLE_MOD = {
        'ExtractPages':  {'class': ExtractPages},
        'ExtractImages': {'class': ExtractImages},
        'SplitFile':     {'class': SplitFile},
        'OrganizePages': {'class': OrganizePages},
        'RemovePages':   {'class': RemovePages},
        'Poster':        {'class': Poster},
        'ArrangerDuo':   {'class': ArrangerDuo},
        'ArrangerTrio':  {'class': ArrangerTrio},
        'ScaleFile':     {'class': ScaleFile},
        'MarginFile':    {'class': MarginFile},
        'RognerFile':    {'class': RognerFile},
        'RotateFile':    {'class': RotateFile},
        'AdditionPage':  {'class': AdditionPage},
        'None':          {'class': None},
        'Custom':        {'class': None},
        #'ExtractPages': {'class': ExtractPages},
        }
    unites = {
        'defaut': 1,
        'mm': 842/297,
        'cm': 842/29.7,
        'inch': 1,
        'pouce': 1}

    def __init__(self):
        self.pm = Settings()
        for k, v in self.TABLE_MOD.items():
            item = self.pm.programs.getItem(k)
            name = item['name']
            info_output = item['output']
            info_input = item['input']
            info_more = item['infos']

            self.TABLE_MOD[k]['name'] = name
            self.TABLE_MOD[k]['output'] = info_output
            self.TABLE_MOD[k]['input'] = info_input
            self.TABLE_MOD[k]['infos'] = info_more

        ut = self.pm.general.general['unit']
        self.unit = self.unites[ut]

    def start_load(self, command_begin, command_end, progress, stat, parent):
        self.command_begin = command_begin
        self.command_end = command_end
        self.progress = progress
        self.parent = parent
        self.stat = stat

    def update_stat(self, text):
        self.stat.set(value = text)
        self.parent.update()

    def export_fusion(self, data, para = {}):
        writer = PdfWriter()
        for info_page in data['pages']:
            reader = PdfReader(info_page['path'])
            writer.add_page(reader.pages[info_page['page']])

        if 'pswd' in list(para.keys()):
            code = 0
            code += para['aload_print']
            code += para['aload_modify']
            code += para['aload_annotation']
            code += para['aload_fields']
            code += para['aload_extract']
            if para['pswd_admin'] == '':
                para['pswd_admin'] = para['pswd']
            print(code, bin(code))
            #writer.encrypt(user_password = para['pswd'],
            #               owner_password = para['pswd_admin'],
            #               permissions_flag = bin(code))

        fichier = './temp_files/temp.pdf'
        fp = open(fichier, 'wb')
        writer.write(fp)
        fp.close()
        return fichier

    def execute(self, module, pdfsea):
        self.update_stat("Préparation du démarrage")
        self.progress['value'] = 0
        self.update_stat("Récupération des données")
        data = self.command_begin(module + '->' + pdfsea)
        if not data:
            return

        self.update_stat("Fusion des fichiers demandés")
        fichier = self.export_fusion(data)

        self.update_stat("Récupération du programme")
        Module = self.TABLE_MOD[module]['class']
        self.pdfsea = pdfsea
        self.function_creator()

        self.update_stat("Paramétrage du programme")
        self.module = Module(fichier, self.function, data['output_file'], data['output_folder'], self.unit)
        nb_iter = self.module.nb_iter
        pos = 0
        self.update_stat("Execution du programme")
        for i in self.module.run():
            pos += i
            pc = 100 * pos/nb_iter
            self.progress['value'] = pc
            self.parent.update()

        self.update_stat("Enregistrement...")
        e = 0
        while e < 10:
            try:
                self.module.close()
                break
            except PermissionError:
                e += 1
                showerror('Enregistrement', "Conflit de droit : le fichier est déjà ouvert par un autre programme et ne peut par conséquent pas être mis à jour. Fermez ce document, et validez pour recommencer")

        if e >= 10:
            self.update_stat("Génération avorté")
            del module
            return

        if data['open_end']:
            self.update_stat("Ouverture du fichier de sortie...")
            os.popen(data['output_file'])
            #os.popen('start ' + data['output_folder'])

        self.update_stat("Libération de la mémoire")
        del module

        self.update_stat("Génération terminée")
        self.command_end()

    def function_creator(self):
        f = PDFSEA(self.pdfsea)
        content = f.read()
        f.close()

        if 'conditions.ini' not in content:
            return

        self.conditions = {}
        data = content['conditions.ini']
        for line in data.split('\n'):
            if not line:
                return

            nb, test, output = line.split('\\')
            self.conditions[nb] = {'test': test, 'output': output}

    def function(self, i, l):
        for nb, settings in self.conditions.items():
            c = Condition(settings['test'], settings['output'])
            able, output = c.function(i, l)
            if able:
                return output

if __name__ == '__main__':
    from test import *
    e = Tester()
