from labirinto import Labirinto
from busca import busca
from copy import deepcopy
from time import sleep

def main():

    with open("lab6.txt") as infile:

        # Read and format labirinth
        dimensions = infile.readline().split(" ")
        nLines, nColumns = int(dimensions[0]), int(dimensions[1])
        lines = infile.readlines()
        labirinto = []
        for line in lines:
            line = line.rstrip()
            labirinto.append(line.split(" "))

        labirintoL = Labirinto(nLines, nColumns, labirinto)
        labirintoP = deepcopy(labirintoL)
        labirintoC = deepcopy(labirintoL)
        labirintoG1 = deepcopy(labirintoL)
        labirintoA1 = deepcopy(labirintoL)
        labirintoG2 = deepcopy(labirintoL)
        labirintoA2 = deepcopy(labirintoL)

        busca(labirintoL, "L")
        print(labirintoL)
        print("LARGURA: ", labirintoL.solution)
        print(labirintoL.result())
        sleep(5)

        busca(labirintoP, "P")
        print(labirintoP)
        print("PROFUNDIDADE: ", labirintoP.solution)
        print(labirintoP.result())
        sleep(5)

        busca(labirintoC, "C")
        print(labirintoC)
        print("CUSTO UNIFORME: ", labirintoC.solution)
        print(labirintoC.result())
        sleep(5)

        busca(labirintoG1, "G", 1)
        print(labirintoG1)
        print("GULOSO H1: ", labirintoG1.solution)
        print(labirintoG1.result())
        sleep(5)

        busca(labirintoG2, "G", 2)
        print(labirintoG2)
        print("GULOSO H2: ", labirintoG2.solution)
        print(labirintoG2.result())
        sleep(5)

        busca(labirintoA1, "A", 1)
        print(labirintoA1)
        print("A* H1: ", labirintoA1.solution)
        print(labirintoA1.result())
        sleep(5)

        busca(labirintoA2, "A", 2)
        print(labirintoA2)
        print("A*: H2", labirintoA2.solution)
        print(labirintoA2.result())


if __name__ == "__main__":
    main()
