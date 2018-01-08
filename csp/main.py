from re import findall
from sudoku import Sudoku
from backtrack import buscaBacktracking
from minimosConflitos import minimosConflitos
from copy import deepcopy

def main():

    with open("sudEasy.txt") as entrada:

        matriz = []
        linhas = entrada.readlines()
        for linha in linhas:
            #O formato mais legível para o sudoku inclui tanto ' ' quanto '|' como delimitadores, e por isso STRING.split() não foi usado. O módulo RE (Expressões Regulares) faz um trabalho chato em uma linha legível de código. 5/5!

            #Busque todo padrão de tamanho 1 composto por caracteres númericos, ou seja, busque só os digitos.
            linha = findall("\d", linha)
            if linha:
                linha = [int(i) for i in linha]
                matriz.append(linha)

        sudoku1 = Sudoku(matriz)
        sudoku2 = deepcopy(sudoku1)

        buscaBacktracking(sudoku1)
        print(sudoku1)
        print()

        minimosConflitos(sudoku2)
        print(sudoku2)

if __name__ == "__main__":
    main()
