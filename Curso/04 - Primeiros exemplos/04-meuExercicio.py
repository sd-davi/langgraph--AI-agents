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

'''[3] Criando StateGraph'''

class GraphState(BaseModel):
    input: str
    output: str
    tipo : str= None


'''[4] Funções '''
def calcular(state: GraphState) -> GraphState:
    valores = state.input
    a,b = map(float,valores.split('+'))
    return GraphState(input=state.input, output =str(a+b))

def responder(state: GraphState) -> GraphState:
    pergunta = state.input
    resposta = llm.invoke([HumanMessage(content=pergunta)])
    return GraphState(input=state.input,
                      output=resposta.text)

def saudacao(state: GraphState) -> GraphState:
    frase = state.input
    if any(palavra in frase for palavra in ['ola','bom dia','oi','eai']):
        return GraphState(input=state.input,
                      output='Olá, como posso ajudar ?')

def classificar(state: GraphState)->GraphState:
    pergunta = state.input.lower()
    if any(palavra in pergunta for palavra in ['soma','quanto é','+','calcular']):
        tipo = 'calculo'
    elif any(palavra in pergunta for palavra in ['quem','onde','quando','por que','qual']):
        tipo = 'curiosidade'
    else:
        tipo = 'saudacao'
    return GraphState(input = state.input, output = '', tipo= tipo)

'''[5] Criando graph'''
graph = StateGraph(GraphState)

# Adição dos nodes
graph.add_node('classificar',classificar)
graph.add_node('calcular',calcular)
graph.add_node('curiosidade',responder)
graph.add_node('saudacao',saudacao)

#Adicionado condicional edge
graph.add_conditional_edges(
    'classificar',
    lambda state :{
        'calculo': 'calcular',
        'curiosidade': 'curiosidade',
        'saudacao': 'saudacao'
    }[state.tipo]
)
#Adicionando entrada e saída
graph.set_entry_point('classificar')
graph.set_finish_point(['calcular','curiosidade','saudacao'])

'''[6] Compilando Grafo'''
compiledGraph = graph.compile()

'''[7] Teste'''

if __name__ == '__main__':
    exemplos = ['5+11', 
                'Quem descobriu o Brasil?', 
                'ola , tudo bem?', 
                'Quem é o maior jogador de futebol da historia?']
    
    for exemplo in exemplos:
        resposta = compiledGraph.invoke(GraphState(input=exemplo,output=''))
        print(f'Pergunta: {exemplo}\nResposta: {resposta["output"]}')

