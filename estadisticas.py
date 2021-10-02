import os
import csv
import statistics


archivos = os.listdir('D:/cosas/beingperson/INGINF/SEM_TITULO/programatesis/archivos/IC/football/resultados')

football = open('D:/cosas/beingperson/INGINF/SEM_TITULO/programatesis/archivos/IC/football/resultados/footballEst.csv','w',newline='')
escribir = csv.writer(football, delimiter=';')
escribir.writerow(['profundidad', 'direccion', 'probvecinos','min xi', 'max xi','min fx', 'max fx', 'promedio xi', 'promedio fx','mediana','desviacion estandar','tiempo ejecucion'])
for i in archivos:
    documento = open('D:/cosas/beingperson/INGINF/SEM_TITULO/programatesis/archivos/IC/football/resultados/'+i, 'r')
    lineas = documento.readlines()
    primeralinea = lineas.pop(0).rstrip("\n").split(";")
    ultimalinea = lineas.pop().rstrip("\n").split(";")
    xi = []
    fx = []
    for i in lineas:
        aux = i.rstrip("\n").split(";")
        xi.append(int(aux[1]))
        fx.append(int(aux[2]))
    minimo = min(xi), min(fx)
    maximo = max(xi), max(fx)
    escritura = primeralinea[3][-1:],primeralinea[4][-1:],primeralinea[5][12:],minimo[0],maximo[0],minimo[1],maximo[1],round(statistics.mean(xi),2),round(statistics.mean(fx),2),statistics.median(fx),round(statistics.pstdev(fx),2),ultimalinea[0]
    escribir.writerow(escritura)
    # print(len(xi),len(fx))