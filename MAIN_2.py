from datetime import datetime
from os import system as clean
from platform import system
from FUNKCJE_inicjalizacji import *
from WER_2 import *

def main():
    try:
        with open('grupy.bin', 'rb') as plik:
            grupy = read(plik)
    except FileNotFoundError:
        grupy = all_groups_maker()
        zapis_grup(grupy)
    nr_fun = 1
    while True:
        # główny wybór
        clean('clear')  # windows - cls
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
            clean('clear' if system() == "Linux" else "cls")
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
                           '9. Zmien grupe', '10. EXIT/ zapis punktu przywracania', '11. Ładowanie punktu przywracania']
            print(*str_funkcje, sep='\n')
            nr_fun = wejscie_ok('Wpisz nr od 1 do 10 >>', 1, 13)  #  todo 1 + len(str_funkcje))
            if nr_fun == -1:
                print("podaj poprawny numer funkcji")
                continue

            if nr_fun == 1:
                sel_group.podsum_grupy()
                sel_group.wykr_porown_szczury()
                a = input("nacisnij enter aby kontynuować")
                continue

            if nr_fun == 2:
                sel_group.wykres_grupy()
                a = input("nacisnij enter aby kontynuować")
                continue
            # todo co z nr 3
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
                sel_group.szczury[nr_szcz].wykres_szczura(sel_group.nazwa)
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
                    input_grupy = input('podaj numery grup (ciągiem) i nacisnij enter')
                    if not input_grupy.isnumeric():
                        print("nieprawidłowo podano numer grupy")
                        continue
                    grups_to_add = list(map(int, list(input_grupy)))
                    print(grups_to_add)
                    for i in grups_to_add:
                        if type(i) is int:
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
                    if input("czy chcesz zapisać zmiany na ten moment jako punkt przywracania? "
                             "(enter-nie/coś innego - tak"):
                        now = datetime.now()
                        zapis_grup(grupy, par=['DATA/restore/','grupy_'+ '-'.join(
                            list(map(str, [now.year, now.month, now.day, now.hour, now.minute, now.second])))])

                    else:
                        zapis_grup(grupy)
                        exit(0)

            if nr_fun == 11:
                rest_result = restore()
                grupy = grupy if rest_result == -1 else rest_result

            if nr_fun == 12:
                for grupa in grupy.values():
                        masakrator(grupa)

            if nr_fun == 13:
                print(sel_group.nazwa,len(sel_group.szczury),sel_group.zwrot_ok())



if __name__ == "__main__":
    # try:
        main()
        # raise MemoryError
    # except Exception as e:
    #     with open('errors.txt', 'w') as plik_errors:
    #         plik_errors.write(str(e))  # todo zapis całej wiadomości błędu
