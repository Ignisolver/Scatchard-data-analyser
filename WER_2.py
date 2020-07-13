import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
from pickle import load as read, dump as save


# todo przetestowac funkcje
# TODO napisac program glowny 1 kartka

class Dane:
    def __init__(self):
        # Lista zawierająca argumenty funkcji ( wartosci pionowe z tabeli danych z B)
        # dla szczura - jego wartosci    /   dla grupy - wartosci srednie
        self.Fy = []
        # Lista zawierająca wartosci funkcji  ( wartosci pionowe z tabeli danych z B/F)
        # dla szczura - jego wartosci    /   dla grupy - wartosci srednie
        self.semy_punktow = []
        # Lista zawierająca wartosci SEM dla kazdego punktu (only Fy) ( dlugosc pionu )
        # same 0.0001 dla szczorów
        self.semy_punktow_O = []
        # Lista zawierająca orginalne wartosci SEM dla kazdego punktu (only Fy)( dlugosc pionu )
        # same 0.0001 dla szczorów
        self.semy_punktow_V2 = []
        # Lista zawierająca wartosci SEM dla kazdego punktu (only Fy) ( dlugosc pionu )
        # same 0.0001 dla szczorów
        self.semy_outputow = {'k1': None, 'k2': None, 'r1': None, 'r2': None}
        ## Słownik zawierający wartosci SEM : k1,r1,k2,r2
        # dla grupy - wartosci srednie
        self.nazwa = ''
        # string - nr szczura/nazwa grupy
        self.By = []
        self.semy_outputow_O = {'k1': None, 'k2': None, 'r1': None, 'r2': None}
        ## Słownik zawierający orginalne wartosci SEM : k1,r1,k2,r2
        # dla grupy - wartosci srednie
        self.outputy = {'k1': None, 'k2': None, 'r1': None, 'r2': None}
        # Słownik zawierający wartosci: k1,r1,k2,r2
        # dla grupy - wartosci srednie
        self.outputy_O = {'k1': None, 'k2': None, 'r1': None, 'r2': None}
        # Słownik zawierający oryginalne wartosci: k1,r1,k2,r2
        # dla grupy - wartosci srednie
        self.parametry = []
        # Lista zawierajaca parametry hiperboli: a, b, d, e
        self.parametry_O = []
        # Lista orginalnych parametrow
        self.ok = []
        # Lista zawierająca info o tym czy dany punkt (z By,Fy) jest uwzględniany przy liczeniu sem/ parametrow/ outputow
        self.klasa = "Dane"

    def obl_output(self):
        """
        oblicza k1,k2,r1,r2 i zapisuje w grupie
        :param parametry: a,b,d,e
        :return: None
        """
        a, b, d, e = self.parametry
        delta = abs(b ** 2 - 4 * a) ** (1 / 2)
        k1 = (b - delta) / 2
        k2 = b - k1
        r1 = (d - e * k1) / (k1 ** 2 - k1 * k2)
        r2 = (e + k1 * r1) / (-k2)
        nazwy_outputow = ['k1', 'k2', 'r1', 'r2']
        wart_outputow = [k1, k2, r1, r2]
        for nr_out in range(len(nazwy_outputow)):
            self.outputy[nazwy_outputow[nr_out]] = wart_outputow[nr_out]

    def obl_parametry(self):
        """
        dopasowuje parametry funkcji scatcharda do danych b i b/F
        :return: zapisuje parametry
        """
        # if self.nazwa == "Szczur":
        #     sigma = [0.001 for i in range(len(self.By))]
        parametry_wejsciowe = np.array([1, 5, 1, 5])
        self.parametry = curve_fit(scatchard_curv, self.zwrot_ok()[0], self.zwrot_ok()[1], p0=parametry_wejsciowe)[0]

    def zwrot_ok(self):
        """
        zwraca wartosci srednir by i fy punktow ktore sa aktywne
        :return: [aktywne_by, aktywne Fy, semy aktywnych Fy]
        """
        by = [self.By[i] for i in range(len(self.By)) if self.ok[i]]
        fy = [self.Fy[i] for i in range(len(self.Fy)) if self.ok[i]]
        fy_s = [self.semy_punktow[i] for i in range(len(self.Fy)) if self.ok[i]]
        return [by, fy, fy_s]

    def dezaktywuj_pkt(self, nr):
        self.ok[nr] = False

    def aktywuj_pkt(self, nr):
        self.ok[nr] = True

    # jedynie deklaracje:

    def obl_semy_outputow(self):
        pass

    def obl_sr_sem_byify(self):
        pass

    def obl_sr_By_Fy_i_semy_pkt_grupy(self):
        pass

    def aktualizacja_D(self):
        self.obl_sr_By_Fy_i_semy_pkt_grupy()
        self.obl_parametry()
        self.obl_output()
        self.obl_semy_outputow()


