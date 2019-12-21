#!/usr/bin/env python
# encoding: utf8
# Artificial Intelligence, UBI 2019-20
# Modified by: Students names and numbers

import rospy
from std_msgs.msg import String
from nav_msgs.msg import Odometry
import Divisao
import networkx as nx

# FUNÇÕES RELEVANTES À LISTA DE DIVISOES E GRAFO

def id_divisoes(array_divisoes):
	lista = []
	for divisao in array_divisoes:
		lista.append(divisao.id)
	return lista

def getDivisao(div_id, array_divisoes):
	if div_id in id_divisoes(array_divisoes):
		for elem in array_divisoes:
			if elem.id is div_id:
				return elem

def getEdges(array_divisoes):
	
	edges = []
	
	for divisao in array_divisoes:
		l_vizinhos = divisao.viz
		for vizinho in l_vizinhos:
			edges.append([divisao.id, vizinho])
	return edges 

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

x_ant = 0
y_ant = 0
obj_ant = ''
curr_room = ''	
room_ant = ''
minimap = []

# Fazer parse de doubles
def fst(tuple):
	return tuple[0]

def snd(tuple):
	return tuple[1]

def present_room(x, y):

	# Paredes Verticais +-0.6
	# Paredes Horizontais +-0.5
	# Adicionar +- 0.1 consoante a orientação da parede para remover edge situations

	if(x == -15.0 and y ==-1.5):
		return "elevador"

	if(y < -1.3):
		return "corredor1"
	
	if((x > -11.9) and (5.4 <= y <= 7.4)):
		return "corredor3"

	if((-11.9 <= x <= -9.4) and (-1.3 <= y <= 5.4)):
		return "corredor2"

	if((-4.0 <= x <= -1.4) and (-1.3 <= y <= 5.4)):
		return "corredor4"

	if((x <= -12.3) and (-0.9 <= y <= 2.4)):
		return "sala5"

	if((x <= -12.3) and (2.9 <= y <= 7.4)):
		return "sala6"

	if((x <= -11.0) and (y >= 7.8)):
		return "sala7"

	if((-10.5 <= x <= -6.1) and (y >= 7.8)):
		return "sala8"

	if((-5.7 <= x <= -1.1) and (y >= 7.8)):
		return "sala9"

	if((x >= -0.6) and (y >= 7.8)):
		return "sala10"
	
	if((x >= -0.9) and (2.2 <= y <= 4.9)):
		return "sala11"

	if((x >= -0.9) and (-1.0 <= y <= 1.7)):
		return "sala12"

	if((-9.0 <= x <= -7.1) and (-1.0 <= y <= 4.9)):
		return "sala13"

	if((-6.5 <= x <= -4.5) and (-1.0 <= y <= 4.9)):
		return "sala14"
	
	return "porta"

# PERGUNTA 1

def quartosOcupados(array_divisoes):

	contOcupados = 0
	bad_divisoes = ["corredor", "elevador"]


	# Percorrer todas as divisoes, ver se está ou não ocupado

	for divisao in array_divisoes:
		if not divisao.ver_ocupado() and divisao.tipo not in bad_divisoes:
			contOcupados += 1
	
	print(f"There are %d rooms occupied, as far as i know." %contOcupados)

	
# PERGUNTA 2

def suite_finder(array_divisoes):
	
	contSuite = 0

	for divisao in array_divisoes:
		if divisao.tipo is "suite":
			contSuite += 1

	if contSuite == 0:
		print(f"I have found %d suite rooms so far." %(contSuite/2))
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
		if divisao.ver_ocupado:
			if divisao.tipo is "corredor" or divisao.tipo is "elevador":
				pessoasCorredores += divisao.getPessoas
			else:
				pessoasQuartos += divisao.getPessoas

	diff = abs(pessoasCorredores - pessoasQuartos)

	if pessoasCorredores > pessoasQuartos:
		print(f"More people in hallways compared to rooms, about %d." %diff)
	elif pessoasCorredores < pessoasQuartos:
		print(f"More people in the rooms compared to hallways, about %d." %diff)
	else:
		return "There are exactly the same number of people outside and inside rooms."

# PERGUNTA 4

