from sudoku import Propagacao

def buscaBacktracking(csp):
    csp.aplicarPropagacaoInicial()
    print(csp)
    print()
    return _backtrack(csp)

def _backtrack(csp):
    if csp.estadoFinal():
        return True

    #print(csp)
    var = csp.buscarVariavelNaoAtribuida()
    dominio = csp.ordenarValoresDoDominio(var)

    for val in dominio:
        csp.atribuir(var, val)

        #O problema pode falhar de duas maneiras: pela propagação de consequências de uma atribuição, ou pelo backtracking.

        #Se a propagação não falhar...
        if csp.propagar(var, val):
            print(csp)
            print()
            #Se o próprio backtracking não falhar...
            if _backtrack(csp):
                return result
            else:
                print(csp)
                print()
        else:
            print(csp)
            print()

        #Em caso de falha
        import pdb; pdb.set_trace();
        csp.restaurar(var, val, resultado.atribuidosAutomaicamente)
        print(csp)
        print()


    print(csp)
    return False
