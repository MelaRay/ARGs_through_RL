import random
import Actions2 
import MyModelNN as MyNN
import torch
import Codages
import EtatInitial
import json

#Module to build ARGs after training on validation set (to select best model for each agent)
#Feature vector: blocks of 3 SNPs overlapping by 1 step shift

L = 10 #number of markers
DICT_ETAT_FINAL = {(0,0,0,0,0,0,0,0,0,0) : 1} #final state

#Model
model = MyNN.MyModel()

#File to stock the best model for each agent
nomFichier = 'textFiles/Valid_bestModel_Agent1et2.txt'

#File to stock length of genealogies
nomFichier3 = 'textFiles/Valid_Agent1et2.txt'

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

nbrEch = 20 #number of samples 
nbrGen = 1 #number of genealogies to build per sample

#File to stock length of genealogies
with open(nomFichier3, 'a') as f2:
    f2.writelines('Echantillon' + "\t" + 'Longueur' + "\t" + 'm' + "\t" + 'Genealogies' + "\t" + 'Agent')

#File to stock best model per agent
with open(nomFichier, 'a') as f2:
    f2.writelines('Agent' + "\t" + 'BestModel')

nbrModels = int((100_000 - 40_000)/(sizeTrain/5) + 1) #number of models per agents
m = 25 #sample size
plafond = 300 #max steps
Seeds =[123, 125, 126, 124, 128, 131, 132, 805, 804, 799, 795, 796, 797]
nbrAgents = len(Seeds) #number of agents trained
bestMod = [0] * nbrAgents

#Building ARGs after learning process
for t in range(nbrAgents):

    seed = Seeds[t]
    #best average range to choose best model for the agent
    bestLen = plafond 
    bestProp = 1

    for e in range(nbrModels):

        #model to use
        noModel = e * 2000 + 40000
        nomModele = 'model_m5All_new_' + str(noModel) + '_' + str(seed) + '.pth'
        model.load_state_dict(torch.load(nomModele))

        #list to keep length of all genealogies built with this model
        allLen = []

        #Number and proportion of infinite genealogies
        nbrInfGen = 0
        propInfGen = 0

        for new in range(nbrEch):
            
            listeLongueur = [0] * nbrGen

            for gen in range(nbrGen):
                #initial state
                dictEtatS = EtatInitial.S0(POP, (new + 1), m, sizeValid, indexValid)
                etatS = Codages.Blocs3Plus(dictEtatS, L-2)
                
                steps = 0
                while (dictEtatS != DICT_ETAT_FINAL) and (steps < plafond) :
                    #possible next states
                    etatSuivantS = Actions2.coalID(dictEtatS)
                    etatSuivantS = etatSuivantS  + Actions2.Mutation(dictEtatS, L)
                    etatSuivantS = etatSuivantS  + Actions2.coalDif(dictEtatS)
                    etatSuivantS = etatSuivantS  + Actions2.recombin(dictEtatS)

                    #estimated value of each next state
                    random.seed(e)
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
                        #next state (highest estimated value)    
                        allIndexSPrime = [x for x in range(len(v)) if v[x] == max(v)]
                        indexSPrime = random.choice(allIndexSPrime)
                        
                    #s' becomes s
                    dictEtatS = etatSuivantS[indexSPrime]
                    etatS = Codages.Blocs3Plus(dictEtatS, L-2)
                   
                    steps = steps + 1

                listeLongueur[gen] = steps
            
            if(min(listeLongueur) != plafond):
                allLen.append(min(listeLongueur))
            else:
                nbrInfGen = nbrInfGen + 1
            
            with open(nomFichier3, 'a') as f2:
                f2.writelines('\n')
                f2.writelines(str(new) + "\t" + str(min(listeLongueur)) + "\t" + str(m) + "\t" + str(noModel)+ "\t" + str(t))

            print(new)
            print(str(min(listeLongueur)))

        #proportion of infinite-length ARGs
        propInfGen = nbrInfGen/nbrEch
        if(len(allLen) != 0):
            aveLen = sum(allLen) / len(allLen)
        else:
            aveLen = 300

        if(propInfGen < bestProp):
            bestLen = aveLen
            bestProp = propInfGen
            bestMod[t] = noModel
        elif(propInfGen == bestProp and aveLen < bestLen):
            bestLen = aveLen
            bestProp = propInfGen
            bestMod[t] = noModel

    print(bestMod[t])
    with open(nomFichier, 'a') as f1:
            f1.writelines('\n')
            f1.writelines(str(t) + "\t" + str(bestMod[t]))
