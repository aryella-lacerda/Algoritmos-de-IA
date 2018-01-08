from time import sleep
from labirinto import Element, Index

def busca(problema, tipo, heuristica = None):

    if tipo == 'P': from aux.pilha import Pilha as Est
    elif tipo == 'L': from aux.fila import Fila as Est
    else: from aux.filaPrioridade import FilaPrioridade as Est

    if heuristica == 1:
        tec = problema.ordenarPorHeuristicaGulosa1
        soma = problema.ordenarPorSoma1
    else:
        tec = problema.ordenarPorHeuristicaGulosa2
        soma = problema.ordenarPorSoma2

    if tipo == 'C': candidatos = Est(problema.ordenarPorCusto)
    elif tipo == 'G': candidatos = Est(tec)
    elif tipo == 'A': candidatos = Est(soma)
    else: candidatos = Est()

    candidatos.push(problema.estadoInicial)

    while candidatos:
        atual = candidatos.pop()
        if not problema.estadoFinal(atual):
            novos = problema.expandir(atual)
            candidatos.push(novos)
        else:
            return problema.solution
