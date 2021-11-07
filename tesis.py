#!/usr/bin/env python
# coding: utf-8


import networkx as nx
from networkx.classes.function import nodes_with_selfloops
import numpy as np
import matplotlib.pyplot as plt
import random
import copy
import argparse as ap
import time
import csv


def buscarVecinosPre(G, nodos):
    vecinos = copy.deepcopy(nodos)
    influenciados = []
    for i in nodos:#[0]
        if not G.nodes[i]['prevecino']:
            for j in G.predecessors(i):#[1,2]
                if (not j in vecinos):
                    vecinos.append(j)
                    if G.edges[(j, i)]['probinfluenciar'] < randomVec: #[0,1]
                        influenciados.append(j)
            G.nodes[i]['prevecino'] = True
    return vecinos, influenciados


def buscarVecinosPos(G, nodos):
    vecinos = copy.deepcopy(nodos)
    influenciados = []
    for i in nodos:
        if not G.nodes[i]['posvecino']:
            for j in G.successors(i):
                if (not j in vecinos):
                    vecinos.append(j)
                    if G.edges[(i, j)]['probinfluenciar'] < randomVec: #[0,1]
                        influenciados.append(j)
            G.nodes[i]['posvecino'] = True
    return vecinos, influenciados



def linear_threshold(G, seeds):
    A = copy.deepcopy(seeds)
    resultado = []
    resultado.extend([i for i in seeds])
    while True:
        oldLen = len(A)
        A, nodosActivos = dispersarLT(G, A)
        resultado.extend(nodosActivos)
        resultado = list(dict.fromkeys(resultado))
        if len(A) == oldLen:
            break
    return resultado


def dispersarLT(G, activos):
    influenciado = set()
    for nodo in activos:
        vecinos = G.successors(nodo)
        for vecino in vecinos:
            if vecino in activos:
                continue
            nodosActivos = list(
                set(G.predecessors(vecino)).intersection(set(activos)))
            if sumaInfluencias(G, nodosActivos, vecino) >= G.nodes[vecino]['etiqueta']:
                influenciado.add(vecino)
    activos.extend(list(influenciado))
    return activos, list(influenciado)


def sumaInfluencias(G, predecesores, nod):
    suma = 0
    for pred in predecesores:
        suma += G.edges[(pred, nod)]['weight']
    return suma


def independent_cascade(G, seeds):
    A = copy.deepcopy(seeds)
    resultado = []
    resultado.extend([i for i in seeds])
    while True:
        oldLen = len(A)
        A, nodosActivos = dispersarIC(G, A, resultado)
        resultado.extend(nodosActivos)
        if len(A) == oldLen:
            break
    return resultado


def dispersarIC(G, nodos, resultado):
    influenciado = set()
    for nodo in nodos:
        for vecino in G.successors(nodo):
            if not vecino in resultado:
                if  round(random.random(), 1) >= G.edges[(nodo, vecino)]['weight']:
                    influenciado.add(vecino)
    nodos = (list(influenciado))
    return nodos, list(influenciado)



def main():
    global args
    Parser = ap.ArgumentParser(
        description='Medida de centralidad generalizada.')
    Parser.add_argument("-a", default=None, type=str,
                        help='Nodo en específico al que se le calculará la centralidad.')
    Parser.add_argument("-l", default=0, type=int,
                        help='Nivel de profundidad.')
    Parser.add_argument("-d", default=0, type=int,
                        help='Sentido de influencia.')
    Parser.add_argument("-r", default=1, type=float,
                        help='valor de influencia en la vecindad.')
    args = Parser.parse_args()


