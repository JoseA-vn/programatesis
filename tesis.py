#!/usr/bin/env python
# coding: utf-8


import networkx as nx
import random
import copy
import time
import csv


def buscarVecinosPre(G, nodos):
    vecinos = nodos
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
    vecinos = nodos
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


def independent_cascade(G, seeds):
    A = copy.deepcopy(seeds)
    resultado = []
    for i in seeds:
        resultado.append(i)
    # while True:
    for i in range(1):
        print(A)
        oldLen = len(A)
        A, nodosActivos = dispersarIC(G, A, resultado)
        resultado.extend(nodosActivos)
        if len(A) == oldLen:
            break
    return resultado


def dispersarIC(G, nodos, resultado):
    influenciado = set()
    for nodo in nodos:
        print(nodo)
        for vecino in G.successors(nodo):
            if not vecino in resultado:
                if round(random.random(), 1) >= G.edges[(nodo, vecino)]['weight']:
                    influenciado.add(vecino)
    nodos = (list(influenciado))
    print(sorted(nodos))
    return nodos, list(influenciado)



if __name__ == "__main__":

    IC = nx.DiGraph()

    # PREPARACIÓN ARCHIVO PARA IC MODEL
    f = open('archivos/IC/bitcoin/bitcoinIC.txt', 'r')
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
    # h = 0
    # for q in [0, 1, 4, 6]:
    #     for e in [0, 1, 2]:
    #         for r in [0.25, 0.5, 0.75, 1]:
    #             vecinosPre = ['1']
    #             vecinosPos = ['1']
    #             vecinos = ['1']
    #             direccion = e
    #             randomVec = r

    #             for i in range(q):

    #                 if direccion == 0:
    #                     auxvecinos, auxinfluenciados = buscarVecinosPre(IC,vecinosPre)
    #                     vecinosPre.extend(auxvecinos) 
    #                     vecinos.extend(auxinfluenciados)

    #                     auxvecinos, auxinfluenciados = buscarVecinosPos(IC,vecinosPos)
    #                     vecinosPos.extend(auxvecinos)
    #                     vecinos.extend(auxinfluenciados)

    #                 if direccion == 1: 
    #                     auxvecinos, auxinfluenciados = buscarVecinosPos(IC,vecinosPos)
    #                     vecinosPos.extend(auxvecinos)
    #                     vecinos.extend(auxinfluenciados)
    #                     h = h + 1


    #                 if direccion == 2:
    #                     auxvecinos, auxinfluenciados = buscarVecinosPre(IC,vecinosPre)
    #                     vecinosPre.extend(auxvecinos) 
    #                     vecinos.extend(auxinfluenciados)

    #             # print(len(vecinos))
    #             for i in IC.nodes():
    #                 IC.nodes[i]['prevecino'] = False
    #                 IC.nodes[i]['posvecino'] = False
    #             # for i in IC.predecessors('1'):
    #             #     print(i, "soy predecesor")
    #             # for i in IC.successors('1'):
    #             #     print(i, "soy sucesor")

 

    for q in [0, 1, 4, 6]:
        for e in [0, 1, 2]:
            for r in [0.25, 0.5, 0.75, 1]:
                profundidad = q
                direccion = e
                randomVec = r
                doc = open('archivos/IC/bitcoin/resultados/bitcoinIC'+str(q)+str(e)+str(r)+'.csv', 'w', newline='')
                escribir = csv.writer(doc, delimiter=';')
                escribir.writerow(['i', '|Xi|', '|F(Xi)|','profundidad'+ str(q), 'dirección'+ str(e), 'prob vecinos'+str(r)])
                
                demoraIC = time.time()
                for nodo in IC.nodes():
                    vecinosPre = [nodo]
                    vecinosPos = [nodo]
                    vecinos = [nodo]

                    for i in range(profundidad):
                        if direccion == 0:
                            auxvecinos, auxinfluenciados = buscarVecinosPre(IC,vecinosPre)
                            vecinosPre = []
                            vecinosPre.extend(auxvecinos) 
                            vecinos.extend(auxinfluenciados)

                            auxvecinos, auxinfluenciados = buscarVecinosPos(IC,vecinosPos)
                            vecinosPos = []
                            vecinosPos.extend(auxvecinos)
                            vecinos.extend(auxinfluenciados)

                        if direccion == 1: 
                            auxvecinos, auxinfluenciados = buscarVecinosPos(IC,vecinosPre)
                            vecinosPre = []
                            vecinosPre.extend(auxvecinos)
                            vecinos.extend(auxinfluenciados)

                        if direccion == 2:
                            auxvecinos, auxinfluenciados = buscarVecinosPre(IC,vecinosPre)
                            vecinosPre = []
                            vecinosPre.extend(auxvecinos) 
                            vecinos.extend(auxinfluenciados)
                    vecinos = list(dict.fromkeys(vecinos))
                    resultadoIC = independent_cascade(IC, vecinos)
                    print(nodo, len(vecinos), len(resultadoIC))
                    aux = nodo, len(vecinos), len(resultadoIC)
                    for i in IC.nodes():
                        IC.nodes[i]['prevecino'] = False
                        IC.nodes[i]['posvecino'] = False
                    escribir.writerow(aux)
                    break
                demoraIC = time.time() - demoraIC
                escribir.writerow([str(demoraIC)])
                break
            break
        break





