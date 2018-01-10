from sudoku import Sudoku
from time import sleep

def minimosConflitos(csp, maxIter = 100000):
    csp.aplicarPropagacaoInicial()
    csp.atribuirEstadoAleatorio()
    maxIter = maxIter
    nIter = 0

    while True:

        if csp.estadoFinal():
            return Inter

        var = csp.varEmConflito()
        val, conf = csp.valQueMinizaConflito(var)
        csp.atribuirMC(var, val, conf)
        nIter += 1

    return nIter
