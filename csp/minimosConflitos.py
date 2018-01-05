from sudoku import Sudoku
from time import sleep

def minimosConflitos(csp, maxIter = 10000):
    csp.atribuirEstadoAleatorio()
    maxIter = maxIter
    nIter = 0
    import pdb; pdb.set_trace()
    while True:
    
        if csp.estadoFinal():
            return True

        var = csp.varEmConflito()
        val, conf = csp.valQueMinizaConflito(var)
        csp.atribuirMC(var, val, conf)
        nIter += 1

        print(csp)
        print()
    print('MAXED OUT')
