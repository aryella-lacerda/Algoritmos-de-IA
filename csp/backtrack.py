def buscaBacktracking(csp):
    csp.aplicarPropagacaoInicial()
    print(csp)
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
            #Se o próprio backtracking não falhar...
            if _backtrack(csp):
                return result
            else:
                print(csp)
        else:
            print(csp)

        #Em caso de falha
        csp.removerAtribuicao(var)
        csp.removerPropagacao(var, val)
    return False
