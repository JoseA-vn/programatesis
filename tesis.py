#!/usr/bin/env python
# coding: utf-8


import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import random
import copy
import argparse as ap
import time
import csv


def buscarVecinosPre(G, nodos): # busca los nodos vecinos de entrada
    vecinos = copy.deepcopy(nodos)
    influenciados = []
    for i in nodos:
        if not G.nodes[i]['prevecino']:
            for j in G.predecessors(i):
                if (not j in vecinos):
                    vecinos.append(j)
                    if G.edges[(j, i)]['probinfluenciar'] < randomVec:
                        influenciados.append(j)
            G.nodes[i]['prevecino'] = True
    return vecinos, influenciados #retorna los vecinos totales del nodo para esta dirección de sentido y los de cada iteración (profundidad) 


def buscarVecinosPos(G, nodos): #busca los nodos vecinos de salida
    vecinos = copy.deepcopy(nodos)
    influenciados = []
    for i in nodos:
        if not G.nodes[i]['posvecino']:
            for j in G.successors(i):
                if (not j in vecinos):
                    vecinos.append(j)
                    if G.edges[(i, j)]['probinfluenciar'] < randomVec:
                        influenciados.append(j)
            G.nodes[i]['posvecino'] = True
    return vecinos, influenciados #retorna los vecinos totales del nodo para esta dirección de sentido y los de cada iteración (profundidad)


def linear_threshold(G, seeds): # comienza el proceso de LT-Model
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
    return resultado #retorna el resultado final de la dispersion de influencia


def dispersarLT(G, activos): #trabaja con el algoritmo de dispersión de LT 
    influenciado = set()
    for nodo in activos:
        vecinos = G.successors(nodo)
        for vecino in vecinos:
            if vecino in activos:
                continue
            nodosActivos = list(
                set(G.predecessors(vecino)).intersection(set(activos)))
            if sumaInfluencias(G, nodosActivos, vecino) >= G.nodes[vecino]['etiqueta']: #envía los nodos vecinos activos a suma inlfuencias y luego compara el resultado de sus fuerzas de dispersión para influenciar al nodo actual
                influenciado.add(vecino)
    activos.extend(list(influenciado))
    return activos, list(influenciado) #retorna el resultado acumulado y el resultado de esta iteración.


def sumaInfluencias(G, predecesores, nod): #recibe los nodos activos y suma las fuerzas de influencia
    suma = 0
    for pred in predecesores:
        suma += G.edges[(pred, nod)]['weight']
    return suma #retorna el resultado de la suma


def independent_cascade(G, seeds): #comienza el proceso de IC-Model
    A = copy.deepcopy(seeds)
    resultado = []
    resultado.extend([i for i in seeds])
    while True:
        oldLen = len(A)
        A, nodosActivos = dispersarIC(G, A, resultado)
        resultado.extend(nodosActivos)
        if len(A) == oldLen:
            break
    return resultado #retorna el resultado final de la dispersión de influencia


def dispersarIC(G, nodos, resultado):#comienza el algoritmo de IC-Model
    influenciado = set()
    for nodo in nodos:
        for vecino in G.successors(nodo):
            if not vecino in resultado:
                if round(random.random(), 1) >= G.edges[(nodo, vecino)]['weight']:#influencia randómica
                    influenciado.add(vecino)
    nodos = (list(influenciado))
    return nodos, list(influenciado) #retorna el resultado acumulado y el de la iteración actual




