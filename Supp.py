#!/usr/bin/env python
# encoding: utf8

import Divisao
import networkx as nx
from math import sqrt

# FUNÇÕES RELEVANTES À LISTA DE DIVISOES E GRAFO

def id_divisoes(array_divisoes):
	
	lista = []

	if array_divisoes is []:
		return lista

	for divisao in array_divisoes:
		lista.append(divisao.id)
	return lista

def twopoint_distance(p1, p2):
	dist = sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)
	return dist

def getDivisao(div_id, array_divisoes):
	
	for elem in array_divisoes:
		if elem.id == div_id:
			return elem

def singleCheck(array_divisoes):
	
	for divisao in array_divisoes:
		if divisao.tipo == 'single':
			return True
	return False

# Sem distancias
def getEdges(array_divisoes):
	
	edges = []
	
	for divisao in array_divisoes:
		l_vizinhos = divisao.viz
		for vizinho in l_vizinhos:
			# Grafo sem peso
			edges.append([divisao.id, vizinho])
	return edges 

# Com distancias e desenhar o grafo a partir da posição atual
def getEdges_weight(array_divisoes, grafo, src, coord):

	for divisao in array_divisoes:
		l_vizinhos = divisao.viz
		for id_vizinho in l_vizinhos:
			vizinho = getDivisao(id_vizinho, array_divisoes)

			if divisao.id == src:
				dist = twopoint_distance(coord, vizinho.pm)
			elif id_vizinho == src:
				dist = twopoint_distance(divisao.pm, coord)
			else:
				dist = twopoint_distance(divisao.pm, vizinho.pm)

			# Grafo com peso
			grafo.add_edges_from([(divisao.id, vizinho.id)], dist=dist)
	return grafo


def pesquisa(grafo, src, dest, path):
	
	if src is dest:
		path.append(src)
		return path
    
	for ponto1, pontos in dict(nx.bfs_successors(grafo, src)).items():
        # Procurar a divisao pretendida nível a nível
            if dest in pontos:
                # Assim que chegarmos ao destino,
                # Armazenar informação e fazer o caminho inverso
                path.append(dest)
                return pesquisa(grafo, src, ponto1, path)

def present_room(x, y):

	# Paredes Verticais +-0.6
	# Paredes Horizontais +-0.5
	# Adicionar +- 0.1 consoante a orientação da parede para remover edge situations

	if(y < -1.3):
		pm = (-6, -2.15)
		return (pm, "corredor1")
	
	if((x > -11.9) and (5.3 <= y <= 7.4)):
		pm = (-4.1, 6.35)
		return (pm, "corredor3")

	if((-11.9 <= x <= -9.4) and (-1.3 <= y <= 5.4)):
		pm = (-10.7, 2.05)
		return (pm, "corredor2")

	if((-4.0 <= x <= -1.4) and (-1.3 <= y <= 5.4)):
		pm = (-2.7, 2.05)
		return (pm, "corredor4")

	if((x <= -12.3) and (-0.9 <= y <= 2.4)):
		pm = (-14.0, 0.8)
		return (pm, "sala5")

	if((x <= -12.3) and (2.9 <= y <= 7.4)):
		pm = (-14.0, 5.0)
		return (pm, "sala6")

	if((x <= -11.0) and (y >= 7.8)):
		pm = (-13.35, -9.5)
		return (pm, "sala7")

	if((-10.5 <= x <= -6.1) and (y >= 7.8)):
		pm = (-8.3, 9.5)
		return (pm, "sala8")

	if((-5.7 <= x <= -1.1) and (y >= 7.8)):
		pm = (-3.4, 9.5)
		return (pm, "sala9")

	if((x >= -0.6) and (y >= 7.8)):
		pm = (1.5, 9.5)
		return (pm, "sala10")
	
	if((x >= -0.9) and (2.2 <= y <= 4.9)):
		pm = (1.35, 3.6)
		return (pm, "sala11")

	if((x >= -0.9) and (-1.0 <= y <= 1.7)):
		pm = (1.35, 0.4)
		return (pm, "sala12")

	if((-9.0 <= x <= -7.1) and (-1.0 <= y <= 4.9)):
		pm = (-8.05, 2)
		return (pm, "sala13")

	if((-6.5 <= x <= -4.5) and (-1.0 <= y <= 4.9)):
		pm = (-5.55, 2)
		return (pm, "sala14")
	
	return ((0, 0), "porta")
