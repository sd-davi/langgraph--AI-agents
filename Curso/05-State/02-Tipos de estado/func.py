import re

PALAVRAS_URGENTES = ['parado','travado','fora do ar','sistema','urgente','não consigo acessar','erro','erro 500']

def classificarTexto(texto: str)-> tuple[str,str]:
    """
    Função que classifica textos.
    parametro: texto : str
    retorno tupla com categoria do texto e prioridade da mensagem
    """
    mensagem = texto.lower()
    if re.search(r'\b(?:boletos?|cobran[cç]as?|faturas?|reembolsos?|pagamentos?)\b',texto):
        categoria = 'financeira'
    elif re.search(r'\b(?:senha|login|acesso|acessar)\b',texto):
        categoria = 'acesso'
    else:
        categoria = 'geral'
    
    prioridade = 'alta' if any(p in texto for p in PALAVRAS_URGENTES) else 'normal'

    return categoria,prioridade

SLA_HORAS = {
    ('financeiro','alta') : 4,
    ('acesso','alta') : 1,
    ('geral','alta') : 8
}
