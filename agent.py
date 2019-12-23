#!/usr/bin/env python
# encoding: utf8
# Artificial Intelligence, UBI 2019-20
# Modified by: Students names and numbers

import rospy
from std_msgs.msg import String
from nav_msgs.msg import Odometry
import Divisao
import networkx as nx
import math
import time

# FUNÇÕES RELEVANTES À LISTA DE DIVISOES E GRAFO

def id_divisoes(array_divisoes):
	
	lista = []

	if array_divisoes is []:
		return lista

	for divisao in array_divisoes:
		lista.append(divisao.id)
	return lista

def twopoint_distance(p1, p2):
	dist = math.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)
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

# Com distancias
def getEdges_weight(array_divisoes, grafo):
	
	for divisao in array_divisoes:
		l_vizinhos = divisao.viz
		for id_vizinho in l_vizinhos:
			vizinho = getDivisao(id_vizinho, array_divisoes)
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

	

# VARIÁVEIS CHAVE

start_time = time.time()
x_ant = 0
y_ant = 0
obj_ant = ''
curr_room = ''	
room_ant = 'corredor1'
minimap = []

# Fazer parse de doubles, might not be needed
def fst(tuple):
	return tuple[0]

def snd(tuple):
	return tuple[1]

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
		pm = (-14.0, 2.2)
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
		pm = (-2.1, 9.5)
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



# PERGUNTA 1

def quartosNaoOcupados(array_divisoes):

	naoOcupados = 0

	# Percorrer todas as divisoes, ver se está ou não ocupado

	for divisao in array_divisoes:
		if divisao.getNumPessoas() is 0 and divisao.tipo != "corredor":
			naoOcupados += 1
	
	print(f"I have seen %d rooms without people so far." %naoOcupados)

	
# PERGUNTA 2

def suite_finder(array_divisoes):
	
	contSuite = 0

	for divisao in array_divisoes:
		if divisao.tipo == "suite":
			contSuite += 1

	if contSuite is not 0:
		print(f"I have found %d suite rooms so far.") %(contSuite/2)
	else:
		print("I haven't found any suites so far.")
	

# PERGUNTA 3

def searchPeople(array_divisoes):

	# Contadores 

	pessoasCorredores = 0
	pessoasQuartos = 0

	# Procurar por pessoas nas divisões, separar por tipo
	# Casos extremos ainda nao contabilizados

	for divisao in array_divisoes:
		if divisao.tipo == "corredor":
			pessoasCorredores += divisao.getNumPessoas()
		else:
			pessoasQuartos += divisao.getNumPessoas()

	diff = abs(pessoasCorredores - pessoasQuartos)

	if pessoasCorredores > pessoasQuartos:
		print(f"More people in hallways compared to rooms, about %d more.") %(diff)
	elif pessoasCorredores < pessoasQuartos:
		print(f"More people in the rooms compared to hallways, about %d more.") %(diff)
	else:
		print(f"There are exactly the same number of people outside and inside rooms (%d)." %pessoasQuartos)

# PERGUNTA 4

def predominancia_computadores(array_divisoes):
	
	pcs_in_generic = 0
	pcs_in_single = 0
	pcs_in_double = 0
	pcs_in_corridor = 0
	pcs_in_conference = 0
	pcs_in_suite = 0

	for divisao in array_divisoes:
		if divisao.tipo == 'generic':
			pcs_in_generic += divisao.getNumComputadores()
		elif divisao.tipo == 'single':
			pcs_in_single += divisao.getNumComputadores()
		elif divisao.tipo == 'double':
			pcs_in_double += divisao.getNumComputadores()
		elif divisao.tipo == 'suite':
			pcs_in_suite += divisao.getNumComputadores()
		elif divisao.tipo == 'conferece room':
			pcs_in_conference += divisao.getNumComputadores()
		elif divisao.tipo == 'corridor':
			pcs_in_corridor += divisao.getNumComputadores()
	
	# Fazer lista com tuplos('tipo', nr_pcs)
	# Inverter consoante nr_pcs para ficar com o valor mais alto na primeira posicao
	# Retornar o tipo

	values_stored = [('generics', pcs_in_generic), ('singles', pcs_in_single), ('doubles', pcs_in_double), ('corridors', pcs_in_corridor), ('conference rooms', pcs_in_conference), ('suites', pcs_in_suite)]
	values_stored.sort(key=snd, reverse=True)

	if values_stored[0][1] is not 0:
		print(f"To find computers, our best chance is in %s." %(values_stored[0][0]))
	else:
		print(f"I haven't found a single computer yet.")

# PERGUNTA 5

def individual_mais_perto(array_divisoes):

	# Calcular o caminho mais perto entre a posicao atual e cada elemento do array

	if singleCheck(array_divisoes):
		div = getDivisao(curr_room, array_divisoes)

		if div.tipo != 'single':
		
			path_distances = []
			start = curr_room

			G = nx.Graph()
			G = getEdges_weight(array_divisoes, G)

			for divisao in array_divisoes:

				if divisao.tipo == 'single':
					#dist é int 100% pois temos src e dest
					dist = nx.shortest_path_length(G, start, divisao.id, weight='dist')
					path_distances.append((divisao.id, dist))	
		
			path_distances.sort(key=snd, reverse=True)
			print(f"The closest single room is %s in a distance of %.1f." %(path_distances[0][0], path_distances[0][1]))
		
		else:
			print(f"The closest single room is %s, in which we are in" %curr_room)
	else:
		print("There are no single rooms as far as i know.")
	
# PERGUNTA 6

