# on prend des valeurs d'exemples :

def test(matrix1, matrix2):
    for y in range(len(matrix1.values)):
        for x in range(len(matrix1.values[y])):
            if float(matrix1.values[y][x] - matrix2.values[y][x]) != 0.0:
                return False

    return True
        
    
class Matrix:
    def __init__(self, table = None):
        if table != None:
            self.values = table

    def __str__(self):
        txt = ''
        for y in range(len(self.values)):
            txt += '|'
            for x in range(len(self.values[y])):
                txt += str(self.values[y][x]) + ' '
            txt = txt[:-1]
            txt += '|\n'
        return txt[:-1]

    def __add__(self, matrix):
        m = self.values.copy()
        for y in range(len(matrix.values)):
            for x in range(len(matrix.values[y])):
                m[y][x] += matrix.values[y][x]

        return Matrix(m)

    def __sub__(self, matrix):
        matrix = matrix * (-1)
        return self.__add__(matrix)

    def __mul__(self, matrix):
        m = self.values.copy()
        if not isinstance(matrix, Matrix):
            for y in range(len(m)):
                for x in range(len(m[y])):
                    m[y][x] *= matrix

            return Matrix(m)
        else:
            return Matrix([])


class Imitator:
    def __init__(self, u):
        self.u = u
        self.ecarts = []

    def give(self, n):
        for i, ec in enumerate(self.ecarts):
            print('Si i congru a', i, '[', len(self.ecarts), '], alors on fait', ec)

def u(n):
    values = [Matrix([[5, 6, 1]]), Matrix([[2, 3, 4]]), Matrix([[11, 12, 7]]), Matrix([[8, 9, 10]])]
    return values[int(n)]

def d(n, a):
    num = u((n/a) + a) - u(n/a)
    deno = 1/(2 - ((n + a) % 2))
    return num * deno

Imi = Imitator([Matrix([[5, 6, 1]]), Matrix([[2, 3, 4]]), Matrix([[11, 12, 7]]), Matrix([[8, 9, 10]])])
a = 0
w = []
while True:
    a += 1
    w.clear()
    n = 0
    while True:
        try:
            r = d(n*a, a)
        except IndexError:
            break

        found = False
        for ma in w:
            if test(ma, r):
                Imi.ecarts.append(r*a)
                found = True

        if not found:
            w.append(r)

        n += 1
        del r

    if n == 0:
        break

    del n
