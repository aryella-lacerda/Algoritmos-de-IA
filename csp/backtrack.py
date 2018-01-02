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
        if csp.foundError(var):
            print('ERRO!!')

        #O problema pode falhar de duas maneiras: pela propagação de consequências de uma atribuição, ou pelo backtracking.

        #Se a propagação não falhar...
        if csp.propagar(var, val):
            print(csp)
            print()
            #Se o próprio backtracking não falhar...
            if _backtrack(csp):
                return result

        #Em caso de falha
        print(csp)
        print()
        csp.restaurar(estado)
        print(csp)
        print()

    print('BACKTRACK')
    print()
    return False
