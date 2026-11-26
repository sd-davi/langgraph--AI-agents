from typing import TypedDict, Annotated
from langgraph.graph import END,START,StateGraph
from langgraph.errors import InvalidUpdateError
import operator

'''[1] Estado'''
class EstadoTeste(TypedDict):
    resultados: list[str]

'''[2] funções simuladas'''

def buscaDocs(state: EstadoTeste) -> EstadoTeste:
    return {'resultados' :['Docs: Frete grátis acima de 199 R$']}

def buscaWeb(stat: EstadoTeste) -> EstadoTeste:
    return {'resultados' :['Web: Entrega em até 5 dias uteis']}


# AQUI VAMOS SIMULAR 2 ERROS
'''[3] Grafo - SEQUENCIAL'''
b = StateGraph(EstadoTeste)
b.add_node('documentos',buscaDocs)
b.add_node('web',buscaWeb)

b.add_edge(START,'documentos')
b.add_edge('documentos','web')
b.add_edge('web',END)
# Na chamada sequencial o ultimo node sobrescreve o estado
print(b.compile().invoke({'resultados' : []}))


'''[3.5] Grafo - PARALELO'''
g = StateGraph(EstadoTeste)
g.add_node('documentos',buscaDocs)
g.add_node('web',buscaWeb)

g.add_edge(START,'documentos')
g.add_edge(START,'web')
g.add_edge('documentos',END)
g.add_edge('web',END)

# Aqui vamos ter um erro de update de estado paralelo
# as duas funções tentam sobrescrever o estado ao mesmo tempo
try:
    print(g.compile().invoke({'resultados' : []}))
except InvalidUpdateError as error:
    print(str(error).splitlines()[0])

''' Como corrigir isso ? Usando Annotated + reducer'''
# vamos usar o operator.add
# completo
class EstadoAcumula(TypedDict):
    resultados: Annotated[list[str],operator.add] # concatena listas
    chamadas : Annotated[int,operator.add] # soma valores

def buscaEmDocs(state: EstadoAcumula):
    return {'resultados' :['Docs: Frete grátis acima de 199 R$'], 'chamadas':1}

def buscaNaWeb(stat: EstadoAcumula):
    return {'resultados' :['Web: Entrega em até 5 dias uteis'],'chamadas':1}


h = StateGraph(EstadoAcumula)
h.add_node('docs',buscaEmDocs)
h.add_node('web',buscaNaWeb)

h.add_edge(START,'docs')
h.add_edge(START,'web')
h.add_edge('docs',END)
h.add_edge('web',END)

acumula = h.compile()
print(acumula.invoke({'resultados': ['Entrada do usuario'], 'chamadas': 0}))