class Grupa(Dane):
    def __init__(self):
        super().__init__()
        self.szczury = []
        self.klasa = "Grupa"
        # Lista zawierajaca obiekty szczorow danej grupy

    def obl_sr_sem_byify(self):
        """
        oblicza srednie wartosci by i fy z aktywnych szczurow i je zapisuje
        :return: None
        """
        by_punktow = list(zip(
            *[self.szczury[i].By for i in range(len(self.szczury)) if self.szczury[i].aktywnosc == 1]))
        fy_punktow = list(zip(
            *[self.szczury[i].Fy for i in range(len(self.szczury)) if self.szczury[i].aktywnosc == 1]))
        self.By = [sum(i) / len(i) for i in by_punktow]
        self.Fy = [sum(i) / len(i) for i in fy_punktow]
        self.semy_punktow = [sem(lista) for lista in fy_punktow]

    def obl_semy_outputow(self):
        """
        zapisuje semy outputow uwzgledniajac aktywne szczury
        :return:none
        """
        outputs_dict = {'k1': None, 'k2': None, 'r1': None, 'r2': None}
        il_szczurow = len(self.szczury)
        for out in outputs_dict:
            lista = [self.szczury[i].outputy[out] for i in range(il_szczurow) if self.szczury[i].aktywnosc == 1]
            self.semy_outputow.update({out:sem(lista)})

    def obl_sr_By_Fy_i_semy_pkt_grupy(self):
        '''
        oblicza i zaapisuje srednie wartosci by i fy dla danej grupy na podstawie danych w szczurach
        uwzglednia zmiany
        :return:
        '''
        sr_by = []
        sr_fy = []
        semy_fy = []
        for nr_pkt in range(len(self.szczury[0].By)):
            sumab = 0
            sumaf = 0
            listaf = []
            il_szczurow = len(self.szczury)
            for szczur in self.szczury:
                if szczur.ok[nr_pkt] is False:
                    print(szczur.nazwa,nr_pkt)
                if szczur.aktywnosc and szczur.ok[nr_pkt]:
                    sumab += szczur.By[nr_pkt]
                    sumaf += szczur.Fy[nr_pkt]
                    listaf.append(szczur.Fy[nr_pkt])
            sr_by.append(sumab / il_szczurow)
            sr_fy.append(sumaf / il_szczurow)
            semy_fy.append(sem(listaf))

        self.By = sr_by
        self.semy_punktow = semy_fy
        self.Fy = sr_fy

    def podsum_grupy(self):
        '''
        podsumowuje grupe printujac najwazniejsze dane czyli
        nazwa
        wartosci k i r wraz z semami
        pkazuje wyniki wszystkich szczurów .....
        :return: nic
        '''
        # grupa jako calosc
        print("GRUPA:", self.nazwa)
        # tworzenie stringa do sprintowania
        str2prt = ''
        szer_pola = 11
        po_przecinku = 6
        print(8 * ' ', "K1", "K2", "R1", "R2", sep=11 * ' ')
        for par in ('k1', 'k2', 'r1', 'r2'):
            str2prt +='{0[' + par + ']:' + str(szer_pola) + '.' + str(po_przecinku) + 'f}\t'
        print(4*' ' + "Wartości: ", end='')
        print(str2prt.format(self.outputy))
        print(4*' ' + "   SEM-y: ", end='')
        print(str2prt.format(self.semy_outputow))

        # grupa jako kazdy osobno
        print(8 * ' ', "K1", "K2", "R1", "R2", sep=12 * ' ',end='')
        print(6*' ',"AKT")
        for nr, szczur in enumerate(self.szczury):
            str2prt = 'szcz_nr > ' + str(nr) + '<# '
            szer_pola = 11
            po_przecinku = 6
            for par in ('k1', 'k2', 'r1', 'r2'):
                str2prt += '{0[' + par + ']:' + str(szer_pola) + '.' + str(po_przecinku) + 'f} | '
            print(str2prt.format(szczur.outputy), szczur.aktywnosc)


    def wykres_grupy(self,zakres = None):
        '''
        tworzy wykres grupy z errorbarami razem dla zmian(ziel) i bez nich(nieb)
        :param [zakres = False] format: [[xmin,xmax],[ymin,ymax]] gdy zamiast krotki flasz - automatyczne
         uwzglednia zakres lub nie
        :return:
        '''
        # format errorbarow z daszkiem
        plt.rcParams.update({'errorbar.capsize': 3})
        plt.errorbar(self.By, self.Fy, self.semy_punktow_O, fmt='b*', ecolor='b')
        plt.errorbar(*self.zwrot_ok(), fmt='g*', ecolor='g')
        # rysowanie lini
        x = np.linspace(min(self.By), max(self.By), 500)
        y_zm = [scatchard_curv(i, *self.parametry) for i in x]
        y = [scatchard_curv(i, *self.parametry_O) for i in x]
        plt.plot(x, y, 'b')
        plt.plot(x, y_zm, 'g-')
        plt.legend(('bez zmian','ze zmianami'), loc='upper right')
        szer_pola = 9
        po_przecinku = 6
        for nr_pkt_w_szczurze, [b, f, ok] in enumerate(zip(self.By, self.Fy,
                                                           self.ok)):
            str2prt = 'pkt nr> {0:2} '
            for os in ('1', '2'):
                str2prt += '{' + os + ':' + str(szer_pola) + '.' + str(po_przecinku) + 'f}|\t'
            str2prt += '{3}'
            print(str2prt.format(nr_pkt_w_szczurze, b, f, ok))

        numery = []
        for nr in range(len(self.By)):
            if self.ok[nr]:
                numery.append(nr)
        #bez tego sie robia brzydkie wykresy z naniesionymi cyframi - to zostawia tylko te w zakresie
        for nr,(x,y) in list(zip(numery,list(zip(*self.zwrot_ok()[:2])))):
            if bool(zakres):
                if zakres[1][0] is not False:
                    if zakres[1][0] <= y <= zakres[1][1]:
                        if zakres[0][0] is not False:
                            if zakres[0][0] <= x <= zakres[0][1]:
                                plt.text(x, y, str(nr))
                        else:
                            plt.text(x, y, str(nr))
                elif zakres[0][0] is not False:
                    if zakres[0][0] <= x <= zakres[0][1]:
                        plt.text(x, y, str(nr))
            else:
                plt.text(x, y, str(nr))


        if bool(zakres):
            if zakres[1][0] is not False:
                plt.ylim(zakres[1][0], zakres[1][1])
            if zakres[0][0] is not False:
                plt.xlim(zakres[0][0], zakres[0][1])
        plt.title("grupa " + self.nazwa)
        plt.grid()
        plt.show()

    def wykr_porown_szczury(self, nr, zmiany=True):

        '''
        funkcja pokazujaca wykresy wszystkich szczurow
        dany numerem szczur na czerwono
        reszta na niebiesko
        zmiany lub bez nich sa okreslane paremetrem
        :param nr: numer szczura do zestawienia z reszta
        :param zmiany: = True - pokazuje wykres ze zmianami, Flase - bez zmian
        :return: nic nie zwraca
        '''
        if zmiany:
            for ind, szczur in enumerate(self.szczury):
                if szczur.aktywnosc and ind != nr:
                    kolor = 'b'

                    x = np.linspace(min(szczur.By), max(szczur.By), 1000)
                    y = [scatchard_curv(i, *szczur.parametry) for i in x]

                    plt.plot(x, y, kolor + '-')
                    # plt.plot(*szczur.zwrot_ok()[:2], kolor + '*')
            # dla wybranego szczura
            kolor = 'r'
            x = np.linspace(min(self.szczury[nr].By), max(self.szczury[nr].By), 1000)
            y = [scatchard_curv(i, *self.szczury[nr].parametry) for i in x]
            plt.plot(x, y, kolor + '-')
            # plt.plot(*self.szczury[nr].zwrot_ok()[:2], kolor + '*')
        else:
            for ind, szczur in enumerate(self.szczury):
                kolor = 'r' if ind == nr else 'b'

                x = np.linspace(min(szczur.By), max(szczur.By), 1000)
                y_O = [scatchard_curv(i, *szczur.parametry_O) for i in x]

                plt.plot(x, y_O, kolor + '-')
                # plt.plot(szczur.By, szczur.Fy, kolor + '*')
            kolor = 'r'
            x = np.linspace(min(self.szczury[nr].By), max(self.szczury[nr].By), 1000)
            y = [scatchard_curv(i, *self.szczury[nr].parametry_O) for i in x]
            plt.plot(x, y, kolor + '-')
            # plt.plot(self.szczury[nr].By, self.szczury[nr].Fy, kolor + '*')
        plt.title('szczur nr ' + str(nr) + ' na czerwowno')
        plt.grid()
        plt.show()

    def mediana(self):
        '''
        liczy mediane k i r z tablicy szczurów
        :return: float mediana
        '''



