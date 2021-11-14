from scipy import stats
import csv
import os

correlacion = open('C:/Users/jvera/Desktop/programatesis/spearmanbitcoin.csv','w',newline='')
escribir = csv.writer(correlacion, delimiter=';')
archivos = os.listdir('C:/Users/jvera/Desktop/programatesis/resultados/bitcoin')
primeraescritura = True
primeraescribir = ['',]
escribirdata = []
cont = 0
spearmanuno = []
spearmandos = []
for i in archivos:
    documento = open('C:/Users/jvera/Desktop/programatesis/resultados/bitcoin/'+i, 'r')
    lineas = documento.readlines()
    primeralinea = lineas.pop(0).rstrip("\n").split(";")
    ultimalinea = lineas.pop().rstrip("\n").split(";")# haciendo esto me quedo con sólo los resultados.
    
    escribirdata.append([i[7]+i[8]+primeralinea[3][-1:]+primeralinea[4][-1:]+primeralinea[5][12:]])
    spearmanuno = []
    for k in range(len(lineas)):
        lineas[k] = lineas[k].rstrip("\n").split(";")
        spearmanuno.append(lineas[k][2])
    for j in archivos:
        documentodos = open('C:/Users/jvera/Desktop/programatesis/resultados/bitcoin/'+j, 'r')
        lineasdos = documentodos.readlines()
        ultimalineados = lineasdos.pop().rstrip("\n").split(";")
        primerados = lineasdos.pop(0).rstrip("\n").split(";")
        if primeraescritura:
            primeraescribir.append(j[7]+j[8]+primerados[3][-1:]+primerados[4][-1:]+primerados[5][12:])
        spearmandos = []
        for h in range(len(lineas)):
            lineasdos[h] = lineasdos[h].rstrip("\n").split(";")
            spearmandos.append(lineasdos[h][2])
            # print(lineas[h][2]) así accedo al resultado
        valor, aux = stats.spearmanr(spearmanuno, spearmandos)
        if aux <= 0.05:
            escribirdata[cont].append(valor)
        else:
            escribirdata[cont].append('x')
    cont = cont + 1
    if primeraescritura:
        # print(primeraescribir) la primera línea del archivo, se escribe una vez
        primeraescritura = False
escribir.writerow(primeraescribir)
escribir.writerows(escribirdata)