# Não necessáriamente o mais curto, isto é bfs 
def percurso_para_elevador(array_divisoes):
	
	# Sabemos 100% que o agente começa no elevador, e que a única maneira de ir para o elevador é por passar pelo corredor1
	# get current position
	# pesquisar de onde estamos até chegar ao elevador
	# no final append de 'elevador'
	# Devolver uma lista ordenada

	G = nx.Graph()
	edge_list = getEdges(array_divisoes)
	G.add_edges_from(edge_list)

	path = []
	dest = 'corredor1'

	if curr_room == 'corredor1':
		pass

	elif curr_room == 'porta':
		start = room_ant
		path = pesquisa(G, start, dest, [])

	else:
		start = curr_room
		path = pesquisa(G, start, dest, [])

	path.reverse()
	path.append('elevador')
	print("We can take the respective path:")
	print(path)
				

# PERGUNTA 7

def estimativa_de_encontrar_livros(array_divisoes):
	
	contaLivros = 0	
	
	for divisao in array_divisoes:
		contaLivros += divisao.getNumLivros()
	
	curr_time = time.time() - start_time	
		
	if curr_time is not 0:
		estimativa = (contaLivros*120.0) / curr_time
		print(f"I estimate finding about %d books in 2 minutes." %estimativa)
	else:
		print("I cant estimate with either no books or timer is 0.")

# PERGUNTA 8
					
def probabilidade_mesa_sem_livros_com_uma_cadeira(array_divisoes):

	# P(m and ~b | >1 chair)
	# P(m and ~b)
	# ------------
	# P(>1 chair)

	contA = 0
	contB = 0

	for divisao in array_divisoes:
		if divisao.getNumLivros() is 0 and divisao.getNumMesas() >= 1:
			contA += 1
		if divisao.getNumCadeiras() >= 1:
			contB += 1
	
	if contB is 0 or contA is 0:
		print("My data says the chance is 0")
	else:
		prob = contA / float(contB)
		print(f"We have about %.2f chance of finding a table in those conditions as of now." %prob)

# Pergunta 9

def inventory(array_divisoes):

	if curr_room != 'porta':
		d = getDivisao(curr_room, array_divisoes)
	
		print(d.id)
		print(d.tipo)
		print(d.camas)
		print(d.cadeiras)
		print(d.mesas)
		print(d.livros)
		print(d.pessoas)
		print(d.computadores)
		print(d.viz)
		print(d.pm)
		print(id_divisoes(array_divisoes))
	else:
		print("Doors are dumb.")

# ---------------------------------------------------------------
# odometry callback
def callback(data):
	
	global x_ant, y_ant, curr_room, room_ant, minimap
	
	bad_rooms = (room_ant, 'porta')

	x=data.pose.pose.position.x-15
	y=data.pose.pose.position.y-1.5

	# show coordinates only when they change
	if x != x_ant or y != y_ant:
		(ponto_medio, curr_room) = present_room(x,y)
		print (" x=%.1f y=%.1f : %s <- %s") % (x,y,curr_room, room_ant)

		# Adicionar objetos à minimapa
		if curr_room not in id_divisoes(minimap) and curr_room != 'porta':

			newdivisao = Divisao.Divisao()
			newdivisao.id = curr_room
			newdivisao.pm = ponto_medio

			if curr_room.startswith('corredor'):
				newdivisao.tipo = 'corredor'
			
			minimap.append(newdivisao)

		# Lógica de adicionar vizinhos e suite check
		if curr_room not in bad_rooms:
			
			thisdiv = getDivisao(curr_room, minimap)
			pastdiv = getDivisao(room_ant, minimap)

			if curr_room not in pastdiv.viz:
				pastdiv.adicionarViz(curr_room)
			if room_ant not in thisdiv.viz:
				thisdiv.adicionarViz(room_ant)

			if thisdiv.suiteCheck(pastdiv):
				thisdiv.tipo = 'suite'
				pastdiv.tipo = 'suite'

			room_ant = curr_room
			
	x_ant = x
	y_ant = y
	

# ---------------------------------------------------------------
# object_recognition callback
def callback1(data):

	global obj_ant, curr_room, minimap
	bad_rooms = ("porta")

	obj = data.data
	if obj != obj_ant and data.data != "":
		print ("object is %s") %data.data
		
		# Lógica para adicionar objetos
		if curr_room not in bad_rooms:

			thisdiv = getDivisao(curr_room, minimap)
			thisdiv.addobj(obj)
			thisdiv.tiparQuarto()

	obj_ant = obj
		
# ---------------------------------------------------------------
# questions_keyboard callback
def callback2(data):

	print ("question is %s") %data.data
	question = data.data

	if question == '1':
		quartosNaoOcupados(minimap)
		
	elif question == '2':
		suite_finder(minimap)
		
	elif question == '3':
		searchPeople(minimap)
		
	elif question == '4':
		predominancia_computadores(minimap)
		
	elif question == '5':
		individual_mais_perto(minimap)
		
	elif question == '6':
		percurso_para_elevador(minimap)

	elif question == '7':
		estimativa_de_encontrar_livros(minimap)
		
	elif question == '8':
		probabilidade_mesa_sem_livros_com_uma_cadeira(minimap)

	elif question == '9':
		inventory(minimap)

# ---------------------------------------------------------------
def agent():
	rospy.init_node('agent')

	rospy.Subscriber("questions_keyboard", String, callback2)
	rospy.Subscriber("object_recognition", String, callback1)
	rospy.Subscriber("odom", Odometry, callback)

	rospy.spin()

# ---------------------------------------------------------------
if __name__ == '__main__':
	agent()
