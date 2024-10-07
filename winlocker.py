from tkinter import *
from tkinter.messagebox import *
import time

class WinLocker:
    def __init__(self):
        self.stat = True
        self.credits = []
        self.cmd = None
        self.stoped = 0
        self.temps = 0
        self.duree = 0

    def open_function(self, fnct = None, *args):
        new_t = time.time()
        if fnct == None:
            showwarning('WinLocker', 'Appel du locker obsolète sur la commande séléctionnée !')

        if not self.stat and fnct not in self.credits and self.stoped >= 20 and self.duree / self.stoped <= 2:
            showwarning('WinLocker', "Le bloqueur n'a pas été débloqué par la précédente commande. La gestion de l'ouverture des fenêtres uniques va être redémarré. Commande source de l'erreur\n" + str(self.cmd) + '\nCommande actuelle en attente\n' + str(fnct) + '\nCette commande sera éxécuté dès la validation de cette information !')
            self.stat = True
            self.cmd = fnct
            self.temps = time.time()
            return False

        if self.stat:
            self.cmd = fnct
            self.stat = False
            self.temps = time.time()
            return False
        elif self.credit_in(fnct)[0]:
            self.stat = False
            return False
        else:
            self.stoped += 1
            self.duree = self.temps - new_t
            self.temps = new_t
            return True

    def credit_in(self, fnct):
        for c in self.credits:
            if c['fnct'] == fnct:
                return (True, c['perisable'])

        return (False, None)

    def restrict(self, fnct):
        self.credits.pop(self.credit_index(fnct))

    def close_function(self, fnct):
        ins, per = self.credit_in(fnct)
        if ins and per:
            self.credits.pop(self.credit_index(fnct))
        elif ins and not per:
            pass
        else:
            if fnct != self.cmd:
                showwarning('WinLocker', "La commande de fermeture ne correspond pas à la commande d'ouverture !")
            self.stat = True
            self.cmd = None
            self.stoped = 0
            self.duree = 0
            self.credits.clear()

    def credit_index(self, fnct):
        for i, c in enumerate(self.credits):
            if c['fnct'] == fnct:
                return i

    def aload(self, fnct, perisable = True):
        self.credits.append({'fnct': fnct, 'perisable': perisable})

if __name__ == '__main__':
    from test import *
    e = Tester()
