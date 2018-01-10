from sudoku import Estado

expan = 0
backtrack = 0

def buscaBacktracking(csp):
    csp.aplicarPropagacaoInicial()
    _backtrack(csp)
    return (expan, backtrack)

def _backtrack(csp):
    global expan, backtrack

    expan += 1

    if csp.estadoFinal():
        return True

    var = csp.buscarVariavelNaoAtribuida()
    dominio = csp.ordenarValoresDoDominio(var)
    estado = Estado(var)

    for val in dominio:
        csp.atribuir(var, val, estado)

        #Se a propagação não falhar...
        if csp.propagar(var, val):
            #Se o backtracking não falhar...
            if _backtrack(csp):
                return True
            else:
                backtrack += 1

        #Em caso de falha...
        csp.restaurar(estado)

    return False
