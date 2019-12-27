#!/usr/bin/env python
# encoding: utf8
# Artificial Intelligence, UBI 2019-20
# Modified by: Students names and numbers

import rospy
from std_msgs.msg import String
from nav_msgs.msg import Odometry
import Divisao
from Support import *
import networkx as nx
import time


# VARIÁVEIS CHAVE
book_time = time.time()
book_help = []
x = 0
y = 0
x_ant = 0
y_ant = 0
obj_ant = ''
curr_room = ''	
room_ant = 'corredor1'
minimap = []

# PERGUNTA 1

def quartosNaoOcupados(array_divisoes):

	# Percorrer todas as divisoes, ver se está ou não ocupado

	naoOcupados = 0

	for divisao in array_divisoes:
		if divisao.getNumPessoas() is 0 and divisao.tipo != "corredor":
			naoOcupados += 1
	
	print "I have seen %d rooms without people so far." %naoOcupados

	
# PERGUNTA 2

def suite_finder(array_divisoes):

	# Percorrer todas as divisões, contar número de divisões suíte
	# No final dividir por 2 pois uma suíte é uma agregação de 2 quartos sobre certas condições
	
	contSuite = 0

	for divisao in array_divisoes:
		if divisao.tipo == "suite":
			contSuite += 1

	if contSuite is not 0:
		print "I have found %d suite rooms so far." %(contSuite/2)
	else:
		print("I haven't found any suites so far.")
	

# PERGUNTA 3

def searchPeople(array_divisoes):

	# Procurar por pessoas nas divisões, separar por tipo
	# Contar ocurrências

	pessoasCorredores = 0
	pessoasQuartos = 0

	for divisao in array_divisoes:
		if divisao.tipo == "corredor":
			pessoasCorredores += divisao.getNumPessoas()
		else:
			pessoasQuartos += divisao.getNumPessoas()

	if pessoasCorredores > pessoasQuartos:
		print "More people in hallways compared to room."
	elif pessoasCorredores < pessoasQuartos:
		print "More people in the rooms compared to hallways"
	else:
		print "There are exactly the same number of people inside and outside of rooms (%d)." %pessoasQuartos

# PERGUNTA 4

def predominancia_computadores(array_divisoes):
	
	# Procurar por computadores nas divisões, separar por tipo
	# Contar ocurrências em cada tipo de quarto
	# Extrair o tipo do maior contador


	pcs_in_generic = 0
	pcs_in_single = 0
	pcs_in_double = 0
	pcs_in_corridor = 0
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
		elif divisao.tipo == 'corridor':
			pcs_in_corridor += divisao.getNumComputadores()
	
	# Fazer lista com tuplos('tipo', nr_pcs)
	# Inverter consoante nr_pcs para ficar com o valor mais alto na primeira posicao
	# Retornar o tipo

	values_stored = [('generics', pcs_in_generic), ('singles', pcs_in_single), ('doubles', pcs_in_double), ('corridors', pcs_in_corridor), ('suites', pcs_in_suite)]
	values_stored.sort(key=snd, reverse=True)

	if values_stored[0][1] is not 0:
		print "To find computers, our best chance is in %s." %(values_stored[0][0])
	else:
		print "I haven't found a single computer yet."

# PERGUNTA 5

def individual_mais_perto(array_divisoes):

	# Verificar se há quartos do tipo individual, verificar se está num quarto individual caso sim
	# Utilizar um grafo com arestas pesadas caso haja quartos individuais mas não esteja num deles

	if singleCheck(array_divisoes):
		
		if curr_room != 'porta':
			div = getDivisao(curr_room, array_divisoes)
		else:
			div = getDivisao(room_ant, array_divisoes)
		
		start = div.id		
		
		if div.tipo != 'single':
		
			path_distances = []

			G = nx.Graph()
			G = getEdges_weight(array_divisoes, G, start, (x,y))

			for divisao in array_divisoes:

				if divisao.tipo == 'single':
					#dist é um valor inteiro pois temos preenchemos o 2º e 3º parâmetro com um nodo
					dist = nx.shortest_path_length(G, start, divisao.id, weight='dist')
					path_distances.append((divisao.id, dist))
					print "%s: %.1f" %(divisao.id, dist)	
		
			path_distances.sort(key=snd)
			print "The closest single room is %s in a distance of %.1f." %(path_distances[0][0], path_distances[0][1])
		
		else:
			print "The closest single room is %s, in which we are in" %start
	else:
		print("There are no single rooms as far as i know.")
	
