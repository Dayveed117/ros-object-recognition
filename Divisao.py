#!/usr/bin/env python
# encoding: utf8

# Parse de doubles

def name_parse(nome):
	full = nome.split("_", 1)
	return (full[0], full[1])
	

class Divisao:

	# Construtor da divisão

	def __init__(self):

		self.id = ""
		self.tipo = "generic"
		self.camas = []
		self.cadeiras = []
		self.mesas = []
		self.livros = []
		self.pessoas = []
		self.computadores = []
		self.viz = []
		self.pm = (0,0)

	def equals(self, other):
		if self.id == "":
			return False
		return self.id == other.id


	# Adders para os arrays atributos

	def adicionarCama(self, nome):
		self.camas.append(nome)

	def adicionarCadeira(self, nome):
		self.cadeiras.append(nome)
	
	def adicionarMesa(self, nome):
		self.mesas.append(nome)
	
	def adicionarLivro(self, nome):
		self.livros.append(nome)

	def adicionarPessoa(self, nome):
		self.pessoas.append(nome)

	def adicionarComputador(self, nome):
		self.computadores.append(nome)
	
	def adicionarViz(self, nome):
		self.viz.append(nome)



	# Getters para nao ter de escrever sempre len(...)

	def getNumCamas(self):
		return len(self.camas)
	
	def getNumCadeiras(self):
		return len(self.cadeiras)
	
	def getNumMesas(self):
		return len(self.mesas)

	def getNumLivros(self):
		return len(self.livros)
	
	def getNumPessoas(self):
		return len(self.pessoas)
	
	def getNumComputadores(self):
		return len(self.computadores)

	def getNumViz(self):
		return len(self.viz)


	# Separar corredores e salas

	def checkHalls(self):
		c = 0
		if self.tipo == "corredor":
			c += 1
		return c

	def checkRooms(self):
		c = 0
		if self.id.startswith("sala"):
			c += 1
		return c


	# Função para alterar o tipo de quarto consoante os seus conteudos
	
	def tiparQuarto(self):

		if self.tipo == "suite" or self.tipo == 'corredor':
			pass
		elif self.getNumCamas() is 1:
			self.tipo = "single"
		elif self.getNumCamas() is 2:
			self.tipo = "double"
		elif self.getNumCadeiras() >= 2 and self.getNumMesas() is 1:
			self.tipo = "conference room"
		else:
			self.tipo = "generic"
		

	def suiteCheck(self, other):

		if self.tipo == "corredor" or other.tipo == 'corredor':
			return False
		elif (self.getNumCamas() + other.getNumCamas()) >= 2:
			if self.id in other.viz and other.id in self.viz:
				return True
		return False
	
	# Função para adicionar objetos
	# Alguams vezes sao identificados mais do que um objeto de cada vez, daí precisarmos de poder separar por ',' primeiro

	def addobj(self, nome, viz):
		
		# Algumas vezes acabam com ','
		rm_shadytrail = nome.rstrip(',')

		if ',' in rm_shadytrail:
			
			elem = rm_shadytrail.split(",")
			for sing_nome in elem:
				
				(tipo, designacao) = name_parse(sing_nome)

				if tipo == "bed":
					if designacao not in self.camas: 
						self.adicionarCama(designacao)
				elif tipo == "chair":
					if designacao not in self.cadeiras:
						self.adicionarCadeira(designacao)
				elif tipo == "table":
					if designacao not in self.mesas:
						self.adicionarMesa(designacao)
				elif tipo == "book":
					if designacao not in self.livros:
						self.adicionarLivro(designacao)
				elif tipo == "person":
					if designacao not in self.pessoas:
						self.adicionarPessoa(designacao)
				elif tipo == "computer":
					if designacao not in self.computadores:
						self.adicionarComputador(designacao)

		else:

			(tipo, designacao) = name_parse(rm_shadytrail)
			
			if tipo == "bed":
				if designacao not in self.camas:
					self.adicionarCama(designacao)
			elif tipo == "chair":
				if designacao not in self.cadeiras:
					self.adicionarCadeira(designacao)
			elif tipo == "table":
				if designacao not in self.mesas:
					self.adicionarMesa(designacao)
			elif tipo == "book":
				if designacao not in self.livros:
					self.adicionarLivro(designacao)
			elif tipo == "person":
				if designacao not in self.pessoas:
					self.adicionarPessoa(designacao)
			elif tipo == "computer":
				if designacao not in self.computadores:
					self.adicionarComputador(designacao)
