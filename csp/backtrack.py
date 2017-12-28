def backtrack(csp):
    if csp.estadoFinal():
        return True

    var = csp.buscarVariavelNaoAtribuida()
    dominio = csp.ordenarValoresDoDominio(var)
    for valor in dominio:
        csp.atribuir(var, val)

        #O problema pode falhar de duas maneiras: pela propagação de consequências de uma atribuição, ou pelo backtracking.

        #Se a propagação não falhar...
        if csp.propagar(var, val):
            #Se o próprio backtracking não falhar...
            if backtrack(csp):
                return result

        #Em caso de falha
        csp.removerAtribuicao(var, val)
        csp.removerPropagacao(var, val)
    return False
