#Classe
#
#Objectos: bed, book, chair, computer, door, person, table

def tipo_obj(nome):
		nome.split("_", maxsplit=1)
		return nome[0]

def nome_obj(nome):
		nome.split("_", maxsplit=1)
		return nome[1]

class Quarto:
	def __init__(self):
		self.tipo= "generic"
		self.camas = []
		self.livros = []
		self.cadeiras = []
		self.pessoas = []
		self.computadores = [] 
		self.mesas = [] 
		self.quartoLigado = -1
		self.portaCoordenadas = []
		
			

	def adicionarCama(self, nomeCama):
		self.camas.append( nomeCama )

	def adicionarLivro(self, livro):
		self.livros.append( livro )

	def adicionarCadeira(self, cadeira):			
		self.cadeiras.append( cadeira )

	def adicionarPessoa(self, pessoa):
		self.pessoas.append( pessoa )

	def adicionarMesa(self, mesa):
		self.pessoas.append( mesa )

	def adicionarComputador(self, pc):
		self.pessoas.append( pc )

	def addobj(self, nome):
	
		if ',' in nome:
			nome.split(",")
			for sing_nome in nome:
			
				tipo = tipo_obj(sing_nome)
				designacao = nome_obj(sing_nome)

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
					pass


	def tipoQuarto(self):
		if( len(self.camas) == 1 ):
			self.tipo = "single"
		elif (len(self.camas) == 2):
			self.tipo = "double"
		elif (len(self.cadeiras) >= 2 and len(self.mesas) == 1 ):
			self.tipo = "conference room"
		else:
			self.tipo = "generic" 



