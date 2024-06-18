import random
import Actions5
import MyModelNN as MyNN
import torch
import Codages
import EtatInitial
import json

#Module pour cronstruire des genealogies apres l'apprentissage
#En utilisant le codage des etats avec des blocs de 3 marqueurs avec chevauchement

L = 10 #number of markers
DICT_ETAT_FINAL = {(0,0,0,0,0,0,0,0,0,0) : 1} #final state


#File to stock length of genealogies
nomFichier3 = 'textFiles/ARG4WG_echantTests_BON.txt'

#nbrEch = 20 #number of samples 
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

    dictEtatS = EtatInitial.S0(POP, (gen + 1), m, sizeTest, indexTest)
    #print(dictEtatS)

    #dictEtatS = {(0, 0, 1, 0, 1, 1, 1, 0, 0, 0) : 1, (0, 0, 0, 0, 0, 0, 0, 0, 0, 0) : 2, (0, 0, 0, 0, 0, 1, 1, 0, 0, 0) : 27, (0, 0, 1, 1, 0, 0, 0, 1, 0, 1) : 6, (1, 0, 0, 0, 0, 1, 1, 0, 1, 0) : 1, (0, 0, 1, 1, 0, 0, 0, 0, 0, 1) : 2, (1, 1, 0, 0, 0, 1, 1, 0, 1, 0) : 4, (0, 0, 1, 1, 0, 0, 0, 1, 0, 0) : 19}
    #dictEtatS = {(0, 0, 1, 0, 1, 1, 1, 0, 0, 0) : 1, (0, 0, 0, 0, 0, 0, 0, 0, 0, 0) : 1, (0, 0, 0, 0, 0, 1, 1, 0, 0, 0) : 1, (0, 0, 1, 1, 0, 0, 0, 1, 0, 1) : 1, (1, 0, 0, 0, 0, 1, 1, 0, 1, 0) : 1, (0, 0, 1, 1, 0, 0, 0, 0, 0, 1) : 1, (1, 1, 0, 0, 0, 1, 1, 0, 1, 0) : 1, (0, 0, 1, 1, 0, 0, 0, 1, 0, 0) : 1}
    
    #dictEtatS = {(0, 0, 0, 0, 1, 1, 0, 0, 0, 1) : 14, (1, 0, 0, 0, 0, 0, 1, 0, 0, 0) : 9, (0, 0, 1, 1, 0, 0, 0,0, 0, 0) : 7, (0, 0, 0, 0, 0, 0, 0, 1, 0, 0) : 4, (0, 0, 0, 0, 0, 0, 0, 0, 0, 0) : 13, (0, 0, 0,0, 0, 1, 0, 0, 0, 1) : 4, (0, 0, 0, 0, 1, 1, 0, 0, 1, 1) : 2, (0, 0, 1, 1, 0, 0, 1, 0, 0, 0) : 4,(0, 1, 0, 0, 1, 1, 0, 0, 0, 1) : 3}

    #ech2 msprime
    #dictEtatS = {(0, 0, 0, 0, 1, 1, 0, 0, 0, 1) : 1, (1, 0, 0, 0, 0, 0, 1, 0, 0, 0) : 1, (0, 0, 1, 1, 0, 0, 0,0, 0, 0) : 1, (0, 0, 0, 0, 0, 0, 0, 1, 0, 0) : 1, (0, 0, 0, 0, 0, 0, 0, 0, 0, 0) : 1, (0, 0, 0,0, 0, 1, 0, 0, 0, 1) : 1, (0, 0, 0, 0, 1, 1, 0, 0, 1, 1) : 1, (0, 0, 1, 1, 0, 0, 1, 0, 0, 0) : 1,(0, 1, 0, 0, 1, 1, 0, 0, 0, 1) : 1}
    #avec toutes les sequences
    #dictEtatS = {(0, 0, 0, 0, 1, 1, 0, 0, 0, 1) : 14, (1, 0, 0, 0, 0, 0, 1, 0, 0, 0) : 9, (0, 0, 1, 1, 0, 0, 0,0, 0, 0) : 7, (0, 0, 0, 0, 0, 0, 0, 1, 0, 0) : 4, (0, 0, 0, 0, 0, 0, 0, 0, 0, 0) : 13, (0, 0, 0,0, 0, 1, 0, 0, 0, 1) : 4, (0, 0, 0, 0, 1, 1, 0, 0, 1, 1) : 2, (0, 0, 1, 1, 0, 0, 1, 0, 0, 0) : 4,(0, 1, 0, 0, 1, 1, 0, 0, 0, 1) : 3}
    
    #meme echantillon (ech1) avec marqueurs 0, 1, 9
    #dictEtatS = {(0, 0, 1, 0, 1, 1, 1, 0, 0, 0) : 1, (0, 0, 0, 0, 0, 0, 0, 0, 0, 0) : 1, (0, 0, 0, 0, 0, 1, 1, 0, 0, 0) : 1, (0, 0, 1, 1, 0, 0, 0, 1, 0, 1) : 1, (1, 0, 0, 0, 0, 1, 1, 0, 1, 0) : 1, (0, 0, 1, 1, 0, 0, 0, 0, 0, 1) : 1, (1, 1, 0, 0, 0, 1, 1, 0, 1, 0) : 1, (0, 0, 1, 1, 0, 0, 0, 1, 0, 0) : 1}
    #avec toutes les sequences
    #dictEtatS = {(0, 0, 1, 0, 1, 1, 1, 0, 0, 0) : 1, (0, 0, 0, 0, 0, 0, 0, 0, 0, 0) : 2, (0, 0, 0, 0, 0, 1, 1, 0, 0, 0) : 27, (0, 0, 1, 1, 0, 0, 0, 1, 0, 1) : 6, (1, 0, 0, 0, 0, 1, 1, 0, 1, 0) : 1, (0, 0, 1, 1, 0, 0, 0, 0, 0, 1) : 2, (1, 1, 0, 0, 0, 1, 1, 0, 1, 0) : 4, (0, 0, 1, 1, 0, 0, 0, 1, 0, 0) : 19}
    
    while (dictEtatS != DICT_ETAT_FINAL and steps < 400):
        #possible actions and next states
        Coal = Actions5.coalID(dictEtatS)
        CoalDif = Actions5.coalDif(dictEtatS)
        etatSuivantS = Coal[0] + CoalDif[0] #etats suivants possibles
        actionsPoss = Coal[1] + CoalDif[1] #actions menant aux etats suivants
        if len(actionsPoss) != 0:
            indexSPrime = random.randint(0, len(etatSuivantS) - 1)
            dictEtatS = etatSuivantS[indexSPrime]
        else:
            Mut = Actions5.Mutation(dictEtatS, L)
            etatSuivantS = etatSuivantS + Mut[0] #etats suivants possibles
            actionsPoss = actionsPoss + Mut[1] #actions menant aux etats suivants

            if len(actionsPoss) != 0:
                indexSPrime = random.randint(0, len(etatSuivantS) - 1)
                dictEtatS = etatSuivantS[indexSPrime]
            else:
                dictEtatS = Actions5.recombin(dictEtatS, L)
                steps = steps + 1

        steps = steps + 1
        #print(dictEtatS)
    
    print(steps)

    with open(nomFichier3, 'a') as f2:
        f2.writelines('\n')
        f2.writelines(str(steps) + "\t" + str(m) + "\t" + str(gen) + "\t" + 'ARG4WG')

    