if __name__ == "__main__":


    LT = nx.DiGraph()
    IC = nx.DiGraph()

    archivo = 'football'
    # PREPARACIÓN ARCHIVO PARA IC MODEL
    f = open('archivos/IC/'+archivo+'/'+archivo+'.txt', 'r')
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

    for q in [0, 1, 4, 6]:
        for e in [0, 1, 2]:
            if q == 0: 
                profundidad = q
                direccion = e

                doc = open('archivos/IC/'+archivo+'/Resultados/'+archivo+'IC'+str(q)+str(e)+'0'+'.csv', 'w', newline='')
                escribir = csv.writer(doc, delimiter=';')
                escribir.writerow(['i', '|Xi|', '|F(Xi)|','profundidad'+ str(q), 'dirección'+ str(e), 'prob vecinos'+'0'])
                
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
                    aux = nodo, len(vecinos), len(resultadoIC)
                    for i in IC.nodes():
                        IC.nodes[i]['prevecino'] = False
                        IC.nodes[i]['posvecino'] = False
                    escribir.writerow(aux)
                demoraIC = time.time() - demoraIC
                escribir.writerow([str(demoraIC)])
            else:
                
                for r in [0.25, 0.5, 0.75, 1]:
                    profundidad = q
                    direccion = e
                    randomVec = r
                    doc = open('archivos/IC/'+archivo+'/Resultados/'+archivo+'IC'+str(q)+str(e)+str(r)+'.csv', 'w', newline='')
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
                        aux = nodo, len(vecinos), len(resultadoIC)
                        for i in IC.nodes():
                            IC.nodes[i]['prevecino'] = False
                            IC.nodes[i]['posvecino'] = False
                        escribir.writerow(aux)
                    demoraIC = time.time() - demoraIC
                    escribir.writerow([str(demoraIC)])

    
    
    f = open('archivos/LT/'+archivo+'/'+archivo+'.txt', 'r')
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
        cont = 0
        for k in LT.predecessors(i):
            cont = cont + 1
            peso = peso + LT.edges[(k, i)]['weight']
        LT.nodes[i]['etiqueta'] = (peso//2)+1
        LT.nodes[i]['prevecino'] = False
        LT.nodes[i]['posvecino'] = False
    for q in [0,1,4,6]:
        for e in [0, 1, 2]:
            if q == 0:
                profundidad = q
                direccion = e
                doc = open('archivos/LT/'+archivo+'/Resultados/'+archivo+'LT'+str(q)+str(e)+'0'+'.csv', 'w', newline='')
                escribir = csv.writer(doc, delimiter=';')
                escribir.writerow(['i', '|Xi|', '|F(Xi)|','profundidad'+ str(q), 'dirección'+ str(e), 'prob vecinos'+'0'])
                demoraLT = time.time()
                for nodo in LT.nodes():
                    vecinosPre = [nodo]
                    vecinosPos = [nodo]
                    vecinos = [nodo]
                    resultadoLT = []

                    for i in range(profundidad):
                        if direccion == 0:
                            auxvecinos, auxinfluenciados = buscarVecinosPre(LT,vecinosPre)
                            vecinosPre = []
                            vecinosPre.extend(auxvecinos) 
                            vecinos.extend(auxinfluenciados)

                            auxvecinos, auxinfluenciados = buscarVecinosPos(LT,vecinosPos)
                            vecinosPre = []
                            vecinosPos.extend(auxvecinos)
                            vecinos.extend(auxinfluenciados)

                        if direccion == 1: 
                            auxvecinos, auxinfluenciados = buscarVecinosPos(LT,vecinosPre)
                            vecinosPre = []
                            vecinosPre.extend(auxvecinos)
                            vecinos.extend(auxinfluenciados)

                        if direccion == 2:
                            auxvecinos, auxinfluenciados = buscarVecinosPre(LT,vecinosPre)
                            vecinosPre = []
                            vecinosPre.extend(auxvecinos) 
                            vecinos.extend(auxinfluenciados)
                    vecinos = list(dict.fromkeys(vecinos))
                    resultadoLT.extend(linear_threshold(LT, vecinos))
                    resultadoLT = list(set(resultadoLT))
                    for i in LT.nodes():
                        LT.nodes[i]['prevecino'] = False
                        LT.nodes[i]['posvecino'] = False
                    aux = nodo, len(vecinos), len(resultadoLT)

                    escribir.writerow(aux)
                demoraLT = time.time() - demoraLT
                escribir.writerow([str(demoraLT)])
            else:
                for r in [0.5, 0.75, 1]:
                    profundidad = q
                    direccion = e
                    randomVec = r
                    doc = open('archivos/LT/'+archivo+'/Resultados/'+archivo+'LT'+str(q)+str(e)+str(r)+'.csv', 'w', newline='')
                    escribir = csv.writer(doc, delimiter=';')
                    escribir.writerow(['i', '|Xi|', '|F(Xi)|','profundidad'+ str(q), 'dirección'+ str(e), 'prob vecinos'+str(r)])
                    demoraLT = time.time()
                    for nodo in LT.nodes():
                        vecinosPre = [nodo]
                        vecinosPos = [nodo]
                        vecinos = [nodo]
                        resultadoLT = []

                        for i in range(profundidad):
                            if direccion == 0:
                                auxvecinos, auxinfluenciados = buscarVecinosPre(LT,vecinosPre)
                                vecinosPre = []
                                vecinosPre.extend(auxvecinos) 
                                vecinos.extend(auxinfluenciados)

                                auxvecinos, auxinfluenciados = buscarVecinosPos(LT,vecinosPos)
                                vecinosPre = []
                                vecinosPos.extend(auxvecinos)
                                vecinos.extend(auxinfluenciados)

                            if direccion == 1: 
                                auxvecinos, auxinfluenciados = buscarVecinosPos(LT,vecinosPre)
                                vecinosPre = []
                                vecinosPre.extend(auxvecinos)
                                vecinos.extend(auxinfluenciados)

                            if direccion == 2:
                                auxvecinos, auxinfluenciados = buscarVecinosPre(LT,vecinosPre)
                                vecinosPre = []
                                vecinosPre.extend(auxvecinos) 
                                vecinos.extend(auxinfluenciados)
                        vecinos = list(dict.fromkeys(vecinos))
                        resultadoLT.extend(linear_threshold(LT, vecinos))
                        resultadoLT = list(set(resultadoLT))
                        for i in LT.nodes():
                            LT.nodes[i]['prevecino'] = False
                            LT.nodes[i]['posvecino'] = False
                        aux = nodo, len(vecinos), len(resultadoLT)

                        escribir.writerow(aux)
                    demoraLT = time.time() - demoraLT
                    escribir.writerow([str(demoraLT)])

