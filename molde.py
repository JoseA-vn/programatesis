import time 
import random

# f = open('higgs-reply_network.edgelist', 'r')
# mensaje = f.readlines()
# f.close()
# h = open('archivos/IC/higgs/semillaHiggsIC.txt', 'w')
# j = open('archivos/IC/higgs/higgsIC.txt', 'w')
# seed = int(time.time())
# h.write(str(seed))
# for i in range(len(mensaje)):
#     seed = seed + 1
#     objetoRandom = random.Random(seed)
#     objetoRandomVec= random.Random(objetoRandom)
#     mensaje[i] = mensaje[i].rstrip("\n").split(" ")
#     aux = mensaje[i][0], mensaje[i][1], round(objetoRandom.random(), 1), round(objetoRandomVec.random(), 1)
#     j.write(str(aux[1]) +' '+ str(aux[0])+' ' + str(aux[2]) + ' '+ str(aux[3])+ '\n')
#     print(aux[0],aux[1],aux[2],aux[3],seed)

f = open('soc-sign-bitcoinalpha.csv', 'r')
mensaje = f.readlines()
f.close()
j = open('archivos/LT/bitcoin/bitcoinLT.txt', 'w')
seed = int(time.time())
print(seed)
for i in range(len(mensaje)):
    seed = seed + 1
    objetoRandom = random.Random(seed)
    mensaje[i] = mensaje[i].rstrip("\n").split(",")
    aux = mensaje[i][0], mensaje[i][1], mensaje[i][2], round(objetoRandom.random(), 1)
    j.write(str(aux[1]) +' '+ str(aux[0])+' ' + str(int(aux[2])+11) + ' '+ str(aux[3]) + '\n') 
    # print(aux[1],aux[0],int(aux[2])+11)