class Szczur(Dane):
    def __init__(self):
        super().__init__()
        self.aktywnosc = True
        self.klasa = "Szczur"
        # info czy dany szczur ma wplyw na wyniki grupy

    def dezaktywuj_szcz(self):
        self.aktywnosc = False

    def aktywuj_szcz(self):
        self.aktywnosc = True

    def wykres_szczura(self, zakres = None):
        '''
        rysuje wykres pojedynczego szczura ze zmianami (zielony) i bez nich (niebieski)
        :param [zakres = None] format: [[xmin,xmax],[ymin,ymax]] gdy zamiast krotki flasz - automatyczne
         uwzglednia zakres lub nie
        :return: nic
        '''
        if zakres is None:
            zakres = []
        x = np.linspace(min(self.By)-0.1, max(self.By), 1000)

        y = [scatchard_curv(i, *self.parametry) for i in x]
        y_O = [scatchard_curv(i, *self.parametry_O) for i in x]
        plt.plot(x, y, 'b-')
        plt.plot(x, y_O, 'r-')
        plt.legend(("ze zmianami", 'bez zmian'), loc='upper right')

        numery = []
        for nr in range(len(self.By)):
            if self.ok[nr]:
                numery.append(nr)

        for nr,(x,y) in list(zip(numery, list(zip(*self.zwrot_ok()[:2])))):
            plt.text(x,y,str(nr))
        plt.plot(self.By, self.Fy, 'b*')
        plt.plot(*self.zwrot_ok()[:2], "r*")
        if zakres:
            if zakres[0][0] is not False:
                plt.xlim(zakres[0][0], zakres[0][1])
            if zakres[1][0] is not False:
                plt.ylim(zakres[1][0], zakres[1][1])
        plt.title("szczur nr:" + str(self.nazwa))
        plt.grid()
        plt.show()

    def aktualizacja_S(self):
        self.obl_sr_By_Fy_i_semy_pkt_grupy()
        self.obl_parametry()
        self.obl_output()

