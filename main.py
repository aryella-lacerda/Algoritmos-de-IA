from labirinto import Labirinto
from busca import busca
from copy import deepcopy

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
        labirintoG = deepcopy(labirintoL)
        labirintoA = deepcopy(labirintoL)

        import pdb; pdb.set_trace() # add pdb here

        busca(labirintoL, "L")
        busca(labirintoP, "P")
        busca(labirintoC, "C")
        busca(labirintoG, "G")
        busca(labirintoA, "A")

        print(labirintoL)
        print("LARGURA: ", labirintoL.solution)
        print(labirintoL.result())

        print(labirintoP)
        print("PROFUNDIDADE: ", labirintoP.solution)
        print(labirintoP.result())

        print(labirintoC)
        print("CUSTO UNIFORME: ", labirintoC.solution)
        print(labirintoC.result())

        print(labirintoG)
        print("GULOSO: ", labirintoG.solution)
        print(labirintoG.result())

        print(labirintoA)
        print("A*: ", labirintoA.solution)
        print(labirintoA.result())

if __name__ == "__main__":
    main()
