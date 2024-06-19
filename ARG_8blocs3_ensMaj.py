import random
import Actions2 
import MyModelNN as MyNN
import torch
import Codages
import EtatInitial
import json

#Module to build ARGs after training with ensemble method: Majority 
#Feature vector: blocks of 3 SNPs overlapping by 1 step shift
L = 10 #number of markers
DICT_ETAT_FINAL = {(0,0,0,0,0,0,0,0,0,0) : 1} #final state

#trained model
model = MyNN.MyModel()

#File to stock the genealogy
#nomFichier2 = 'textFiles/NN_MC/tests.txt'

#File to stock length of genealogies
nomFichier3 = 'textFiles/Test_Agent1a13_Maj.txt'

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
m = 50 #size initial state
plafond = 400 #maximum length ARG

#Models to use
ListeNomModele = []
indAgent =  [123, 125, 126, 124, 128, 131, 132, 805, 804, 799, 795, 796, 797]
indMod = [56, 96, 80, 66, 82, 84, 92, 70, 88, 98, 98, 70, 98]
for j in range (len(indMod)):
    mod = indAgent[j]
    g = indMod[j]
    nom = 'model_m5All_new_' + str(g * 1000) + '_' + str(mod) + '.pth'
    ListeNomModele = ListeNomModele + [nom]

listeMod = [ListeNomModele]

#File to stock length of genealogies
with open(nomFichier3, 'a') as f2:
    f2.writelines('Echantillon' + "\t" + 'Longueur' + "\t" + 'm' + "\t" + 'Agent')

#Building ARGs
for e in range(len(listeMod)):

    ListeNomsModele = listeMod[e]
    nbrMod = len(ListeNomsModele)

    for new in range(nbrEch):

        listeLongueur = [0] * nbrGen

        for gen in range(nbrGen):
            #change initial state
            dictEtatS = EtatInitial.S0(POP, (new + 1), m, sizeTest, indexTest)
            etatS = Codages.Blocs3Plus(dictEtatS, L-2)

            #File with ARGs
            # with open(nomFichier2, 'a') as f:
            #     f.writelines('\n')
            #     f.writelines(str(dictEtatS))
            #     f.writelines('\n')
                        
                
            steps = 1
            while (dictEtatS != DICT_ETAT_FINAL) and (steps < plafond) :
                #possible next states
                etatSuivantS = Actions2.coalID(dictEtatS)
                etatSuivantS = etatSuivantS  + Actions2.Mutation(dictEtatS, L)
                etatSuivantS = etatSuivantS  + Actions2.coalDif(dictEtatS)
                etatSuivantS = etatSuivantS  + Actions2.recombin(dictEtatS)

                #estimated values possible next state
                hatValue = torch.zeros((len(etatSuivantS),nbrMod,))
                #for each agent
                for modele in range(nbrMod):

                    nomModele = ListeNomsModele[modele]
                    model.load_state_dict(torch.load(nomModele))
                        
                    j = 0
                    etatFinalTrouve = False
                    for etat in etatSuivantS:
                        if etat == DICT_ETAT_FINAL:
                            hatValue[j, modele] = 0
                            etatFinalTrouve = True
                            indexSPrime = j
                        else:
                            input = Codages.Blocs3Plus(etat, L-2)
                            hatValue[j, modele] = model(torch.tensor([input], dtype = torch.float32))
                            
                        j = j+1

                #highest estimated value per agent    
                v = torch.argmax(hatValue, 0) 

                if not etatFinalTrouve:
                    #majority vote    
                    allIndexSPrime = torch.mode(v)
                    indexSPrime = allIndexSPrime[0]
                        
                #next state s' becomes actual state s
                dictEtatS = etatSuivantS[indexSPrime]
                etatS = Codages.Blocs3Plus(dictEtatS, L-2)

                steps = steps + 1

            listeLongueur[gen] = steps

        with open(nomFichier3, 'a') as f2:
            f2.writelines('\n')
            f2.writelines(str(new) + "\t" + str(min(listeLongueur)) + "\t" + str(m) + "\t" + str(e) + '_Maj')


        print(new)
        print(str(min(listeLongueur)))
