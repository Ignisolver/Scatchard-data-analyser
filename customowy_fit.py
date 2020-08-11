import numpy as np
import matplotlib.pyplot as mpl
import random as rnd

#Uwaga! funkcje są w pełni znumpajowane, więc i skrajnie nieczytelne. Za długie czytanie może kutkowac bólem głowy.

def F(x, k_1, k_2, q_1, q_2):
    # definicja krzywej scatcharda
    y = np.divide(np.add(np.subtract(np.add(np.sqrt(np.add(np.subtract(np.power(np.add(np.sum(np.multiply(k_2,q_2),),np.multiply(k_1,q_1)),2),np.multiply(2,np.multiply(np.subtract(k_1,k_2),np.multiply(x,np.subtract(np.multiply(k_1,q_1),np.multiply(k_2,q_2)))))),np.multiply(np.power(np.subtract(k_1,k_2),2),np.power(x,2)))),np.multiply(k_2,q_2)),np.multiply(np.add(k_2,k_1),x)),np.multiply(k_1,q_1)),2)
    return y


def dF_Dk_1(x, k_1, k_2, q_1, q_2):
    # pochodna po k_1
    y = np.add(np.subtract(np.divide(np.subtract(np.add(np.subtract(np.multiply(2,np.multiply(q_1,np.add(np.multiply(q_1,k_1),np.multiply(k_2,q_2)))),np.multiply(2,np.multiply(x,np.subtract(np.multiply(q_1,k_1),np.multiply(k_2,q_2))))),np.multiply(2,np.multiply(np.power(x,2),np.subtract(k_1,k_2)))),np.multiply(2,np.multiply(q_1,np.multiply(x,np.subtract(k_1,k_2))))),np.multiply(4,np.sqrt(np.subtract(np.add(np.power(np.add(np.multiply(q_1,k_1),np.multiply(k_2,q_2)),2),np.multiply(np.power(x,2),np.power(np.subtract(k_1,k_2),2))),np.multiply(2,np.multiply(x,np.multiply(np.subtract(k_1,k_2),np.subtract(np.multiply(q_1,k_1),np.multiply(k_2,q_2))))))))),np.divide(x,2)),np.divide(q_1,2))
    return y


def dF_Dk_2(x, k_1, k_2, q_1, q_2):
    # pochodna po k_2
    y = np.add(np.subtract(np.divide(np.add(np.subtract(np.add(np.multiply(2,np.multiply(q_2,np.add(np.multiply(q_2,k_2),np.multiply(k_1,q_1)))),np.multiply(2,np.multiply(x,np.subtract(np.multiply(k_1,q_1),np.multiply(q_2,k_2))))),np.multiply(2,np.multiply(np.power(x,2),np.subtract(k_1,k_2)))),np.multiply(2,np.multiply(q_2,np.multiply(x,np.subtract(k_1,k_2))))),np.multiply(4,np.sqrt(np.add(np.subtract(np.power(np.add(np.multiply(q_2,k_2),np.multiply(k_1,q_1)),2),np.multiply(2,np.multiply(x,np.multiply(np.subtract(k_1,k_2),np.subtract(np.multiply(k_1,q_1),np.multiply(q_2,k_2)))))),np.multiply(np.power(x,2),np.power(np.subtract(k_1,k_2),2)))))),np.divide(x,2)),np.divide(q_2,2))
    return y


def dF_Dq_1(x, k_1, k_2, q_1, q_2):
    # pochodna po q_1
    y = np.add(np.divide(np.subtract(np.multiply(2,np.multiply(k_1,np.add(np.multiply(k_1,q_1),np.multiply(k_2,q_2)))),np.multiply(2,np.multiply(k_1,np.multiply(np.subtract(k_1,k_2),x)))),np.multiply(4,np.sqrt(np.add(np.subtract(np.power(np.add(np.multiply(k_1,q_1),np.multiply(k_2,q_2)),2),np.multiply(2,np.multiply(np.subtract(k_1,k_2),np.multiply(x,np.subtract(np.multiply(k_1,q_1),np.multiply(k_2,q_2)))))),np.multiply(np.power(np.subtract(k_1,k_2),2),np.power(x,2)))))),np.divide(k_1,2))
    return y


