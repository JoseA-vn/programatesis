from scipy import stats
import csv



spearmam = open('C:/Users/jvera/Desktop/programatesis/archivos/IC/higgs/spearman.csv','w',newline='')
escribir = csv.writer(spearmam, delimiter=';')
escribir.writerow(['direccionalidad','máximos','promedios'])
higgs = open(
    'C:/Users/jvera/Desktop/programatesis/archivos/IC/higgs/higgsEst.csv', 'r')
lineas = higgs.readlines()
lineas.pop(0)

maxxcero = []
maxfxcero = []
promxcero = []
promfxcero = []

maxxuno = []
maxfxuno = []
promxuno = []
promfxuno = []


maxxdos = []
maxfxdos = []
promxdos = []
promfxdos = []

for i in range(len(lineas)):
    lineas[i] = lineas[i].rstrip("\n").split(";")
    # print(lineas[i])
    if lineas[i][1] == '0':
        maxxcero.append(int(lineas[i][4]))
        maxfxcero.append(int(lineas[i][6]))
        promxcero.append(float(lineas[i][7]))
        promfxcero.append(float(lineas[i][8]))
    if lineas[i][1] == '1':
        maxxuno.append(int(lineas[i][4]))
        maxfxuno.append(int(lineas[i][6]))
        promxuno.append(float(lineas[i][7]))
        promfxuno.append(float(lineas[i][8]))

    if lineas[i][1] == '2':
        maxxdos.append(int(lineas[i][4]))
        maxfxdos.append(int(lineas[i][6]))
        promxdos.append(float(lineas[i][7]))
        promfxdos.append(float(lineas[i][8]))

mcorrcero, mpcero = stats.spearmanr(maxxcero,maxfxcero)
pcorrcero, ppcero = stats.spearmanr(promxcero,promfxcero)
mcorruno, mpuno = stats.spearmanr(maxxuno,maxfxuno)
pcorruno, ppuno = stats.spearmanr(promxuno,promfxuno)
mcorrdos, mpdos = stats.spearmanr(maxxdos,maxfxdos)
pcorrdos, ppdos = stats.spearmanr(promxdos,promfxdos)





escribir.writerow(['0', mcorrcero if mpcero < 0.05 else 'X', pcorrcero if ppcero < 0.05 else 'X'])
escribir.writerow(['1', mcorruno if mpuno < 0.05 else 'X', pcorruno if ppuno < 0.05 else 'X'])
escribir.writerow(['2', mcorrdos if mpdos < 0.05 else 'X' , pcorrdos if ppdos < 0.05 else 'X'])
