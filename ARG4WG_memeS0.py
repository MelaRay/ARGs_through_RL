import random
import Actions5
import MyModelNN as MyNN
import EtatInitial
import json

#Module to build ARGs with ARG4WG, for 60 samples used when learning with same initial state

L = 10 #number of markers
DICT_ETAT_FINAL = {(0,0,0,0,0,0,0,0,0,0) : 1} #final state

#File to stock length of genealogies
nomFichier3 = 'textFiles/test.txt'

nbrEch = 60 #number of samples 
nbrGen = 1 #number of genealogies to build per sample

#File to stock length of genealogies
with open(nomFichier3, 'a') as f2:
    f2.writelines('Longueur' + "\t" + 'n' + "\t" + 'Genealogies' + "\t" + 'Echantillon' + "\t" + 'Methode')

#Simulated population
with open("pop2", "r") as fp:
     POP = json.load(fp)

indexSize = 0
sampleSizes = [40, 60, 100]
indexEch = 0
n = 0

for new in range(nbrEch):

    indexEch = indexEch + n

    if new % 20 == 0:
        n = sampleSizes[indexSize]
        indexSize = indexSize + 1

    for gen in range(nbrGen):

        steps = 0

        dictEtatS = dictEtatS = EtatInitial.S0_all(POP, indexEch, n, range(len(POP)))
        random.seed(gen)

        while (dictEtatS != DICT_ETAT_FINAL and steps < 400):
            #possible coalescences and next states
            Coal = Actions5.coalID(dictEtatS)
            CoalDif = Actions5.coalDif(dictEtatS)
            etatSuivantS = Coal[0] + CoalDif[0] #possible next states
            actionsPoss = Coal[1] + CoalDif[1] #actions leading to next states
            if len(actionsPoss) != 0:
                indexSPrime = random.randint(0, len(etatSuivantS) - 1)
                dictEtatS = etatSuivantS[indexSPrime]
            else:
                #possibles mutations and next states
                Mut = Actions5.Mutation(dictEtatS, L)
                etatSuivantS = etatSuivantS + Mut[0] #possible next states
                actionsPoss = actionsPoss + Mut[1] #actions leading to next states

                if len(actionsPoss) != 0:
                    indexSPrime = random.randint(0, len(etatSuivantS) - 1)
                    dictEtatS = etatSuivantS[indexSPrime]
                else:
                    #if no coalescence and no mutation possible, do recombination
                    dictEtatS = Actions5.recombin(dictEtatS, L)
                    steps = steps + 1

            steps = steps + 1

        with open(nomFichier3, 'a') as f2:
            f2.writelines('\n')
            f2.writelines(str(steps) + "\t" + str(n) + "\t" + str(gen) + "\t" + str(new)+ "\t" + 'ARG4WG')

    