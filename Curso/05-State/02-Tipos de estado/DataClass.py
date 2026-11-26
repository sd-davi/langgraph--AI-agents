from func import classificarTexto, SLA_HORAS
from langgraph.graph import START,END,StateGraph
from dataclasses import dataclass
from typing import Literal
from Typedict_state import montaGrafo

@dataclass
class TicketDT:
    cliente : str 
    mensagem : str
    categoria : str | None = None
    prioridade : str = 'normal'
    sla_horas : int = 24

def classificarDT(state: TicketDT) -> dict:
    categoria,prioridade = classificarTexto(state.mensagem)
    return {'categoria' : categoria, 'prioridade': prioridade}

def definirSLA(state: TicketDT) -> dict:
    return {'sla_horas' : SLA_HORAS.get((state.categoria,state.prioridade),24) }

grafo = montaGrafo(TicketDT,classificarDT,definirSLA)
print(grafo.invoke({'cliente': 'Ana Maria', 'mensagem':'O sistema esta travado não consigo pagar o boleto'}))
print(grafo.invoke({'cliente': 42, 'mensagem':'O sistema esta travado não consigo pagar o boleto'}))
