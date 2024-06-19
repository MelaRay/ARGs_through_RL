import random
import Actions2 
import MyModelNN as MyNN
import torch
import Codages
import json
import EtatInitial

#Module to build ARGs after training, when learning with the same initial state
#Feature vector: blocks of 3 SNPs overlapping by 1 step shift

L = 10 #number of markers
DICT_ETAT_FINAL = {(0,0,0,0,0,0,0,0,0,0) : 1} #final state

#Model
model = MyNN.MyModel()

with open("pop2", "r") as fp:
     POP = json.load(fp)

#File to stock the genealogy
nomFichier2 = 'textFiles/tests.txt'

#File to stock length of genealogies
nomFichier3 = 'textFiles/tests.txt'

#File to stock length of genealogies
with open(nomFichier3, 'a') as f2:
    f2.writelines('Longueur' + "\t" + 'n' + "\t" + 'Genealogies' + "\t" + 'Echantillon' + "\t" + 'Methode')

plafond = 300

nbrEch = 60 #number of samples
nbrGen = 1 #number of genealogies to build per sample
indexSize = 0
sampleSizes = [40, 60, 100]

indexEch = 0
n = 0

#Building ARGs after learning process
for new in range(nbrEch):

    if(new < 46):
        nomModele = 'model_echant' + str(new) + '_new.pth'
        model.load_state_dict(torch.load(nomModele))
    else:
        nomModele = 'model_echant' + str(new) + '.pth'
        model.load_state_dict(torch.load(nomModele))

    indexEch = indexEch + n

    #change sample size
    if new % 20 == 0:
        n = sampleSizes[indexSize]
        indexSize = indexSize + 1

    for gen in range(nbrGen):
        #initial state
        dictEtatS = EtatInitial.S0_all(POP, indexEch, n, range(len(POP)))
        etatS = Codages.Blocs3Plus(dictEtatS, L-2)

        random.seed(gen)

        steps = 0
        while (dictEtatS != DICT_ETAT_FINAL) and (steps < plafond) :
            #possible next states
            etatSuivantS = Actions2.coalID(dictEtatS)
            etatSuivantS = etatSuivantS  + Actions2.Mutation(dictEtatS, L)
            etatSuivantS = etatSuivantS  + Actions2.coalDif(dictEtatS)
            etatSuivantS = etatSuivantS  + Actions2.recombin(dictEtatS)

            #estimated value of each next state
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
            
        with open(nomFichier3, 'a') as f2:
            f2.writelines('\n')
            f2.writelines(str(steps) + "\t" + str(n) + "\t" + str(gen) + "\t" + str(new)+ "\t" + 'RL')

        print(gen)
        print(steps)


