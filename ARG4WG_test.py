import random
import Actions5
import MyModelNN as MyNN
import EtatInitial
import json

#Module to build ARGs with ARG4WG on test set

L = 10 #number of markers
DICT_ETAT_FINAL = {(0,0,0,0,0,0,0,0,0,0) : 1} #final state

#File to stock length of genealogies
nomFichier3 = 'textFiles/ARG4WG_echantTests_BON.txt'

nbrGen = 100 #number of genealogies to build

#File to stock length of genealogies
with open(nomFichier3, 'a') as f2:
    f2.writelines('Longueur' + "\t" + 'm' + "\t" + 'Genealogies' + "\t" + 'Agent')

m = 50 #sample size

#Simulated population
with open("pop1", "r") as fp:
     POP = json.load(fp)

taillePop = 15_500 #sample size
sizeTrain = 10_000 #size training set
sizeValid = 500 #size validation set
sizeTest = 5_000 #size test set

random.seed(1234)
allIndexPop = list(range(taillePop))
indexTrain = random.sample(allIndexPop , k = sizeTrain) #training set

#removing training set from sample
for ind in indexTrain:
    allIndexPop.remove(ind)

indexValid = random.sample(allIndexPop, k = sizeValid) #validation set

indexTest = allIndexPop #test set

#removing validation set from test set
for ind in indexValid:
    indexTest.remove(ind)


for gen in range(nbrGen):
    steps = 0

    #initial state
    dictEtatS = EtatInitial.S0(POP, (gen + 1), m, sizeTest, indexTest)
   
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
            #possible mutations and next states
            Mut = Actions5.Mutation(dictEtatS, L)
            etatSuivantS = etatSuivantS + Mut[0] #etats suivants possibles
            actionsPoss = actionsPoss + Mut[1] #actions menant aux etats suivants

            if len(actionsPoss) != 0:
                indexSPrime = random.randint(0, len(etatSuivantS) - 1)
                dictEtatS = etatSuivantS[indexSPrime]
            else:
                #if no coalescence and no mutation possible, do recombination
                dictEtatS = Actions5.recombin(dictEtatS, L)
                steps = steps + 1

        steps = steps + 1
    
    print(steps)

    with open(nomFichier3, 'a') as f2:
        f2.writelines('\n')
        f2.writelines(str(steps) + "\t" + str(m) + "\t" + str(gen) + "\t" + 'ARG4WG')

    