import os
import csv
import statistics
import numpy as np


archivos = os.listdir('C:/Users/jvera/Desktop/programatesis/archivos/IC/bitcoin/resultados')

bitcoin = open('C:/Users/jvera/Desktop/programatesis/archivos/IC/bitcoin/bitcoinEst.csv','w',newline='')
escribir = csv.writer(bitcoin, delimiter=';')
escribir.writerow(['profundidad', 'direccion', 'probvecinos','min xi', 'max xi','min fx', 'max fx', 'promedio xi', 'promedio fx','mediana xi','mediana fx','desviacion estandar xi','desviacion estandar fx','cantidad de valores distintos xi','cantidad de valores distintos fx','tiempo ejecucion'])
for i in archivos:
    documento = open('C:/Users/jvera/Desktop/programatesis/archivos/IC/bitcoin/resultados/'+i, 'r')
    lineas = documento.readlines()
    primeralinea = lineas.pop(0).rstrip("\n").split(";")
    ultimalinea = lineas.pop().rstrip("\n").split(";")
    ultimalinea[0] = ultimalinea[0].replace('.',',')
    xi = []
    fx = []
    for i in lineas:
        aux = i.rstrip("\n").split(";")
        xi.append(int(aux[1]))
        fx.append(int(aux[2]))
    minimo = min(xi), min(fx)
    maximo = max(xi), max(fx)
    escritura = primeralinea[3][-1:],primeralinea[4][-1:],primeralinea[5][12:],minimo[0],maximo[0],minimo[1],maximo[1],round(statistics.mean(xi),2),round(statistics.mean(fx),2),statistics.median(xi),statistics.median(fx),round(statistics.pstdev(xi),2),round(statistics.pstdev(fx),2),len(np.unique(xi)),len(np.unique(fx)),ultimalinea[0]
    escribir.writerow(escritura)
    # print(len(xi),len(fx))