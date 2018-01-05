from sudoku import Estado

def buscaBacktracking(csp):
    #import pdb; pdb.set_trace();
    csp.aplicarPropagacaoInicial()
    return _backtrack(csp)

def _backtrack(csp):
    if csp.estadoFinal():
        return True

    #print(csp)
    var = csp.buscarVariavelNaoAtribuida()
    dominio = csp.ordenarValoresDoDominio(var)
    estado = Estado(var)

    for val in dominio:
        csp.atribuir(var, val, estado)

        #O problema pode falhar de duas maneiras: pela propagação de consequências de uma atribuição, ou pelo backtracking.

        #Se a propagação não falhar...
        if csp.propagar(var, val):
            if _backtrack(csp):
                return True

        #Em caso de falha...
        csp.restaurar(estado)

    return False
