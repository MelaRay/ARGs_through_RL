import random
import Actions2 
import MyModelNN as MyNN
import torch
import Codages
import json
import EtatInitial

#Module pour cronstruire des genealogies apres l'apprentissage
#En utilisant le codage des etats avec des blocs de 3 marqueurs avec chevauchement

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

# listS0 = [{(0, 0, 1, 0, 1, 1, 1, 0, 0, 0) : 1, (0, 0, 0, 0, 0, 0, 0, 0, 0, 0) : 1, (0, 0, 0, 0, 0, 1, 1, 0, 0, 0) : 1, (0, 0, 1, 1, 0, 0, 0, 1, 0, 1) : 1, (1, 0, 0, 0, 0, 1, 1, 0, 1, 0) : 1, (0, 0, 1, 1, 0, 0, 0, 0, 0, 1) : 1, (1, 1, 0, 0, 0, 1, 1, 0, 1, 0) : 1, (0, 0, 1, 1, 0, 0, 0, 1, 0, 0) : 1},
#             {(0, 0, 1, 0, 1, 1, 1, 0, 0, 0) : 1, (0, 0, 0, 0, 0, 0, 0, 0, 0, 0) : 2, (0, 0, 0, 0, 0, 1, 1, 0, 0, 0) : 27, (0, 0, 1, 1, 0, 0, 0, 1, 0, 1) : 6, (1, 0, 0, 0, 0, 1, 1, 0, 1, 0) : 1, (0, 0, 1, 1, 0, 0, 0, 0, 0, 1) : 2, (1, 1, 0, 0, 0, 1, 1, 0, 1, 0) : 4, (0, 0, 1, 1, 0, 0, 0, 1, 0, 0) : 19},
#             {(0, 0, 0, 0, 1, 1, 0, 0, 0, 1) : 1, (1, 0, 0, 0, 0, 0, 1, 0, 0, 0) : 1, (0, 0, 1, 1, 0, 0, 0,0, 0, 0) : 1, (0, 0, 0, 0, 0, 0, 0, 1, 0, 0) : 1, (0, 0, 0, 0, 0, 0, 0, 0, 0, 0) : 1, (0, 0, 0,0, 0, 1, 0, 0, 0, 1) : 1, (0, 0, 0, 0, 1, 1, 0, 0, 1, 1) : 1, (0, 0, 1, 1, 0, 0, 1, 0, 0, 0) : 1,(0, 1, 0, 0, 1, 1, 0, 0, 0, 1) : 1},
#             {(0, 0, 0, 0, 1, 1, 0, 0, 0, 1) : 14, (1, 0, 0, 0, 0, 0, 1, 0, 0, 0) : 9, (0, 0, 1, 1, 0, 0, 0,0, 0, 0) : 7, (0, 0, 0, 0, 0, 0, 0, 1, 0, 0) : 4, (0, 0, 0, 0, 0, 0, 0, 0, 0, 0) : 13, (0, 0, 0,0, 0, 1, 0, 0, 0, 1) : 4, (0, 0, 0, 0, 1, 1, 0, 0, 1, 1) : 2, (0, 0, 1, 1, 0, 0, 1, 0, 0, 0) : 4,(0, 1, 0, 0, 1, 1, 0, 0, 0, 1) : 3}]

#nbrEch = len(listS0)

# listModels = ['model_echant1_test.pth',
#               'model_echant1_test.pth',
#               'model_echant2_test.pth',
#               'model_echant2_test.pth']

nbrEch = 60 #number of samples
nbrGen = 1 #number of genealogies to build per sample
indexSize = 0
sampleSizes = [40, 60, 100]

#listModels = ['model_echant1_test_N0.pth',
#              'model_echant2_test_N0.pth']

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

    if new % 20 == 0:
        n = sampleSizes[indexSize]
        indexSize = indexSize + 1

    for gen in range(nbrGen):
        #initial state
        dictEtatS = EtatInitial.S0_all(POP, indexEch, n, range(len(POP)))
        etatS = Codages.Blocs3Plus(dictEtatS, L-2)

        #On inscrit dans un fichier la genealogie
        # with open(nomFichier2, 'a') as f:
        #     f.writelines('\n')
        #     f.writelines(str(dictEtatS))
        #     f.writelines('\n') 

        random.seed(gen)

        steps = 0
        while (dictEtatS != DICT_ETAT_FINAL) and (steps < plafond) :
                #possible actions and next states
                # Coal = Actions5.coalID(dictEtatS)
                # Mut = Actions5.Mutation(dictEtatS, L)
                # CoalDif = Actions5.coalDif(dictEtatS)
                # Rec = Actions5.recombin(dictEtatS)
                # etatSuivantS = Coal[0] + Mut[0] + CoalDif[0] + Rec[0] #etats suivants possibles
                # actionsPoss = Coal[1] + Mut[1] + CoalDif[1] + Rec[1] #actions menant aux etats suivants

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
                #print('valeur')
                #print(v[indexSPrime])
                #print(etatSuivantS[indexSPrime])
                        
            #s' becomes s
            dictEtatS = etatSuivantS[indexSPrime]
            etatS = Codages.Blocs3Plus(dictEtatS, L-2)
            #actionChoisie = actionsPoss[indexSPrime]

            #On inscrit dans un fichier la genealogie
            # with open(nomFichier2, 'a') as f:
            #     f.writelines(str(dictEtatS))
            #     f.writelines('\n')
                #f.writelines(str(actionChoisie))
                #f.writelines('\n')

            #print(steps)
            steps = steps + 1
            
        with open(nomFichier3, 'a') as f2:
            f2.writelines('\n')
            f2.writelines(str(steps) + "\t" + str(n) + "\t" + str(gen) + "\t" + str(new)+ "\t" + 'RL')

        print(gen)
        print(steps)


