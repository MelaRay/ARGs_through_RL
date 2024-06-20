import random
import Actions2 
import MyModelNN as MyNN
import torch
import Codages
import EtatInitial
import json

#Module to build ARGs (after training) on the test set
#Feature vector: blocks of 3 SNPs overlapping by 1 step shift

L = 10 #number of markers
DICT_ETAT_FINAL = {(0,0,0,0,0,0,0,0,0,0) : 1} #final state

#trained model
model = MyNN.MyModel()

#File to stock length of genealogies
nomFichier3 = 'textFiles/Test_Agent1a13.txt'

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

nbrEch = 100 #number of samples 
nbrGen = 1 #number of genealogies to build per sample

#Models to use
ListeNomModele = []
indAgent =  [123, 125, 126, 124, 128, 131, 132, 805, 804, 799, 795, 796, 797]
indMod = [56, 96, 80, 66, 82, 84, 92, 70, 88, 98, 98, 70, 98]
for j in range (len(indMod)):
    mod = indAgent[j]
    g = indMod[j]
    nom = 'model_m5All_new_' + str(g * 1000) + '_' + str(mod) + '.pth'
    ListeNomModele = ListeNomModele + [nom]

#File to stock length of genealogies
with open(nomFichier3, 'a') as f2:
    f2.writelines('Echantillon' + "\t" + 'Longueur' + "\t" + 'm' + "\t" + 'Agent')

nbrAgents = len(ListeNomModele) #number of agents trained
nbrModels = 1 #number of models per agents

#Building ARGs after learning process
for t in range(nbrAgents):

    m = 50 #sample size
    plafond = 400 #max steps

    for e in range(nbrModels):

        #model to use
        nomModele = ListeNomModele[t]
        model.load_state_dict(torch.load(nomModele))

        for new in range(nbrEch):

            listeLongueur = [0] * nbrGen

            for gen in range(nbrGen):
                #initial state
                dictEtatS = EtatInitial.S0(POP, (new + 1), m, sizeTest, indexTest)
                etatS = Codages.Blocs3Plus(dictEtatS, L-2)      
                
                steps = 1
                while (dictEtatS != DICT_ETAT_FINAL) and (steps < plafond) :
                    #possible next states
                    etatSuivantS = Actions2.coalID(dictEtatS)
                    etatSuivantS = etatSuivantS  + Actions2.Mutation(dictEtatS, L)
                    etatSuivantS = etatSuivantS  + Actions2.coalDif(dictEtatS)
                    etatSuivantS = etatSuivantS  + Actions2.recombin(dictEtatS)

                    #choosing next state
                    #estimated values of possible next states
                    v = [0] * len(etatSuivantS) 
                    j = 0
                    etatFinalTrouve = False
                    for etat in etatSuivantS:
                        if etat == DICT_ETAT_FINAL:
                            v[j] = 0
                            etatFinalTrouve = True
                            indexSPrime = j
                        else:
                            input = Codages.Blocs3Plus(etat, L-2)
                            v[j] = model(torch.tensor([input], dtype = torch.float32))
                        
                        j = j+1

                    if not etatFinalTrouve:
                        #next state with highest estimated value   
                        allIndexSPrime = [x for x in range(len(v)) if v[x] == max(v)]
                        indexSPrime = random.choice(allIndexSPrime)
                        
                    #s' becomes s
                    dictEtatS = etatSuivantS[indexSPrime]
                    etatS = Codages.Blocs3Plus(dictEtatS, L-2)
                   
                    steps = steps + 1

                listeLongueur[gen] = steps

            with open(nomFichier3, 'a') as f2:
                f2.writelines('\n')
                f2.writelines(str(new) + "\t" + str(min(listeLongueur)) + "\t" + str(m) + "\t" + str(t))

            print(new)
            print(str(min(listeLongueur)))
