from WER_2 import Grupa, Szczur
from pickle import dump as save
from copy import deepcopy as dcopy


def import_grupy(nazwa_grupy):
    """
    pobiera dane
    :return: lista zawierajaca [ B,B/F]
    B, B/F - listy wartosci B dla punktów
    wartosci dla dago punktu
    """
    wszystkie_dane = []
    with open('DATA/' + nazwa_grupy + '.txt') as plik:
        liniki = plik.readlines()
    polowa_pliku = []
    for nr_lini in range(len(liniki)):
        liniki[nr_lini] = liniki[nr_lini].replace(',', '.').replace('\n', '')
        if liniki[nr_lini] == '-':
            wszystkie_dane.append(polowa_pliku)
            polowa_pliku = []
            continue
        try:
            polowa_pliku.append(list(map(float, liniki[nr_lini].split('\t'))))
        except:
            pass
    return wszystkie_dane


def inicjalizacja_grupy(pobrane_dane, nazwa):
    """
    tworzy grupe z szczurami i inicjalizuje :
        nazwe,ok,by,fy,semy_pkt,parametry,outputy,semy outputow i stale  - grupy
        by, fy,ok,semy,nr - szczura
    :param
        pobrane_dane: to co zwraca funkcja import_grupy()[ B [ punkty [ wart ] ] ]
        nazwa: nazwa grupy - string
    :return: grupa ze szczurami i podstawowymi danymi
    """
    grupa = Grupa()

    ilosc_szczurow = len(pobrane_dane[0][0])
    for nr_szczura in range(ilosc_szczurow):
        grupa.szczury.append(Szczur())
        szczur = grupa.szczury[nr_szczura]
        ilosc_punktow = len(pobrane_dane[0])
        for nr_punktu in range(ilosc_punktow):
            szczur.By.append(pobrane_dane[0][nr_punktu][nr_szczura])
            szczur.Fy.append(pobrane_dane[1][nr_punktu][nr_szczura])
        szczur.ok = [True for i in range(ilosc_punktow)]
        szczur.nazwa = nr_szczura
        szczur.semy = [0.001 for i in range(ilosc_punktow)]
        szczur.semy_punktow = [0 for i in range(len(szczur.By))]
        szczur.obl_parametry(*szczur.zwrot_ok()[:2])
        szczur.obl_output(szczur.parametry)
        szczur.parametry_O = dcopy(szczur.parametry)
        szczur.outputy_O = dcopy(szczur.outputy)

    grupa.nazwa = nazwa
    grupa.ok = [True for i in range(len(grupa.szczury[0].ok))]
    grupa.obl_sr_By_Fy_i_semy_pkt_grupy()
    grupa.semy_punktow_O = dcopy(grupa.semy_punktow)
    grupa.obl_parametry(*grupa.zwrot_ok()[0:2])
    grupa.parametry_O = dcopy(grupa.parametry)
    grupa.obl_outputy_sr()
    grupa.outputy_O = dcopy(grupa.outputy)
    grupa.obl_semy_outputow()
    grupa.semy_outputow_O = dcopy(grupa.semy_outputow)
    for szczur in grupa.szczury:
        szczur.semy_punktow = [0] * len(grupa.Fy)

    return grupa

def all_groups_maker():
    """
    tworzy slownik zawierajacy grupy - klucze to numery z nazwy
    :return: dict consist all groups
    """
    GRUPY = {}
    nazwy = ["1 - GKC_w", "2 - GKR_w", "3 - SDC_w", "4 - SDR_w", "5 - GKC_m", "6 - GKR_m", "7 - SDC_m", "8 - SDR_m"]
    for nazwa_grupy in nazwy:
        GRUPY.update({nazwa_grupy: inicjalizacja_grupy(import_grupy(nazwa_grupy), nazwa_grupy)})
    return GRUPY


def zapis_grup(grupy, par=None):
    if par is None:
        par = ['', '']
    with open(par[0] + "grupy" + par[1] + ".bin", 'wb') as plik:
        save(grupy, plik)
