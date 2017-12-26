from time import sleep
from labirinto import Element, Index

def busca(problema, tipo):

    if tipo == 'P': from pilha import Pilha as Est
    elif tipo == 'L': from fila import Fila as Est
    else: from filaPrioridade import FilaPrioridade as Est

    if tipo == 'C': candidatos = Est(problema.ordenarPorCusto)
    elif tipo == 'G': candidatos = Est(problema.ordenarPorHeuristicaGulosa)
    elif tipo == 'A': candidatos = Est(problema.ordenarPorSoma)
    else: candidatos = Est()

    visitados = []
    candidatos.push(problema.estadoInicial)

    while candidatos:
        atual = candidatos.pop()
        if not problema.estadoFinal(atual):
            novos = problema.expandir(atual)
            candidatos.push(novos)
            # print(problema)
            # print(len(candidatos))
            # sleep(0.04)
        else:
            return problema.solution
