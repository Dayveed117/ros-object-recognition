# Classe que corresponde às salas



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
		self.tipo = "generic"
		self.camas = []
		self.cadeiras = []
		self.mesas = []
		self.livros = []
		self.pessoas = []
		self.computadores = []
		self.ocupado = False



	# Adders para os arrays atributos

	def adicionarCama(self, nome):
		self.camas.append(nome)

	def adicionarCadeira(self, nome):
		self.cadeiras.append(nome)
	
	def adicionarMesa(self, nome):
		self.cadeiras.append(nome)
	
	def adicionarLivro(self, nome):
		self.livros.append(nome)

	def adicionarPessoa(self, nome):
		self.pessoas.append(nome)

	def adicionarComputador(self, nome):
		self.computadores.append(nome)



	# Getters para nao ter de escrever sempre len(...)

	def getCamas(self):
		return len(self.camas)
	
	def getCadeiras(self):
		return len(self.cadeiras)
	
	def getMesas(self):
		return len(self.mesas)

	def getLivros(self):
		return len(self.livros)
	
	def getPessoas(self):
		return len(self.pessoas)
	
	def getComputadores(self):
		return len(self.computadores)



	# Ver se existe pelo menos uma pessoa na divisao

	def ver_ocupado(self):
		if self.pessoas > 0:
			self.ocupado = True
		else:
			self.ocupado = False


	# Função para alterar o tipo de quarto consoante os seus conteudos
	
	def tipoQuarto(self):
		if self.getCamas == 1:
			self.tipo = "single"
		elif self.getCamas == 2:
			self.tipo = "double"
		elif self.getCadeiras >= 2 and self.getMesas == 1:
			self.tipo = "conference room"
		else:
			self.tipo = "generic"
	
	
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
