from mainwin import *
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog = 'main.exe', description="Logiciel de traitement de fichiers PDF.\nIl est possible de contrôler l\'ouverture du programme en passant ici par la ligne de commande.\nVous pouvez utiliser plusieurs fois chaque commande. Cependant, à partir du deuxième projet ouvert, tout sera importé et non ouvert.", epilog = 'Merci d\'utiliser notre application !')
    parser.add_argument('-p', dest = 'project', help='Le projet s\'il y en a un à ouvrir', nargs = '+')
    parser.add_argument('-pdf', dest = 'PDF', help = 'Ouvre dans le logiciel un fichier, de type PDF', nargs = '+')
    parser.add_argument('-img', dest = 'IMG', help = 'Ouvre dans le logiciel un fichier, de type image', nargs = '+')
    parser.add_argument('-sea', dest = 'SEA', help = 'Importe une fonction et lance le programme d\'enregistrement', nargs = '+')
    parser.add_argument('-csv', dest = 'CSV', help = 'Ouvre les fichiers dans une liste de fichier au format csv ou excel', nargs = '+')
    parser.add_argument('-run', dest = 'runing', metavar = 'MODE', help = "Lance un programme du mode basic : FUSION, IMAGES, CSV")
    parser.add_argument('-exe', dest = 'execute', metavar = ('PROGRAMME', 'FONCTION'), help = "Lance le programme indiqué par la fonction. Syntaxe : [programme fonction]", nargs = 2)
    parser.add_argument('-o', dest = 'output', help = "Fichier ou dossier de sortie pour l'éxécution du programme")
    parser.add_argument('-exit', dest = 'exit_on_end', action = 'store_true', help = "Ferme la fenêtre une fois l'action réalisée")
    parser.add_argument('-save', dest = 'save_on_end', action = 'store_true', help = "Enregistre le projet ouvert (s'il y en a un) automatiquement avant de fermer")
    parser.add_argument('-l', dest = 'files', help = 'Ouvre une liste de fichiers, sans distinctions entre les projets, les pdf ou autres formats.', nargs = '+')

    args = parser.parse_args()
    mw = MainWindow(args = args)
    mw.Generate()