def predominancia_computadores(array_divisoes):
	
	pcs_in_generic = 0
	pcs_in_single = 0
	pcs_in_double = 0
	pcs_in_corridor = 0
	pcs_in_conference = 0
	pcs_in_suite = 0

	for divisao in array_divisoes:
		if divisao.tipo is 'generic':
			pcs_in_generic += divisao.getComputadores
		elif divisao.tipo is 'single':
			pcs_in_single += divisao.getComputadores
		elif divisao.tipo is 'double':
			pcs_in_double += divisao.getComputadores
		elif divisao.tipo is 'suite':
			pcs_in_suite += divisao.getComputadores
		elif divisao.tipo is 'conferece room':
			pcs_in_conference += divisao.getComputadores
		elif divisao.tipo is 'corridor':
			pcs_in_corridor += divisao.getComputadores
	
	# Fazer lista com tuplos('tipo', nr_pcs)
	# Inverter consoante nr_pcs para ficar com o valor mais alto na primeira posicao
	# Retornar o tipo

	values_stored = [('generic', pcs_in_generic), ('single', pcs_in_single), ('double', pcs_in_double), ('corridor', pcs_in_corridor), ('conference room', pcs_in_conference), ('suite', pcs_in_suite)]
	values_stored.sort(key=snd, reverse=True)

	predominancia = values_stored[0][0]

	print(f"To find computers, our best chance is in %s." %predominancia)


# PERGUNTA 5

def individual_mais_perto(array_divisoes):

	G = nx.Graph()
	edge_list = getEdges
	G.add_edges_from(edge_list)

	pass

# PERGUNTA 6

# Não necessáriamente o mais curto
def percurso_para_elevador(array_divisoes):
	
	# Sabemos 100% que o agente começa no elevador, e que a única maneira de ir para o elevador é por passar pelo corredor1
	# get current position
	# pesquisar de onde estamos até chegar ao elevador
	# no final append de 'elevador'
	# Devolver uma lista ordenada

	G = nx.Graph()
	edge_list = getEdges(array_divisoes)
	G.add_edges_from(edge_list)

	dest = 'corredor1'

	if curr_room is 'corredor1':
		path = ['elevador']
	elif curr_room is 'porta':
		start = room_ant
		path = pesquisa(start, dest, minimap, [])
		path.append('elevador')
	else:
		start = curr_room
		path = pesquisa(start, dest, minimap, [])
		path.append('elevador')

	path.reverse()
	print("Por ordem, o caminho é o respetivo:")
	print(path)
				

# PERGUNTA 7

def estimativa_de_encontrar_livros(array_divisoes):
	pass

# PERGUNTA 8
					
def probabilidade_mesa_sem_livros_com_uma_cadeira(array_divisoes):
	pass




# ---------------------------------------------------------------
# odometry callback
def callback(data):
	
	global x_ant, y_ant, curr_room, room_ant, minimap

	x=data.pose.pose.position.x-15
	y=data.pose.pose.position.y-1.5

	# show coordinates only when they change
	
	if x != x_ant or y != y_ant:
		curr_room = present_room(x,y)
		print (" x=%.1f y=%.1f : %s") % (x,y,curr_room)
		
		if curr_room is not room_ant or curr_room is not "elevador" and curr_room not in id_divisoes(minimap):
			newdivisao = Divisao.Divisao()
			newdivisao.id = curr_room
			minimap.append(newdivisao)
		else:
			divisao = getDivisao(curr_room, minimap)
			divisao2 = getDivisao(room_ant, minimap)
			if (divisao.suitecheck(divisao2)):
				divisao.viz.append(room_ant)
				divisao.tipo = "suite"
			
			
	
	x_ant = x
	y_ant = y
	if curr_room is not "porta" or curr_room is not "elevador":
		room_ant = curr_room

# ---------------------------------------------------------------
# object_recognition callback
def callback1(data):
	global obj_ant
	obj = data.data
	if obj != obj_ant and data.data != "":
		print ("object is %s") %data.data
	obj_ant = obj
		
# ---------------------------------------------------------------
# questions_keyboard callback
def callback2(data):

	print ("question is %s") %data.data
	question = data.data

	if question is '1':
		#quartosOcupados(minimap)
		pass
	elif question is '2':
		#suite_finder(minimap)
		pass
	elif question is '3':
		#searchPeople(minimap)
		pass
	elif question is '4':
		#predominancia_computadores(minimap)
		pass
	elif question is '5':
		pass
	elif question is '6':
		percurso_para_elevador(minimap)
	elif question is '7':
		pass
	elif question is '8':
		pass
	else:
		print("Not recognizable")

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