def dF_Dq_2(x, k_1, k_2, q_1, q_2):
    # pochodna po q_2
    y = np.add(np.divide(np.add(np.multiply(2,np.multiply(k_2,np.add(np.multiply(k_2,q_2),np.multiply(k_1,q_1)))),np.multiply(2,np.multiply(np.subtract(k_1,k_2),np.multiply(k_2,x)))),np.multiply(4,np.sqrt(np.add(np.subtract(np.power(np.add(np.multiply(k_2,q_2),np.multiply(k_1,q_1)),2),np.multiply(2,np.multiply(np.subtract(k_1,k_2),np.multiply(x,np.subtract(np.multiply(k_1,q_1),np.multiply(k_2,q_2)))))),np.multiply(np.power(np.subtract(k_1,k_2),2),np.power(x,2)))))),np.divide(k_2,2))
    return y


def row(x, k_1, k_2, q_1, q_2):
    #funkcja generująca rząd macierzy M
    return [dF_Dk_1(x, k_1, k_2, q_1, q_2), dF_Dk_2(x, k_1, k_2, q_1, q_2), dF_Dq_1(x, k_1, k_2, q_1, q_2),
            dF_Dq_2(x, k_1, k_2, q_1, q_2)]


def make_M(x, k_1, k_2, q_1, q_2):
    #składa macierz M z pojedyńczych rzędów
    M = row(x[0], k_1, k_2, q_1, q_2)
    for k in range(1, len(x)):
        M = np.append(M, row(x[k], k_1, k_2, q_1, q_2))
    M = np.reshape(M, (len(x), 4))
    return M


#wszystkie powyższe funkcje są pomocnicze, nieskomplikowane i nie tak ważne

def get_r(x, y, k_1, k_2, q_1, q_2):
    H = np.subtract(y, F(x, k_1, k_2, q_1, q_2))
    H = np.reshape(H, (len(y), 1))
    R = np.subtract(1, np.divide(np.sum(np.power(H, 2)), np.sum(np.power(np.subtract(y, np.average(y)), 2))))
    return R


def fit(x, y):

    #pista resistance całego programu
    #input:array x-ów i array odpowiadających im y-ków
    #output: dopasowane parametry z dopisaną na końcu wartośią R

    #zakładamy początkowe wartości parametrów
    k_1 = 0.1
    k_2 = 0.5
    q_1 = 0.1
    q_2 = 2

    for i in range(1, 100):
        print(k_1,k_2,q_1,q_2)
        #obliczanie H (wektora różnic pomiędzy wartościami przewidywanymi i zmierzonymi)
        H = np.subtract(y,F(x, k_1, k_2, q_1, q_2))
        H = np.reshape(H, (len(y), 1))
        #tworzenie macierzy pochodnych
        M = make_M(x, k_1, k_2, q_1, q_2)
        #print(M)
        #cała magia z odwracaniem macierzy i wynarzaniem jej przez wektor H
        Mt = np.transpose(M)
        corr = np.dot(np.dot(np.linalg.inv(np.dot(Mt, M)), Mt), H)
        corr = np.reshape(corr, (1, 4))
        #poprawianie parametrów
        k_1 = max(0.0001, np.add(k_1,corr[0][0]))
        k_2 = max(0.0001, np.add(k_2,corr[0][1]))
        q_1 = max(0.0001, np.add(q_1,corr[0][2]))
        q_2 = max(0.0001, np.add(q_2,corr[0][3]))
    R = get_r(x,y,k_1,k_2,q_1,q_2)
    #R = np.subtract(1, np.divide(np.sum(np.power(H, 2)), np.sum(np.power(np.subtract(y,np.average(y)), 2))))
    return k_1, k_2, q_1, q_2, R


print(fit(np.array([14.228124299813, 7.22534382502001, 1.22042144571886, 0.164052280608162, 0.023733262203254, 0.00420182448653, 0.002272606028274]),
          np.array([0.020302634443719, 0.031305017605634, 0.05397807140849, 0.073043677371344, 0.097161252560726, 0.08471731959956, 0.081962481962482])))

#mały komentarz: W większości pzypadków w których próbowałem działa bez zarzutu, ale znowu rzeczy zależą od początkowych parametrów, ale generalnie kombinacja liczb całkowitych z zakresu 1-20 działa.
#Jak już ruszy to zazwyczaj działa dobrze. Nie wiem jak działa łapanie błędów w pythonie, ale generalnie fajnie byłoby napisdać jakiegoś while-a który próbuje różne wartośći początkowe aż któraś nie zadziała