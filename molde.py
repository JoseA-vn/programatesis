import time 
import random
import os

archivo = 'football'
f = open(archivo +'.txt', 'r') #red que se quiere moldear para trabajar
mensaje = f.readlines()
f.close()
os.makedirs("archivos/LT/"+archivo+ "/Resultados", exist_ok=True) #se crean los directorios
os.makedirs("archivos/IC/"+archivo+ "/Resultados", exist_ok=True)
h = open('archivos/IC/'+archivo+'/'+archivo+'_Seed.txt', 'w') #creacion archivo con semilla para IC
j = open('archivos/IC/'+archivo+ '/'+archivo+ '.txt', 'w') #archivo 
lt = open('archivos/LT/'+archivo+ '/'+archivo+ '.txt', 'w')#archivo red LT 
seed = int(time.time()) #semilla del valor randomico que permite la influencia entre vecinos y prob de influenciar para replicar basta con hacer la variable seed igual a una semilla utilizada antes
h.write(str(seed)) 
for i in range(len(mensaje)):
    seed = seed + 1
    objetoRandom = random.Random(seed) #probabilidad de inflouenciar vecinos
    objetoRandomVec= random.Random(objetoRandom) #probabilidad de que los vecinos sean vecinos 
    mensaje[i] = mensaje[i].rstrip("\n").split(" ")
    aleatorioVec =  round(objetoRandom.random(), 1)
    aux_ic = mensaje[i][0], mensaje[i][1], aleatorioVec, round(objetoRandomVec.random(), 1)
    aux_lt = mensaje[i][0], mensaje[i][1], mensaje[i][2], aleatorioVec
    j.write(str(aux_ic[0]) +' '+ str(aux_ic[1])+' ' + str(aux_ic[2]) + ' '+ str(aux_ic[3])+ '\n')
    lt.write(str(aux_lt[0]) +' '+ str(aux_lt[1])+' ' + str(int(aux_lt[2])) + ' '+ str(aux_lt[3]) + '\n') ##aqui aux_lt[2] tiene +11 dado que en la red especifica era necesario sumar 11 para que no dieran valores negativos

