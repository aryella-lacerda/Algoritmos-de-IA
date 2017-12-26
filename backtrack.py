def buscaBacktracking(csp):
    ''' Retorna uma solução, ou um status de fracasso.'''
    #Estado é representado por uma lista.
    #Lista vazia é estado inicial genérico. Cada CSP deve implementar seu estado inicial.
    return _backtrack(csp, [])

def _backtrack(csp, atual):
    if csp.estadoFinal(atual):
        return atual

    var = csp.buscarVariavelNaoAtribuida()
    dominio = csp.ordenarValoresDoDominio(var)
    for valor in dominio:
        csp.atribuir(var, val, atual)

        #O problema pode falhar de duas maneiras: pela propagação de consequências de uma atribuição, ou pelo backtracking.

        #Se a propagação não falhar...
        if csp.propagar(var, val):
            #Se o próprio backtracking não falhar...
            if _backtrack(csp, atual):
                return result

        #Em caso de falha
        csp.removerAtribuicao(var, val, atual)
        csp.removerPropagacao(var, val)
    return False
