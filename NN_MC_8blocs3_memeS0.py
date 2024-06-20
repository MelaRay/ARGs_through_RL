import itertools
import random
import Actions2 
import MyModelNN as MyNN
import torch
import Codages
import EtatInitial
import time
import json

#Module for approximation method: same initial state
#RL Monte Carlo algorithm with neural network
#Feature vector : blocks of 3 markers with overlaps

L = 10 #number of markers
alpha = 1/10_000 #learning rate
epsilon = 0.1 #exploration rate

#Final state
DICT_ETAT_FINAL = {(0, 0, 0, 0, 0, 0, 0, 0, 0, 0) : 1}

nbEpisodes = 10_000 #number of episodes per sample
nomFichier = 'textFiles/Longueur_memeS0_60ech_N0_v2.txt'
nomFichierTemps = 'textFiles/Temps_memeS0_60ech_N0_v2.txt'

with open("pop2", "r") as fp:
     POP = json.load(fp)

#File to stock the length of the genealogies
with open(nomFichier, 'a') as f:
    f.writelines('Genealogies' + "\t" + 'Longueur' + "\t" + 'MSE_one'+ "\t"+ 'Exploration'+ "\t"+ 'Echantillon'+ "\t" + 'Taille')

#File to keep learning time
with open(nomFichierTemps, 'a') as f:
    f.writelines('Genealogies' + "\t" + 'Temps')

nbrEch = 60 #number of samples
indexSize = 0
sampleSizes = [40, 60, 100]

indexEch = 0
n = 0

for noEch in range(nbrEch):

    #Model to train
    torch.manual_seed(124)
    model = MyNN.MyModel()
    optimizer = torch.optim.SGD(model.parameters(), lr= alpha)
    loss_fn = torch.nn.MSELoss()
    indexEch = indexEch + n

    if noEch % 20 == 0:
        n = sampleSizes[indexSize]
        indexSize = indexSize + 1
    
    #we run e episodes
    e = 1
    TimeBegin = time.time()
    while (e <= nbEpisodes): 
        #Return and values of the episode
        G = torch.tensor([])
        genealogy = torch.tensor([])

        #Same initial state 
        dictEtatS = EtatInitial.S0_x(POP, indexEch, n, range(len(POP)))

        etatS = Codages.Blocs3Plus(dictEtatS, L-2)

        random.seed(e) 
        
        steps = 1
        explo = 0 #exploration rate of the episode
        while dictEtatS != DICT_ETAT_FINAL:
            #possible actions and next states
            etatSuivantS = Actions2.coalID(dictEtatS)
            etatSuivantS = etatSuivantS  + Actions2.Mutation(dictEtatS, L)
            etatSuivantS = etatSuivantS  + Actions2.coalDif(dictEtatS)
            etatSuivantS = etatSuivantS  + Actions2.recombin(dictEtatS)

            #We choose the next state epsilon-greedy
            u = random.uniform(0,1)
            if u > epsilon:
                #estimated value of each possible next state
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
                    #we choose the next state (highest estimated value)    
                    allIndexSPrime = [x for x in range(len(v)) if v[x] == max(v)]
                    indexSPrime = random.choice(allIndexSPrime)
                
                vHatSPrime = v[indexSPrime]
            else:
                #we choose the next state randomly
                explo = explo + 1
                indexSPrime = random.randint(0, len(etatSuivantS) - 1)
                etat = etatSuivantS[indexSPrime]
                if etat == DICT_ETAT_FINAL:
                    vHatSPrime = 0
                else:
                    input = Codages.Blocs3Plus(etat, L-2)
                    vHatSPrime = model(torch.tensor([input], dtype = torch.float32))

            #Reward and return
            G = G - 1   
            R = torch.tensor([-1])
            G = torch.cat((G, R), 0)
            
            etat = torch.tensor([etatS], dtype = torch.float32)
            genealogy = torch.cat((genealogy, etat), 0)

            #s' becomes s
            dictEtatS = etatSuivantS[indexSPrime]
            etatS = Codages.Blocs3Plus(dictEtatS, L-2)
        
            steps = steps + 1

        print(e)
        print(steps)

        #Update weight vector w
        pred = model(genealogy)
        loss = loss_fn(pred, G.unsqueeze(1))
        print(loss)
        loss.backward()
        optimizer.step()
        optimizer.zero_grad()

        pred = torch.tensor([])

        #Length of the genealogy
        with open(nomFichier, 'a') as f:
            f.writelines('\n')
            f.writelines(str(e) + "\t" + str(steps) + "\t" + str(loss.item())+ "\t" + str(explo/steps)+ "\t" + str(noEch) + "\t" + str(n))

        e = e + 1

    #Saving final model
    nomModele = 'model_echant' + str(noEch) + '_new.pth'
    torch.save(model.state_dict(), nomModele)

    TimeEnd = time.time()
    temps = TimeEnd - TimeBegin
    with open(nomFichierTemps, 'a') as f:
        f.writelines('\n')
        f.writelines(str(e) + "\t" + str(temps))
















