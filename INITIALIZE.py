from funkcje import *
import pickle

with open("grupy.bin", "rb") as plik:
    grupy = pickle.load(plik)

for i in range(8):
    try:
        grupy[i].semk1,grupy[i].semk2,grupy[i].semr1,grupy[i].semr2 = kkrr(grupy[i],w = False)
    except:
        print(grupy[i].nazwa)
    # sr b i f dla pkt
    grupy[i].sreB,grupy[i].sre = sr_BF(grupy[i])
    grupy[i].semy = sem_gr(grupy[i])
    grupy[i].parametry = c_fit(scatchard_curv,grupy[i].sreB,grupy[i].sre,grupy[i].semy)
    a,b,c,d = parametry_rownanie(grupy[i].parametry)[:4]
    grupy[i].k1sr,grupy[i].k2sr,grupy[i].r1sr,grupy[i].r2sr = -a,-b,c,d
    as_tabl = parametry_rownanie(grupy[i].parametry)
    grupy[i].as1,grupy[i].as2 = Prosta(as_tabl[0],as_tabl[4]),Prosta(as_tabl[1],as_tabl[5])

# zapis _o
for i in range(len(grupy)):
    grupy[i].sre_o = grupy[i].sre
    grupy[i].sreB_o = grupy[i].sreB
    grupy[i].semy_o = grupy[i].semy
    grupy[i].k1sr_o = grupy[i].k1sr
    grupy[i].k2sr_o = grupy[i].k2sr
    grupy[i].r1sr_o = grupy[i].r1sr
    grupy[i].r2sr_o = grupy[i].r2sr
    grupy[i].parametry_o = grupy[i].parametry
    grupy[i].semk1_o = grupy[i].semk1
    grupy[i].semk2_o = grupy[i].semk2
    grupy[i].semr1_o = grupy[i].semr1
    grupy[i].semr2_o = grupy[i].semr2
    grupy[i].as1_o = grupy[i].as1
    grupy[i].as2_o = grupy[i].as2
    with open("grupy.bin", "wb") as plik:
        pickle.dump(grupy, plik)

# WYKRESY + WARTOSCI
# for i in range(4):
#     wykres([grupy[2*i],grupy[2*i+1]])
#     print('  ',grupy[2*i].nazwa,  grupy[2*i+1].nazwa,'       ',grupy[2*i].nazwa,  grupy[2*i+1].nazwa,)
#     print('K1', round(grupy[2*i].k1sr,5),'[+_]' ,round(grupy[2*i].semk1,6), round(grupy[2*i+1].k1sr,5),'[+_]'  '',round(grupy[2*i+1].semk1,6),
#                                         '\tk2: ', round(grupy[2*i].k2sr,5),'[+_]',round(grupy[2*i].semk2,6), round(grupy[2*i+1].k2sr,5),'[+_]',round(grupy[2*i+1].semk2,6))
