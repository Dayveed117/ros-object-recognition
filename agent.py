#!/usr/bin/env python
# encoding: utf8
# Artificial Intelligence, UBI 2019-20
# Modified by: Students names and numbers

import rospy
from std_msgs.msg import String
from nav_msgs.msg import Odometry
import Divisao

x_ant = 0
y_ant = 0
obj_ant = ''	

# Fazer parse de doubles
def fst(tuple):
	return tuple[0]

def snd(tuple):
	return tuple[1]

def present_room(x, y):

	# Paredes Verticais +-0.6
	# Paredes Horizontais +-0.5
	# Adicionar +- 0.1 consoante a orientação da parede para remover edge situations

	if(y < -1.3):
		return "Corredor1"
	
	if((x > -11.9) and (5.4 <= y <= 7.4)):
		return "Corredor3"

	if((-11.9 <= x <= -9.4) and (-1.3 <= y <= 5.4)):
		return "Corredor2"

	if((-4.0 <= x <= -1.4) and (-1.3 <= y <= 5.4)):
		return "Corredor4"

	if((x <= -12.3) and (-0.9 <= y <= 2.4)):
		return "Sala5"

	if((x <= -12.3) and (2.9 <= y <= 7.4)):
		return "Sala6"

	if((x <= -11.0) and (y >= 7.8)):
		return "Sala7"

	if((-10.5 <= x <= -6.1) and (y >= 7.8)):
		return "Sala8"

	if((-5.7 <= x <= -1.1) and (y >= 7.8)):
		return "Sala9"

	if((x >= -0.6) and (y >= 7.8)):
		return "Sala10"
	
	if((x >= -0.9) and (2.2 <= y <= 4.9)):
		return "Sala11"

	if((x >= -0.9) and (-1.0 <= y <= 1.7)):
		return "Sala12"

	if((-9.0 <= x <= -7.1) and (-1.0 <= y <= 4.9)):
		return "Sala13"

	if((-6.5 <= x <= -4.5) and (-1.0 <= y <= 4.9)):
		return "Sala14"
	
	return "Porta"

lista_divisoes



# PERGUNTA 1

def quartosOcupados(array_divisoes):

	contOcupados = 0
	bad_divisoes = ["corredor", "elevador"]


	# Percorrer todas as divisoes, ver se está ou não ocupado

	for divisao in array_divisoes:
		if not divisao.ver_ocupado() and divisao.tipo not in bad_divisoes:
			contOcupados += 1
	
	print(f"There are %d rooms occupied." %contOcupados)

	
# PERGUNTA 2

def suite_finder(array_divisoes):
	# Implementar com os grafos
	pass

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
		print(f"More people in hallways compared to rooms, about %d" %diff)
	elif pessoasCorredores < pessoasQuartos:
		print(f"More people in the rooms compared to hallways." %diff)
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

	print(f"To find computers, our best chance is in %s" %predominancia)


# PERGUNTA 5

def individual_mais_perto(array_divisoes):
	pass

# PERGUNTA 6

# Não necessáriamente o mais curto
def percurso_para_elevador(array_divisoes):
	pass

# PERGUNTA 7

def estimativa_de_encontrar_livros(array_divisoes):
	pass

# PERGUNTA 8
					
def probabilidade_mesa_sem_livros_com_uma_cadeira(array_divisoes):
	pass




# ---------------------------------------------------------------
# odometry callback
def callback(data):
	global x_ant, y_ant
	x=data.pose.pose.position.x-15
	y=data.pose.pose.position.y-1.5
	# show coordinates only when they change
	if x != x_ant or y != y_ant:
		curr_space = present_room(x,y)
		print (" x=%.1f y=%.1f : %s") % (x,y,curr_space)
	x_ant = x
	y_ant = y

# ---------------------------------------------------------------
# object_recognition callback
def callback1(data):
	global obj_ant
	obj = data.data
	if obj != obj_ant and data.data != "":
		print ("object is %s") % data.data
	obj_ant = obj
		
# ---------------------------------------------------------------
# questions_keyboard callback
def callback2(data):
	print ("question is %s") % data.data

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
