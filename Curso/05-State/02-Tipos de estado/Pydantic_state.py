from func import classificarTexto, SLA_HORAS
from langgraph.graph import START,END,StateGraph
from pydantic import BaseModel, Field, ValidationError
from typing import Literal
from Typedict_state import montaGrafo

'''
Pydantic

[1] Valida e converte tipos ('41' -> 41)
[2] Podemos aplicar Fields
    > limites de tamanho
    > padrões e descrições
[3] No node o estado chega como objeto
    > state.campo
[4] Node devolve dict parcial
'''

'''[1] State'''

class TicketPD(BaseModel):
    cliente : str = Field(min_length=2) # nome tem de ter no minimo 2 letras
    mensagem : str = Field(min_length= 5, description= 'Mensagem enviada pelo cliente')
    categoria : str | None = None
    prioridade : Literal['normal','alta'] = 'normal'
    sla_horas : int = Field(default=24, ge=1, le=72)

'''[2] Funções'''

def classificarPD(state: TicketPD) -> dict:
    categoria,prioridade = classificarTexto(state.mensagem)
    return {'categoria' : categoria, 'prioridade': prioridade}

def definirSLA(state: TicketPD) -> dict:
    return {'sla_horas' : SLA_HORAS.get((state.categoria,state.prioridade),24) }

grafo = montaGrafo(TicketPD,classificarPD,definirSLA)
print(grafo.invoke({'cliente': 'Ana Maria', 'mensagem':'O sistema esta travado não consigo pagar o boleto'}))

# TESTANDO VALIDAÇÕES
try:
    print(grafo.invoke({'cliente': 'A', 'mensagem':'O sistema esta travado não consigo pagar o boleto'}))
except ValueError as erro:
    for e in erro.errors():
        print(f'{e["loc"][0]} : {e["msg"]}')