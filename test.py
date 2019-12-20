import networkx as nx
import Divisao

G = nx.Graph()

d1 = Divisao.Divisao()
d1.id = "what"
d1.adicionarCadeira("cadeira1")
d1.adicionarCama("cama1")
d1.adicionarComputador("pc")
d1.adicionarLivro("book1")
d1.adicionarMesa("mesa1")
d1.adicionarPessoa("pessoa1")
d1.tipo = "normal"

d2 = Divisao.Divisao()
d2.id = "poopoo"
d2.adicionarCadeira("cadeira1")
d2.adicionarCama("cama1")
d2.adicionarComputador("pc")
d2.adicionarLivro("book1")
d2.adicionarMesa("mesa1")
d2.adicionarPessoa("pessoa1")
d2.tipo = "normal"

