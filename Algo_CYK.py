import json

class Stare:
    nume = ""
    drum = []


    def __init__(self, nume, drum):
        self.nume = nume
        self.drum = drum


    def preiaNume(self):
        return self.nume


    def preiaDrum(self):
        return self.drum


    def preiaStareCuLitera(self, caracter):
        for val in self.drum:
            if caracter == val[0]:
                return True
        return False

    def verificaNeterminal(self, nod):
        for val in self.drum:
            if val == nod:
                return True
        return False


class AlgoCYK:
    stari = []
    cuvant = ""
    tabel = {}


    def __init__(self, citit):
        self.cuvant = citit["cuvant"]
        for stare in citit["stari"]:
            self.stari.append(Stare(stare["nume"], stare["drum"]))


    def preiaCuvant(self):
        return self.cuvant


    def Pasul1(self):
        self.tabel[1] = {}
        for i in range(1, len(self.cuvant)+1):
            self.tabel[1][i] = []
            for stare in self.stari:
                if stare.preiaStareCuLitera(self.cuvant[i-1]):
                    self.tabel[1][i].append(stare.preiaNume())

    def reuniune(self, m1, m2):
        for val in m2:
            if val not in m1:
                m1.append(val)
        return m1


    def produs(self, m1, m2):
        rezultat = []
        for m1_elem in m1:
            for m2_elem in m2:
                elem_nou = m1_elem + m2_elem
                if elem_nou not in rezultat:
                    rezultat.append(elem_nou)
        return rezultat


    def preiaStariCuLitere(self, drum):
        stari = []
        for stare in self.stari:
            if stare.verificaNeterminal(drum):
                stari.append(stare.preiaNume())
        return stari

    def calcVij(self, i, j):
        rezultat = {}
        rezultat['final'] = []
        for k in range(1, j):
            tmp = self.produs(self.tabel[k][i], self.tabel[j-k][i+k])
            rezultat[k] = []
            for val in tmp:
                elem_nou = self.preiaStariCuLitere(val)
                rezultat[k] = self.reuniune(rezultat[k], elem_nou)
            rezultat['final'] = self.reuniune(rezultat['final'], rezultat[k])
        return rezultat['final']


    def run(self):
        self.Pasul1()
        for j in range(2,len(self.cuvant) + 1):
            self.tabel[j] = {}
            for i in range(1, len(self.cuvant) + 1):
                if not i + j <= len(self.cuvant) + 1:
                    break
                self.tabel[j][i] = self.calcVij(i, j)
        if self.stari[0].preiaNume() in self.tabel[len(self.cuvant)][1]:
            return True
        return False


    def afiseaza(self):
        print ('V(i,j)')
        for i in range(1, len(self.cuvant) + 1):
            print ('i = ' + str(i), end='\t |')
        print()
        for j in range(1, len(self.cuvant) + 1):
            print ('j = ' + str(j), end='\t |')
            for i in range(1, len(self.cuvant) + 1):
                if not i + j <= len(self.cuvant) + 1:
                    break
                print ('{', end='')
                for val in self.tabel[j][i]:
                    print (val, end=', ')
                print ('}', end=' | ')
            print ()
        print ('END')


if __name__ == "__main__":
    with open('gramatica.json') as f:
        data = json.load(f)
    cyk = AlgoCYK(data)
    print ('Cuvantul:' + str(cyk.preiaCuvant()) + ' ' + ('' if cyk.run() else ' NU ') + 'este acceptat')
    cyk.afiseaza()