# PERGUNTA 6
 
def percurso_para_elevador(array_divisoes):
	
	# Utilizar pesquisa em largura para encontrar o melhor caminho para o elevador
	# Para chegar ao elevador passa-se SEMPRE pelo corredor 1
	# Utilizar pesquisa em largura para chegar ao corredor 1, no final adiciona-se o elevador
	# Não usa peso nas arestas

	path = []
	dest = 'corredor1'

	if curr_room != dest:
		G = nx.Graph()
		edge_list = getEdges(array_divisoes)
		G.add_edges_from(edge_list)

		if curr_room == 'porta':
			start = room_ant
		else:
			start = curr_room

		path = pesquisa(G, start, dest, [])		
	
	path.reverse()
	path.append('elevador')
	print("We can take the respective path:")
	print(path)
				

# PERGUNTA 7

def estimativa_de_encontrar_livros(array_divisoes):

	# Estimativa feita segundo uma simples regra de 3 simples
	# É inicializado um temporizador no início do programa
	# Estimativa depende do número de livros encontrados até ao momento e do tempo atual do temporizador
	
	tempos = 0
	mediaTempo = 0

	for _,tempo in book_help:
		tempos += float(tempo)
	
	if len(book_help) > 0:
		mediaTempo = tempos/len(book_help)
		
	if mediaTempo > 0:
		estimativa = (1*120.0/mediaTempo)
		print "I estimate finding about %.2f books in 2 minutes." %estimativa
	else:
		print("I cant estimate with either no books found or timer being 0.")

# PERGUNTA 8
					
def probabilidade_mesa_sem_livros_com_uma_cadeira(array_divisoes):

	# Nas divisões que têm mais do que uma cadeira,
	# Contar quantas delas não têm livros e têm pelo menos uma mesa
	# (Tentação de aplicação de uma probabilidade condicionada)

	# P(m and ~b | >1 chair)
	# P(m and ~b)
	# ------------
	# P(>1 chair)

	contA = 0
	contB = 0

	for divisao in array_divisoes:
		if divisao.getNumCadeiras() >= 1:
			contB += 1
			if divisao.getNumLivros() is 0 and divisao.getNumMesas() >= 1:
				contA += 1
		
	
	if contB is 0 or contA is 0:
		print("My data says the chance is 0")
	else:
		prob = contA / float(contB)
		print "We have about %.2f chance of finding a table in those conditions as of now." %prob

# Pergunta 9

def inventory(array_divisoes):

	# Imprime para o ecrã variáveis importantes
	# Imprime atributos da divisão atual

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
		print(time.time() - book_time)
		print(id_divisoes(array_divisoes))
	else:
		print("Doors are dumb.")

# ---------------------------------------------------------------
# odometry callback
def callback(data):
	
	global x, y, x_ant, y_ant, curr_room, room_ant, minimap
	
	bad_rooms = (room_ant, 'porta')

	x=data.pose.pose.position.x-15
	y=data.pose.pose.position.y-1.5

	# show coordinates only when they change
	if x != x_ant or y != y_ant:
		(ponto_medio, curr_room) = present_room(x,y)
		print (" x=%.1f y=%.1f : %s <- %s") % (x,y,curr_room, room_ant)

		# Adicionar objetos ao minimapa
		if curr_room not in id_divisoes(minimap) and curr_room != 'porta':

			newdivisao = Divisao.Divisao()
			newdivisao.id = curr_room
			newdivisao.pm = ponto_medio

			if curr_room.startswith('corredor'):
				newdivisao.tipo = 'corredor'
			
			minimap.append(newdivisao)

		# Lógica de adicionar vizinhos
		# Verificação de suite quando se troca de divisão
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

	global obj_ant, curr_room, minimap, book_time, book_help
	bad_rooms = ("porta")

	obj = data.data
	if obj != obj_ant and data.data != "":
		print ("object is %s") %data.data

		# Ao encontrar um livro adicionar à lista book_help com o tempo necessário para o encontrar
		if parsebook(obj, book_help, time.time() - book_time):
			# Recomeçar timer asism que encontra um livro
			book_time = time.time()
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
