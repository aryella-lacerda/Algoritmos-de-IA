from sudoku import Estado

def buscaBacktracking(csp):
    import pdb; pdb.set_trace()
    csp.aplicarPropagacaoInicial()
    return _backtrack(csp)

def _backtrack(csp):
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
        #Em caso de falha...
        csp.restaurar(estado)

    return False
