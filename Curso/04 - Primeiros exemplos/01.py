from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage, HumanMessage
from langgraph.graph import StateGraph
from pydantic import BaseModel
from dotenv import load_dotenv
import os

# gera grafo
from langchain_core.runnables.graph import MermaidDrawMethod

''' Exemplo mais simples: Manda mensagem e llm responde'''

'''
[1] Carregando API KEY
'''
load_dotenv()
API_KEY = os.getenv('OPENAI_KEY')

'''
[2] Definir modelo
'''
llm = ChatOpenAI(model='gpt-6-luna',api_key = API_KEY)

'''
[3] Criando StateGraph
'''
class GraphState(BaseModel):
    input: str
    output: str

'''
[4] Função para responder pergunta
'''
def responder(state):
    pergunta = state.input
    resposta = llm.invoke([HumanMessage(content=pergunta)])
    return GraphState(input=state.input,output=resposta.content)

'''
[5] Criando graph
'''
graph = StateGraph(GraphState)
graph.add_node('responder',responder)
graph.set_entry_point('responder')
graph.set_finish_point('responder')

'''
[6] Compilando Grafo
'''
comp = graph.compile()

'''
[7] Teste
'''

if __name__ == '__main__':
    resultado = comp.invoke(GraphState(input="qual a capital do Brasil?",output=""))
    print(resultado)

'''
[8] Visualizar Grafo
'''
print(comp.get_graph().draw_mermaid())
# Vai gerar um código. copiar cód para www.mermaid.live

''' ou '''

grafo_png = comp.get_graph().draw_mermaid_png(
    draw_method=MermaidDrawMethod.API
)
with open('grafo_01.png','wb') as file:
    file.write(grafo_png)