nazwy = ["1 - GKC_w", "2 - GKR_w", "3 - SDC_w", "4 - SDR_w", "5 - GKC_m", "6 - GKR_m", "7 - SDC_m", "8 - SDR_m"]


def scatchard_curv(x, a, b, d, e):
    """
    warring for absolute delta
    :param x: argument
    :params a, b, c, d: function parameters
    :return: value of the scatchard function
    """
    A = 1
    B = e + b * x
    C = a * x * x + d * x
    delta = abs(B * B - 4 * A * C)
    return -B / (2 * A) + (delta ** (1 / 2)) / (2 * A)


def pdf_maker(grupy, zmiany=True):
    '''
    tworzy pdfy z danych w liscie grup
    :param grupy: lista grup
    :param zmiany: wykesy bez/z zmianami
    :return: zapisuje pdfy
    '''
    plt.rcParams.update({'errorbar.capsize': 3})
    colors = ['r', 'b', 'g', 'm', 'y', 'k']
    color = colors[0]
    c_nr = 0
    if zmiany:
        mx = max([max(grupa.zwrot_ok()[0]) for grupa in grupy])
        my = max([max(grupa.zwrot_ok()[1]) for grupa in grupy])
        x = np.linspace(0, mx, 500)
        for grupa in grupy:
            color = colors[c_nr]
            y = [scatchard_curv(i, *grupa.parametry_O) for i in x]
            plt.errorbar(grupa.zwrot_ok()[0], grupa.zwrot_ok()[1], grupa.zwrot_ok()[2],fmt=color + '*', ecolor=color)
            plt.plot(x, y, color + '-')
            c_nr += 1
    else:
        mx = max([max(i) for grupa in grupy for i in grupa.By])
        my = max([max(i) for grupa in grupy for i in grupa.Fy])
        x = np.linspace(0, mx, 500)
        for grupa in grupy:
            color = colors[c_nr]
            y = [scatchard_curv(i, *grupa.pmarametry) for i in x]
            plt.errorbar(grupa.By, grupa.Fy, grupa.semy_punktow, fmt=color + '*', ecolor=color)
            plt.plot(x, y, 'r-')
            c_nr += 1
    nazwa = ''
    for grupa in grupy:
        nazwa += '+' + grupa.nazwa[3:]
    nazwa = nazwa[2:]

    plt.xlim(-1, mx + 1)
    plt.ylim(0, my * 10 / 9)
    # plt.legend("legenda", loc='upper right')
    plt.xlabel('Bound Insulin (nmol/l)')
    plt.ylabel("Bound/Free Insulin")
    plt.grid()
    plt.title(nazwa)
    plt.savefig("./wykresy/" + nazwa + ".svg", quality=95, format='svg')
    plt.show()


