from mainwin import *
from confr import *

class Tester:
    def __init__(self, tests = []):
        print('#############################################################')
        print('##### MODE DE TESTS !! ######################################')
        print('#############################################################')
        print()
        print('Lancement de la fenêtre')
        self.mw = MainWindow()
        print('Récupération des paramètres')
        s = self.mw.pm
        print('Recherche d\'éxécution')
        if s.work.general['testing'] == '1' and tests == []:
            print('Execution trouvées dans le fichiers de configuration de travail')
            for test in s.work.general['working'].split(', '):
                if self.run_test(test):
                    print('Arrêt de l\'éxécution des tests sur demande de', test)
                    break
        elif tests != []:
            print('Execution directe depuis un programme')
            for test in tests:
                if self.run_test(test):
                    print('Arrêt de l\'éxécution des tests sur demande de', test)
                    break

        print()
        print('#############################################################')
        print('###### FIN DES LANCEMENTS DES TESTS #########################')
        print('###### FENETRE PRETTE POUR USAGE    #########################')
        print('#############################################################')
        self.mw.Generate()

    def run_test(self, name):
        print('Demande d\'éxécution d\'un test, call=', name)

        if name == 'tips' and self.mw.pm.general.general['tips'] == '0':
            print('Test des conseils au démarrage')
            self.mw.tips.start_tips_index(0)
            return True

        if name == 'import_pdf':
            print('Importation de fichiers PDF')
            self.mw.open_PDFfile(path = ['./tests/jaquette.pdf', './tests/test.pdf', './tests/test2.pdf', './tests/test1.pdf', './tests/PDFsam_addbackpages.pdf', './tests/PDFsam_alternatemix.pdf'])
            self.mw.onglets.select(0)

        if name == 'import_csv':
            print('Importation de liste de fichier CSV ou Excel')
            self.mw.open_CSVfile(csv = ['./tests/liste.csv'])

        if name == 'import_img':
            print('Importation d\'images')
            self.mw.import_images(files = ['./tests/img.png'])

        if name == 'open_project':
            print('Ouverture d\'un projet')
            self.mw.open_project(path = './tests/test_dépliant.pdfpro')

        if name == 'import_project':
            print('Importation de plusieurs projets')
            self.mw.import_project(paths = ['./tests/test_dépliant.pdfpro', './tests/test1.pdfpro'])

        if name == 'export_fusion':
            print('Exportation de la fusion sous un fichier pré défini')
            self.mw.export_fusion(path = './tests/output.pdf')

        if name == 'import_insert':
            print('Importation de fichier pour la zone d\'insertion')
            self.mw.import_insert(paths = ['./tests/jaquette.pdf', './tests/test.pdf', './tests/test2.pdf', './tests/test1.pdf', './tests/PDFsam_addbackpages.pdf', './tests/PDFsam_alternatemix.pdf'])
            self.mw.onglets.select(2)

        if name == 'show_aide':
            print('Ouverture de la page d\'aide')
            self.mw.aide_doc('all')

        if name == 'show_config':
            print('Ouverture de la page de configuration')
            self.mw.configure()

        if name == 'show_pages':
            print('Affichage de l\'onglet pages')
            self.mw.onglets.select(1)

        if name == 'show_search':
            print('Ouverture de la fenêtre de recherche')
            self.mw.search()

        return False
