from scipy import stats
import csv
import os

correlacion = open('C:/Users/jvera/Desktop/programatesis/spearmanhiggs.csv','w',newline='')
escribir = csv.writer(correlacion, delimiter=';')
archivos = os.listdir('C:/Users/jvera/Desktop/programatesis/resultados/higgs')
primeraescritura = True
primeraescribir = ['',]
escribirdata = []
cont = 0
spearmanuno = []
spearmandos = []
for i in archivos:
    documento = open('C:/Users/jvera/Desktop/programatesis/resultados/higgs/'+i, 'r')
    lineas = documento.readlines()
    primeralinea = lineas.pop(0).rstrip("\n").split(";")
    ultimalinea = lineas.pop().rstrip("\n").split(";")# haciendo esto me quedo con sólo los resultados.
    
    escribirdata.append([i[5]+i[6]+primeralinea[3][-1:]+primeralinea[4][-1:]+primeralinea[5][12:]])
    spearmanuno = []
    for k in range(len(lineas)):
        lineas[k] = lineas[k].rstrip("\n").split(";")
        spearmanuno.append(lineas[k][2])
    for j in archivos:
        documentodos = open('C:/Users/jvera/Desktop/programatesis/resultados/higgs/'+j, 'r')
        lineasdos = documentodos.readlines()
        ultimalineados = lineasdos.pop().rstrip("\n").split(";")
        primerados = lineasdos.pop(0).rstrip("\n").split(";")
        if primeraescritura:
            primeraescribir.append(j[5]+j[6]+primerados[3][-1:]+primerados[4][-1:]+primerados[5][12:])
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