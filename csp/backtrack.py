from sudoku import Propagacao

def buscaBacktracking(csp):
    csp.aplicarPropagacaoInicial()
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

        import pdb; pdb.set_trace();
        #Se a propagação não falhar...
        propagacao = csp.propagar(var, val)
        if not propagacao.falha:
            #print(csp)
            #Se o próprio backtracking não falhar...
            if _backtrack(csp):
                return result
            else:
                print(csp)
                print('\n\n\n')
        else:
            print(csp)
            print('\n\n\n')

        #Em caso de falha
        csp.removerAtribuicao(var)
        csp.removerPropagacao(var, val)
        csp.removerAtribuicaoAutomatica(propagacao.atribuidosAutomaicamente)

    print(csp)
    return False
