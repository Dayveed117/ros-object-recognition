#!/usr/bin/env python
# encoding: utf8
# Artificial Intelligence, UBI 2019-20
# Modified by: Students names and numbers

import classeQuarto
import classeCorredor
import rospy
from std_msgs.msg import String
from nav_msgs.msg import Odometry

x_ant = 0
y_ant = 0
obj_ant = ''

def present_room(x, y):

	# Paredes Verticais +0.6
	# Paredes Horizontais +0.5
	# Adicionar +/- 0.1 para remover edge situations

	if(y < -1.3):
		return 1
	
	if((x > -11.9) and (5.4 <= y <= 7.4)):
		return 3

	if((-11.9 <= x <= -9.4) and (-1.3 <= y <= 5.4)):
		return 2

	if((-4.0 <= x <= -1.4) and (-1.3 <= y <= 5.4)):
		return 4

	if((x <= -12.3) and (-0.9 <= y <= 2.4)):
		return 5

	if((x <= -12.3) and (2.9 <= y <= 7.4)):
		return 6

	if((x <= -11.0) and (y >= 7.8)):
		return 7

	if((-10.5 <= x <= -6.1) and (y >= 7.8)):
		return 8

	if((-5.7 <= x <= -1.1) and (y >= 7.8)):
		return 9

	if((x >= -0.6) and (y >= 7.8)):
		return 10
	
	if((x >= -0.9) and (2.2 <= y <= 4.9)):
		return 11

	if((x >= -0.9) and (-1.0 <= y <= 1.7)):
		return 12

	if((-9.0 <= x <= -7.1) and (-1.0 <= y <= 4.9)):
		return 13

	if((-6.5 <= x <= -4.5) and (-1.0 <= y <= 4.9)):
		return 14
	
	return -1

divisaoAtual = -1

total_quartos = 10
total_corredores = 4 


array_quartos = []
array_corredores = []

for i in range( total_quartos ):
	array_quartos.append( classeQuarto.Quarto())

for i in range ( total_corredores ):
	array_corredores.append( classeCorredor.Corredor())



# ---------------------------------------------------------------
# odometry callback
def callback(data):
	global x_ant, y_ant, divisaoAtual

	x=data.pose.pose.position.x-15
	y=data.pose.pose.position.y-1.5
	# show coordinates only when they change
	if x != x_ant or y != y_ant:
		print " x=%.1f y=%.1f, sala=%d" % (x,y,present_room(x,y))

		divisaoAtual = present_room(x, y)
		#print "sala=%d" %divisaoAtual	
	x_ant = x
	y_ant = y

# ---------------------------------------------------------------
# object_recognition callback
def callback1(data):
	global obj_ant, divisaoAtual, array_quartos

	obj = data.data
	if obj != obj_ant and data.data != "":
		print "object is %s" % data.data
		
		print "Test %d" %divisaoAtual
		if divisaoAtual > 4:
			array_quartos[ divisaoAtual - 5].addobj(data.data)
			print ""
			print "Camas %d, Livros %d, Cadeiras %d, Pessoas %d, Computadores %d, Mesas %d" %(len(array_quartos[ divisaoAtual - 5].camas), len(array_quartos[ divisaoAtual - 5].livros), len(array_quartos[ divisaoAtual - 5].cadeiras), len(array_quartos[ divisaoAtual - 5].pessoas), len(array_quartos[ divisaoAtual - 5].computador), len(array_quartos[ divisaoAtual - 5].mesas)) 
		
	obj_ant = obj
		
# ---------------------------------------------------------------
# questions_keyboard callback
def callback2(data):
	print "question is %s" % data.data

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
