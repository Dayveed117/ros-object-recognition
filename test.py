import networkx as nx
import Divisao
import math

G = nx.Graph()

d1 = Divisao.Divisao()
d1.id = "1"
d1.adicionarCadeira("cadeira1")
d1.adicionarCama("cama1")
d1.adicionarComputador("pc")
d1.adicionarLivro("book1")
d1.adicionarMesa("mesa1")
d1.adicionarPessoa("pessoa1")
d1.tipo = "normal"
d1.viz = ['2','3','4','5','6']

d2 = Divisao.Divisao()
d2.id = "4"
d2.adicionarCadeira("cadeira1")
d2.adicionarCama("cama1")
d2.adicionarComputador("pc")
d2.adicionarLivro("book1")
d2.adicionarMesa("mesa1")
d2.adicionarPessoa("pessoa1")
d2.tipo = "normal"
d2.viz = ['1','2','3','5']

a = [d1, d2]

def getEdges(array_divisoes):
	
	edges = []
	
	for divisao in array_divisoes:
		l_vizinhos = divisao.viz
		for vizinho in l_vizinhos:
			edges.append([divisao.id, vizinho])
	return edges

def twopoint_distance(p1, p2):
	dist = math.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)
	return dist
	