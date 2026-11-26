from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage,SystemMessage,AIMessage
from langchain_core.tools import tool
#from langgraph.prebuilt import create_react_agent
from langchain.agents import create_agent
from dotenv import load_dotenv
import os
from pprint import pprint

'''[1] Carregando API KEY'''
load_dotenv()
API_KEY = os.getenv('OPENAI_KEY')

'''[2] Definir modelo'''
llm = ChatOpenAI(model='gpt-6-luna',api_key = API_KEY)

'''[3] Definir System message'''

system_message = SystemMessage('''
    Voce é um assitente, sua função é responder a pergunta do usuário usando preferencialmete
    as tools que possui, se não tiver nenhuma tool que possar ser usada para responder a
    pergunta, voce pode responder com seu conhecimento.
''')

'''[4] Tools'''
@tool
def somar(valores: str):
    '''Soma dois valores separados por virgula'''
    try:
        a,b = map(float,valores.split(','))
        return str(a+b)
    except Exception as e:
        return f'Erro ao somar: {str(e)}'

@tool
def multiplicar(valores: str):
    '''Multiplica dois valores separados por virgula'''
    try:
        a,b = map(float,valores.split(','))
        return str(a*b)
    except Exception as e:
        return f'Erro ao multiplicar: {str(e)}'


'''[5] Criando lista de tolls'''
tools = [somar,multiplicar]

'''[6] Criando react Agent'''
graph = create_agent(
    model=llm,
    tools=tools,
    system_prompt=system_message
)
exportGraph = graph

'''[7] Extraindo resposta final'''
def extrairResposta(resultado):
    resposta = [m for m in resultado['messages'] if isinstance(m,AIMessage) and m.text]
    if resposta:
        return resposta[-1].text
    else:
        return 'Nenhuma resposta final encontrada'
'''[8] Testando agente'''

if __name__ == '__main__':
    entrada01 = HumanMessage(content='Quanto é 5+5?')
    resposta01 = exportGraph.invoke({'messages':[entrada01]})
    #r = extrairResposta(resposta01)
    pprint(resposta01)


    '''entrada02 = HumanMessage(content='Quando é 5*5?')
    resposta02 = exportGraph.invoke({'message':[entrada02]})
    r2 = extrairResposta(resposta02)
    print(r2)
    entrada03 = HumanMessage(content='O que é AI?')
    resposta03 = exportGraph.invoke({'message':[entrada03]})
    r3 = extrairResposta(resposta03)
    print(r3)'''