if __name__ == "__main__":
    main()
    # profundidad = args.l
    # direccion = args.d
    # randomVec = args.r
    # nodopara = args.a
    LT = nx.DiGraph()
    IC = nx.DiGraph()

    # PREPARACIÓN ARCHIVO PARA IC MODEL
    f = open('archivos/IC/football/footballIC.txt', 'r')
    mensaje = f.readlines()
    f.close()
    nodosIC = []
    for i in range(len(mensaje)):
        mensaje[i] = mensaje[i].rstrip("\n").split(" ")
        aux = mensaje[i][0], mensaje[i][1], float(mensaje[i][2])
        nodosIC.append(aux)
    IC.add_weighted_edges_from(nodosIC)
    for i in range(len(mensaje)):
        IC.edges[(mensaje[i][0], mensaje[i][1])
                 ]['probinfluenciar'] = float(mensaje[i][3])
    for i in IC.nodes():
        IC.nodes[i]['prevecino'] = False
        IC.nodes[i]['posvecino'] = False

    # vecinosPre = ['1']
    # vecinosPos = ['1']
    # vecinos = ['1']
    # direccion = 2
    # randomVec = 1
    # for i in range(3):
    #     if direccion == 0:
    #         auxvecinos, auxinfluenciados = buscarVecinosPre(IC,vecinosPre)
    #         vecinosPre.extend(auxvecinos) 
    #         vecinos.extend(auxinfluenciados)

    #         auxvecinos, auxinfluenciados = buscarVecinosPos(IC,vecinosPos)
    #         vecinosPos.extend(auxvecinos)
    #         vecinos.extend(auxinfluenciados)
            
    #     if direccion == 1: 
    #         auxvecinos, auxinfluenciados = buscarVecinosPos(IC,vecinosPos)
    #         vecinosPos.extend(auxvecinos)
    #         vecinos.extend(auxinfluenciados)

    #     if direccion == 2:
    #         auxvecinos, auxinfluenciados = buscarVecinosPre(IC,vecinosPre)
    #         vecinosPre.extend(auxvecinos) 
    #         vecinos.extend(auxinfluenciados)

    # print(vecinos)
    # for i in IC.predecessors('1'):
    #     print(i, "soy predecesor")
    # for i in IC.successors('1'):
    #     print(i, "soy sucesor")

 

    for q in [0, 1, 4, 6]:
        for e in [0, 1, 2]:
            for r in [0.25, 0.5, 0.75, 1]:
                profundidad = q
                direccion = e
                randomVec = r
                doc = open('archivos/IC/football/resultados/footballIC'+str(q)+str(e)+str(r)+'.csv', 'w', newline='')
                escribir = csv.writer(doc, delimiter=';')
                escribir.writerow(['i', '|Xi|', '|F(Xi)|','profundidad'+ str(q), 'dirección'+ str(e), 'prob vecinos'+str(r)])
                
            # if nodopara:
            #     vecinos = [nodopara]
            #     IC.nodes[nodopara]['vecino'] = True
            #     for i in range(profundidad):
            #         vecinos.extend(buscarVecinos(IC, vecinos, direccion))
            #     print(len(vecinos), "esta es la cantidad de vecinos")
            #     resultadoIC = list(map(int, independent_cascade(IC, vecinos)))
            #     print("El conjunto resultado es: ", sorted(
            #         resultadoIC), " de tamaño: ", len(resultadoIC))
            #     for vaciar in IC.nodes():
            #         IC.nodes[vaciar]['vecino'] = False
            # else:
                # calcular tiempo aquí
                demoraIC = time.time()
                for nodo in IC.nodes():
                    vecinosPre = [nodo]
                    vecinosPos = [nodo]
                    vecinos = [nodo]

                    for i in range(profundidad):
                        if direccion == 0:
                            auxvecinos, auxinfluenciados = buscarVecinosPre(IC,vecinosPre)
                            vecinosPre.extend(auxvecinos) 
                            vecinos.extend(auxinfluenciados)

                            auxvecinos, auxinfluenciados = buscarVecinosPos(IC,vecinosPos)
                            vecinosPos.extend(auxvecinos)
                            vecinos.extend(auxinfluenciados)

                        if direccion == 1: 
                            auxvecinos, auxinfluenciados = buscarVecinosPos(IC,vecinosPos)
                            vecinosPos.extend(auxvecinos)
                            vecinos.extend(auxinfluenciados)

                        if direccion == 2:
                            auxvecinos, auxinfluenciados = buscarVecinosPre(IC,vecinosPre)
                            vecinosPre.extend(auxvecinos) 
                            vecinos.extend(auxinfluenciados)

                    resultadoIC = independent_cascade(IC, vecinos)

                    aux = nodo, len(vecinos), len(resultadoIC)

                    escribir.writerow(aux)
                demoraIC = time.time() - demoraIC
                escribir.writerow([str(demoraIC)])

