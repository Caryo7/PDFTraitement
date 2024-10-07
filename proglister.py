from pathlib import Path
import sqlite3
import zipfile as zp

class PDFSEA:
    def __init__(self, file):
        self.file = file

    def read(self):
        z = zp.ZipFile(self.file, 'r')
        data = {}
        for f in z.namelist():
            data[f] = z.read(f).decode('utf-8')
        z.close()
        return data

    def write(self, data):
        z = zp.ZipFile(self.file, 'w')
        for file, content in data.items():
            f = z.open(file, 'w')
            f.write(content.encode())
            f.close()
        z.close()

    def close(self):
        pass

class ProgLister:
    def __init__(self):
        self.conn = sqlite3.connect('./programs/prog_list.db')
        self.cur = self.conn.cursor()

    def getList(self, prog_name):
        result = self.cur.execute('SELECT * FROM programs')
        r = {}
        for row in result:
            if row[1] == prog_name:
                fp = Path(row[2])
                dic = {'path': fp,
                       'file': fp.name,
                       'type': 'Par défaut' if row[4] else 'Personnel',
                       'favori': True if row[5] == 1 else False,}
                r[row[3]] = dic

        return r

    def update(self, desc, cat, content, new_name, fav):
        result = self.cur.execute('SELECT * FROM programs')
        for row in result:
            if row[1] == cat and desc == row[3]:
                self.cur.execute('UPDATE programs SET favorite = "{0}" WHERE id = {1}'.format(1 if fav else 0, row[0]))
                self.conn.commit()
                file = Path(row[2])
                f = PDFSEA(file)
                f.write(content)
                f.close()
                self.rename(desc, new_name)
                return

        item_nb = str(row[0] + 2)
        fp = "./programs/Program-" + item_nb + ".pdfsea"
        file = Path(fp)
        f = PDFSEA(file)
        f.write(content)
        f.close()
        self.cur.execute('INSERT INTO programs (name, file, description, origin, favorite) VALUES ("{0}", "{1}", "{2}", "{3}", "{4}")'.format(cat, fp, new_name, 0, fav))
        self.conn.commit()

    def delete(self, cat, desc):
        result = self.cur.execute('SELECT id, name, description FROM programs')
        nb = 0
        for row in result:
            if row[1] == cat and row[2] == desc:
                nb = row[0]

        self.cur.execute('DELETE FROM programs WHERE id={}'.format(nb))
        self.conn.commit()

    def rename(self, old_name, new_name):
        if old_name == new_name:
            return

        result = self.cur.execute('SELECT id, description FROM programs')
        for row in result:
            if row[1] == old_name:
                self.cur.execute('UPDATE programs SET description = "{0}" WHERE id = {1}'.format(new_name, row[0]))
                self.conn.commit()
                return

    def duplicate(self, name, desc):
        result = self.cur.execute('SELECT * FROM programs')
        for row in result:
            pass

        nb = row[0] + 1
        result = self.cur.execute('SELECT * FROM programs')
        for row in result:
            if row[1] == name and desc == row[3]:
                file_origin = Path(row[2])
                f = './programs/' + 'Program-' + str(nb) + '.pdfsea'
                file_dest = Path(f)
                fo = PDFSEA(file_origin)
                fd = PDFSEA(file_dest)
                fd.write(fo.read())
                fd.close()
                fo.close()

                self.cur.execute('INSERT INTO programs (name, file, description, origin, favorite) VALUES ("{0}", "{1}", "{2}", "{3}", "{4}")'.format(name, f, desc + ' (2)', 0, 0))
                self.conn.commit()
                return

        raise ValueError('No value searched in data base !')

    def new(self, cat, file, fav, origin, name):
        self.cur.execute('INSERT INTO programs (name, file, description, origin, favorite) VALUES ("{0}", "{1}", "{2}", "{3}", "{4}")'.format(cat, file, name, origin, fav))
        self.conn.commit()


if __name__ == '__main__':
    pl = ProgLister()
    r = pl.getList('ExtractPages')
    print(r)
    i = r["Extraction d'une page sur deux"]
    print(i)
    print(i['path'].parent.parent)
