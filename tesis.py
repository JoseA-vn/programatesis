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



def linear_threshold(G, seeds):
    A = copy.deepcopy(seeds)
    resultado = []
    resultado.extend([i for i in seeds])
    while True:
        print("hola yo me buguee")
        oldLen = len(A)
        A, nodosActivos = dispersarLT(G, A)
        resultado.extend(nodosActivos)
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
    activos = (list(influenciado))
    return activos, list(influenciado)


def sumaInfluencias(G, predecesores, nod):
    suma = 0
    for pred in predecesores:
        suma += G.edges[(pred, nod)]['weight']
    return suma




if __name__ == "__main__":
    LT = nx.DiGraph()


#    PREPARACIÓN ARCHIVO PARA LT MODEL
    f = open('archivos/LT/football/footballLT.txt', 'r')
    archivolt = f.readlines()
    f.close()
    pesos = []
    nodos = []
    for i in range(len(archivolt)):
        archivolt[i] = archivolt[i].rstrip("\n").split(" ")
        h = archivolt[i][0], archivolt[i][1], int(archivolt[i][2])
        nodos.append(h)
    LT.add_weighted_edges_from(nodos)
    for i in range(len(archivolt)):
        LT.edges[(archivolt[i][0], archivolt[i][1])]['probinfluenciar'] = float(archivolt[i][3])
    for i in LT.nodes():
        peso = 0
        for k in LT.predecessors(i):
            peso = peso + LT.edges[(k, i)]['weight']
        LT.nodes[i]['etiqueta'] = (peso/2)+1
        LT.nodes[i]['vecino'] = False

    ### ejecución de LTR


    for q in [0, 1, 4, 6]:
        for e in [0, 1, 2]:
            for r in [0.25, 0.5, 0.75, 1]:
                profundidad = q
                direccion = e
                randomVec = r
                doc = open('archivos/LT/football/resultados/pruebaLT'+str(q)+str(e)+str(r)+'.csv', 'w', newline='')
                escribir = csv.writer(doc, delimiter=';')
                escribir.writerow(['i', '|Xi|', '|F(Xi)|','profundidad'+ str(q), 'dirección'+ str(e), 'prob vecinos'+str(r)])
                demoraLT = time.time()
                for nodo in LT.nodes():
                    
                    resultadoLT = []
                    vecinos= [nodo]
                    LT.nodes[nodo]['vecino'] = True

                    for i in range(profundidad):
                        vecinos.extend(buscarVecinos(LT,vecinos,e))
                    resultadoLT.extend(linear_threshold(LT, vecinos))
                    resultadoLT = list(set(resultadoLT))
                    # graficar.append(len(resultadoLT))
                    for vaciar in LT.nodes():
                        LT.nodes[vaciar]['vecino'] = False
                    aux = nodo, len(vecinos), len(resultadoLT)

                    escribir.writerow(aux)
                demoraLT = time.time() - demoraLT
                escribir.writerow([str(demoraLT)])






                