def zapis_grup(grupy):
    '''
    zapisue grupy w pliku grupy.bin
    :param grupy: grupy jako slownik
    :return: nic
    '''
    with open("grupy.bin", 'wb') as plik:
        save(grupy, plik)


def odczyt_grup():
    '''
    odczytuje grupy z pliku grupy.bin
    :return: grupy jako slownik
    '''
    with open("grupy.bin", 'rb') as plik:
        grupy = read(plik)
    return grupy


def sem(lista):
    '''
    oblicza sem zadanej listy z brzydkiego wzorku
    :param lista: lista wartosci
    :return: sem listy
    '''
    return (sum([(x - sum(lista) / len(lista)) ** 2 for x in lista]) /
            (len(lista) - 1)) ** (1 / 2) / len(lista) ** (1 / 2)


def wejscie_ok(string, min, max):
    '''
    zwraca podana wartosc jako int jezeli
     da sie ja zkonwertowac i jest w przedziale zamnietym <min,max>
      jak sie nieda lub jest z poza przedzialu to 0
    :param string: input
    :param min: minimalna wartosc
    :param max: maxymalna wartosc
    :return: int
    '''
    try:
        string = int(input(string))
        string = string if min <= string <= max else -1
    except:
        string = -1
    return string

def gn(nr):
    return ["1 - GKC_w", "2 - GKR_w", "3 - SDC_w", "4 - SDR_w", "5 - GKC_m", "6 - GKR_m", "7 - SDC_m", "8 - SDR_m"][nr-1]

def ii(str):
    try:
        return float(input(str))
    except:
        return False