#     # fig, ax = plt.subplots()  # Create a figure containing a single axes.
#     # Plot some data on the axes.
#     # ax.plot([i for i in range(len(graficar))], sorted(graficar, reverse=True))



#    PREPARACIÓN ARCHIVO PARA LT MODEL
    # f = open('archivos/LT/football/footballLT.txt', 'r')
    # archivolt = f.readlines()
    # f.close()
    # pesos = []
    # nodos = []
    # for i in range(len(archivolt)):
    #     archivolt[i] = archivolt[i].rstrip("\n").split(" ")
    #     h = archivolt[i][0], archivolt[i][1], int(archivolt[i][2])
    #     nodos.append(h)
    # LT.add_weighted_edges_from(nodos)
    # for i in range(len(archivolt)):
    #     LT.edges[(archivolt[i][0], archivolt[i][1])]['probinfluenciar'] = float(archivolt[i][3])
    # for i in LT.nodes():
    #     peso = 0
    #     for k in LT.predecessors(i):
    #         peso = peso + LT.edges[(k, i)]['weight']
    #     LT.nodes[i]['etiqueta'] = (peso/2)+1
    #     LT.nodes[i]['vecino'] = False
    #     # print(LT.nodes[i]['resistencia'])
                



    # ### ejecución de LTR
    # # if nodopara:
    # #         resultadoLT = []
    # #         vecinos= [nodopara]
    # #         LT.nodes[nodopara]['vecino'] = True
    # #         for i in range(profundidad):
    # #             vecinos.extend(buscarVecinos(LT,vecinos,direccion))
    # #         resultadoLT.extend(linear_threshold(LT, vecinos))
    # #         resultadoLT = list(set(resultadoLT))
    # #         print("El conjunto resultado es: ",resultadoLT, " de tamaño: ", len(resultadoLT))
    # #         for vaciar in LT.nodes():
    # #             LT.nodes[vaciar]['vecino'] = False
    # # else:

    # for q in [0, 1, 4, 6]:
    #     for e in [0, 1, 2]:
    #         for r in [0.25, 0.5, 0.75, 1]:
    #             profundidad = q
    #             direccion = e
    #             randomVec = r
    #             doc = open('archivos/LT/football/resultados/pruebaLT'+str(q)+str(e)+str(r)+'.csv', 'w', newline='')
    #             escribir = csv.writer(doc, delimiter=';')
    #             escribir.writerow(['i', '|Xi|', '|F(Xi)|','profundidad'+ str(q), 'dirección'+ str(e), 'prob vecinos'+str(r)])
    #             demoraLT = time.time()
    #             for nodo in LT.nodes():
                    
    #                 resultadoLT = []
    #                 vecinos= [nodo]
    #                 LT.nodes[nodo]['vecino'] = True

    #                 for i in range(profundidad):
    #                     vecinos.extend(buscarVecinos(LT,vecinos,e))
    #                 resultadoLT.extend(linear_threshold(LT, vecinos))
    #                 resultadoLT = list(set(resultadoLT))
    #                 # graficar.append(len(resultadoLT))
    #                 for vaciar in LT.nodes():
    #                     LT.nodes[vaciar]['vecino'] = False
    #                 aux = nodo, len(vecinos), len(resultadoLT)

    #                 escribir.writerow(aux)
    #             demoraLT = time.time() - demoraLT
    #             escribir.writerow([str(demoraLT)])

    # fig, ax = plt.subplots()  # Create a figure containing a single axes.
    # ax.plot([i for i in range(len(graficar))],sorted(graficar,reverse=True))  # Plot some data on the axes.
