#!/usr/bin/env python
# encoding: utf8

# Parse de doubles

def tipo_obj(nome):
	nome.split("_", maxsplit=1)
	return nome[0]

def nome_obj(nome):
	nome.split("_", maxsplit=1)
	return nome[1]

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
		self.ocupado = False
		self.viz = []
		self.pm = 0

	def equals(self, other):
		if self.id is "":
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



	# Ver se existe pelo menos uma pessoa na divisao

	def ver_ocupado(self):
		if self.pessoas > 0:
			self.ocupado = True
		else:
			self.ocupado = False


	# Função para alterar o tipo de quarto consoante os seus conteudos
	
	def tipoQuarto(self):
		if self.getNumCamas == 1:
			self.tipo = "single"
		elif self.getNumCamas == 2:
			self.tipo = "double"
		elif self.getNumCadeiras >= 2 and self.getNumMesas == 1:
			self.tipo = "conference room"
		else:
			self.tipo = "generic"
	
	def suiteCheck(self, other):
		if self.camas > 2:
			if self.id in other.viz and other.id in self.viz:

				return True
		return False
		
	
	
	# Função para adicionar objetos
	# Alguams vezes sao identificados mais do que um objeto de cada vez, daí precisarmos de poder separar por ',' primeiro

	def addobj(self, nome):
		
		if ',' in nome:
			nome.split(",")
			for sing_nome in nome:
				
				tipo = tipo_obj(sing_nome)
				designacao = nome_obj(sing_nome)

				if tipo is "bed":
					if designacao not in self.camas:
						self.adicionarCama(designacao)
				elif tipo is "chair":
					if designacao not in self.cadeiras:
						self.adicionarCadeira(designacao)
				elif tipo is "table":
					if designacao not in self.mesas:
						self.adicionarMesa(designacao)
				elif tipo is "book":
					if designacao not in self.livros:
						self.adicionarLivro(designacao)
				elif tipo is "person":
					if designacao not in self.pessoas:
						self.adicionarPessoa(designacao)
				elif tipo is "computer":
					if designacao not in self.computadores:
						self.adicionarComputador(designacao)

		else:
			tipo = tipo_obj(sing_nome)
			designacao = nome_obj(sing_nome)
			
			if tipo is "bed":
				if designacao not in self.camas:
					self.adicionarCama(designacao)
			elif tipo is "chair":
				if designacao not in self.cadeiras:
					self.adicionarCadeira(designacao)
			elif tipo is "table":
				if designacao not in self.mesas:
					self.adicionarMesa(designacao)
			elif tipo is "book":
				if designacao not in self.livros:
					self.adicionarLivro(designacao)
			elif tipo is "person":
				if designacao not in self.pessoas:
					self.adicionarPessoa(designacao)
			elif tipo is "computer":
				if designacao not in self.computadores:
					self.adicionarComputador(designacao)
