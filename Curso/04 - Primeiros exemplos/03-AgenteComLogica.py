from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from langchain_core.tools import tool
from langgraph.graph import StateGraph
from pydantic import BaseModel
from dotenv import load_dotenv
import os
from pprint import pprint

'''[1] Carregando API KEY'''
load_dotenv()
API_KEY = os.getenv('OPENAI_KEY')

'''[2] Definir modelo'''
llm = ChatOpenAI(model='gpt-6-luna',api_key = API_KEY)

'''[3] Criando State do grafo '''
class graphState(BaseModel):
    input: str 
    output: str
    tipo: str = None

'''[4] Funções ficticias'''

def calcular(state: graphState) -> graphState:
    return graphState(input = state.input, output = 'O resultado é: 22')

def responder(state: graphState) -> graphState:
    #testar sem lista
    resposta = llm.invoke([HumanMessage(content=state.input)])
    return graphState(input = state.input,
                      output = resposta.text)   # se  der erro usar resposta.content

def responderSaudacao(state: graphState) -> graphState:
    return graphState(input = state.input, output = 'Ola, bom dia!')


'''[5] Classificador de funções'''

def classificar(state: graphState)->graphState:
    pergunta = state.input.lower()
    if any(palavra in pergunta for palavra in ['soma','quanto é','+','calcular']):
        tipo = 'calculo'
    elif any(palavra in pergunta for palavra in ['quem','onde','quando','por que','qual']):
        tipo = 'curiosidade'
    elif any(palavra in pergunta for palavra in ['ola','bom dia','oi','eai']):
        tipo = 'saudacao'
    return graphState(input = state.input, output = '', tipo= tipo)


'''[6] Montando Grafo'''
# Adicionando nodes
graph = StateGraph(graphState)
graph.add_node('classificar',classificar)
graph.add_node('calcular',calcular)
graph.add_node('responder',responder)
graph.add_node('saudacao',responderSaudacao)

# Adionando condicional edges
graph.add_conditional_edges(
    'classificar',
    lambda state:{
        'calculo':'calcular',
        'curiosidade': 'responder',
        'saudacao': 'responderSaudacao'
    }[state.tipo]
)

# Adicionando entrada e saida
graph.set_entry_point('classificar')
graph.set_finish_point(['calcular','responder','saudacao'])
export_graph = graph.compile()

'''[7] Testando'''

if __name__ == '__main__':
    exemplos = ['Quando é 5 + 11 ?', 'Quem descobriu o Brasil?', 'Ola , tudo bem?', 'Quem é o maior jogador de futebol da historia?']

    for exemplo in exemplos:
        resposta = export_graph.invoke(graphState(input=exemplo,output=''))
        print(f'Pergunta: {exemplo}\nResposta: {resposta["output"]}')




