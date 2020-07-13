from FUNKCJE_inicjalizacji import *
from WER_2 import *
from os import system as clean

# Todo mechanizm doboru parametrow

try:
    with open('grupy.bin', 'rb') as plik:
        grupy = read(plik)
except FileNotFoundError:
    grupy = all_groups_maker()
    zapis_grup(grupy)
nr_fun = 1
while True:
    # główny wybór
    clean('clear') # windows - cls
    print("wybierz grupę którą chcesz się zająć:")
    print("1 - GKC_w", "2 - GKR_w", "3 - SDC_w", "4 - SDR_w", "5 - GKC_m", "6 - GKR_m", "7 - SDC_m", "8 - SDR_m")
    g_n = ["1 - GKC_w", "2 - GKR_w", "3 - SDC_w", "4 - SDR_w", "5 - GKC_m", "6 - GKR_m", "7 - SDC_m", "8 - SDR_m"]
    nr_gr = wejscie_ok("Wpisz nr od 1 do 8 >>", 1, 8)
    if nr_gr != -1:
        sel_group = grupy[group_name(nr_gr)]
    else:
        print("podaj poprawny numer grupy")
        continue
    while True:
        clean('clear')  # windows - cls
        if nr_fun in (5, 6, 7):
            sel_group.aktualizacja_D()
            with open('grupy.bin', 'rb') as plik:
                zapis_grup(grupy)
        print("WYBRANA GRUPA :    ", sel_group.nazwa)
        print("Wybierz funkcje:")
        str_funkcje = ['1. Pokaż podsumowanie grupy', '2.Pokaż wykres grupy i jej dane',
                       "3.Pokaż zestawienie jednego szczura z innymi",
                       "4. Pokaż wykres pojedyńczego szczura i jego dane",
                       '5. Dezaktywuj/ aktywuj punkt w grupie', '6. Dezaktywuj/ aktywuj szczura',
                       '7. Dezaktywuj/ aktywuj punkt w szczurze', '8. Stwórz pliki pdf uwzględniając zmiany',
                       '9. Zmien grupe', '10. EXIT']
        print(*str_funkcje, sep='\n')
        nr_fun = wejscie_ok('Wpisz nr od 1 do 10 >>', 1, 10)
        if nr_fun == -1:
            print("podaj poprawny numer grupy")
            continue

        if nr_fun == 1:
            sel_group.podsum_grupy()
            a = input("nacisnij enter aby kontynuować")
            continue

        if nr_fun == 2:
            sel_group.wykres_grupy()
            a = input("nacisnij enter aby kontynuować")
            continue

        if nr_fun == 3:
            il_szcz = len(sel_group.szczury) - 1
            nr_szcz = wejscie_ok("podaj nr szczura do zestawienia (od 0 do " + str(il_szcz) + ">> ",
                                 0, il_szcz)
            if nr_szcz == -1:
                print('niepoprawny numer szczura')
                continue
            zmiany = True
            if input("uwzglednic zmiany? (enter-tak / cos innego - nie>>"):
                zmainy = False
            sel_group.wykr_porown_szczury(nr_szcz)
            continue

        if nr_fun == 4:
            il_szcz = len(sel_group.szczury) - 1
            nr_szcz = wejscie_ok("podaj nr szczura (od 0 do " + str(il_szcz) + ">> ",
                                 0, il_szcz)
            if nr_szcz == -1:
                print('niepoprawny numer szczura')
                continue
            szer_pola = 9
            po_przecinku = 6
            print("Szczur {:2}".format(nr_szcz), '> B', 8 * ' ' + '\t', 'B/F', 6 * ' ', 'aktywnosc punktu')
            for nr_pkt_w_szczurze, [b, f, ok] in enumerate(
                    zip(sel_group.szczury[nr_szcz].By, sel_group.szczury[nr_szcz].Fy,
                        sel_group.szczury[nr_szcz].ok)):
                str2prt = 'pkt nr> {0:2} '
                for os in ('1', '2'):
                    str2prt += '{' + os + ':' + str(szer_pola) + '.' + str(po_przecinku) + 'f}|\t'
                str2prt += '{3}'
                print(str2prt.format(nr_pkt_w_szczurze, b, f, ok))
            sel_group.szczury[nr_szcz].wykres_szczura()
            a = input("nacisnij enter aby kontynuować")
            continue

        if nr_fun == 5:
            il_pkt = len(sel_group.By) - 1
            nr_pkt = wejscie_ok("podaj nr punktu do (dez)aktywacji (od 0 do " + str(il_pkt) + ">> ",
                                0, il_pkt)
            if nr_pkt == -1:
                print('niepoprawny numer punktu')
                continue
            if input('dezaktywacja - enter / aktywacja - cos innego>>'):
                sel_group.aktywuj_pkt(nr_pkt)
            else:
                sel_group.dezaktywuj_pkt(nr_pkt)
            a = input("nacisnij enter aby kontynuować")
            continue

        if nr_fun == 6:
            il_szcz = len(sel_group.szczury) - 1
            nr_szcz = wejscie_ok("podaj nr szczura do (dez)aktywacji (od 0 do " + str(il_szcz) + ">> ",
                                 0, il_szcz)
            if nr_szcz == -1:
                print('niepoprawny numer szczura')
                continue
            if input('dezaktywacja - enter / aktywacja - cos innego>>'):
                sel_group.szczury[nr_szcz].aktywuj_szcz()
            else:
                sel_group.szczury[nr_szcz].dezaktywuj_szcz()
            a = input("nacisnij enter aby kontynuować")
            continue

        if nr_fun == 7:
            il_szcz = len(sel_group.szczury) - 1
            nr_szcz = wejscie_ok("podaj nr szczura (od 0 do " + str(il_szcz) + ">> ",
                                 0, il_szcz)
            if nr_szcz == -1:
                print('niepoprawny numer szczura')
                continue
            il_pkt = len(sel_group.By)
            nr_pkt = wejscie_ok("podaj nr punktu do (dez)aktywacji (od 0 do " + str(il_pkt) + ">> ",
                                0, il_pkt)
            if nr_pkt == -1:
                print('niepoprawny numer punktu')
                continue
            if input('dezaktywacja - enter / aktywacja - cos innego>>'):
                sel_group.szczury[nr_szcz].aktywuj_pkt(nr_pkt)
            else:
                sel_group.szczury[nr_szcz].dezaktywuj_pkt(nr_pkt)
            a = input("nacisnij enter aby kontynuować")
            sel_group.szczury[nr_szcz].aktualizacja_S()
            continue

        if nr_fun == 8:
            if input("czy chcesz wybrac grupy do dolaczenia? (enter - tak, cos innego - nie>>"):
                pdf_maker([sel_group])
            else:
                print("wybierz grupy ktore chcesz dołaczyć:")
                print("1 - GKC_w", "2 - GKR_w", "3 - SDC_w", "4 - SDR_w", "5 - GKC_m", "6 - GKR_m", "7 - SDC_m",
                      "8 - SDR_m", )
                grups_to_add = list(map(int, input('podaj numery grup po spacji i nacisnij enter').split(' ')))
                print(grups_to_add)
                for i in grups_to_add:
                    if 1 > i or i > 8:
                        grups_to_add = -1
                if -1 in grups_to_add:
                    print("wprowadzono niepoprawny numer grupy")
                    continue
                grups = [grupy[group_name(i)] for i in grups_to_add]
                if sel_group not in grups:
                    grups.append(sel_group)
                pdf_maker(grups)
            a = input("nacisnij enter aby kontynuować")
            continue

        if nr_fun == 9:
            break
        if nr_fun == 10:
            with open('grupy.bin', 'rb') as plik:
                sel_group.aktualizacja_D()
                zapis_grup(grupy)
                exit(0)
