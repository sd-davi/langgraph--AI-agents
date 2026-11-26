from func import classificarTexto, SLA_HORAS
from typing import Literal, NotRequired, TypedDict
from langgraph.graph import START,END,StateGraph

'''
TypedDict

[1] É um dict comum em execução (sem validação)
[2] Campos que só existem depois de algum node devem ser opcionais
    > NotRequired[] ou  total = False
[3] Prefira usar state.get('campo')
    > Usar state['campo'] pode causar KeyError se ele ainda não existir
'''

'''[1] State'''
class TicketTD(TypedDict):
    cliente : str
    mensagem : str
    categoria : NotRequired[str]
    prioridade : NotRequired[Literal['normal','alta']]
    sla_horas : NotRequired[int]

'''[2] Funções'''

def classificarTD(state: TicketTD) -> dict:
    categoria,prioridade = classificarTexto(state.get('mensagem'))
    return {'categoria' : categoria, 'prioridade': prioridade}

def definirSLA(state) -> dict:
    return {'sla_horas' : SLA_HORAS.get((state['categoria'],state['prioridade']),24) }

def montaGrafo(state,classificarTD, definirSLA):
    grafo = StateGraph(state)
    # Adicionar Nodes
    grafo.add_node('classificar',classificarTD)
    grafo.add_node('definir',definirSLA)

    #Adicionar arestas
    grafo.add_edge(START,'classificar')
    grafo.add_edge('classificar','definir')
    grafo.add_edge('definir',END)
    
    #Compila grafo
    return grafo.compile()

#grafo = montaGrafo(TicketTD,classificarTD,definirSLA)
#print(grafo.invoke({'cliente': 'Ana Maria', 'mensagem':'O sistema esta travado não consigo pagar o boleto'}))


