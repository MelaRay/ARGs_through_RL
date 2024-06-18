import itertools
import random
import Actions2 
import MyModelNN as MyNN
import torch
import Codages
import json
import EtatInitial
import time

#Monte Carlo algorithm with neural network
#Feature vector : blocks of 3 markers with overlaps

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


L = 10 #number of markers
alpha = 1/100000 #learning rate
epsilon = 0.1 #exploration rate

#Final state
DICT_ETAT_FINAL = {(0,0,0,0,0,0,0,0,0,0) : 1}

nbEpisodes = 100_000 #nombre de genealogies a generer
nomFichier = 'textFiles/Longueur_14agents.txt'
nomFichierTemps = 'textFiles/Temps_14agents.txt'

#File to stock the length of the genealogies
with open(nomFichier, 'a') as f:
    f.writelines('Genealogies' + "\t" + 'Longueur' + "\t" + 'MSE_one'+ "\t"+ 'Exploration'+ "\t"+ 'Seed'+ "\t")

#File to keep learning time
with open(nomFichierTemps, 'a') as f:
    f.writelines('Genealogies' + "\t" + 'Temps')

Seeds =[123, 125, 126, 124, 127, 128, 131, 132, 805, 804, 799, 795, 796, 797]
nbrAgents = len(Seeds)
m = 5

for no_mod in range(nbrAgents):

    #First samples for training
    random.seed(1234 + no_mod)
    index = random.sample(indexTrain, k = sizeTrain) 

    seed = Seeds[no_mod]
    #Model to train
    torch.manual_seed(seed)
    model = MyNN.MyModel()
    optimizer = torch.optim.SGD(model.parameters(), lr= alpha)
    loss_fn = torch.nn.MSELoss()
    
    #we run e episodes
    e = 1
    onChange = int(sizeTrain/m)
    TimeBegin = time.time()
    while (e <= nbEpisodes): 
        #Return and values of the episode
        G = torch.tensor([])
        genealogy = torch.tensor([])

        random.seed(e) 
        #Initial state drawn from training set
        dictEtatS = EtatInitial.S0(POP, e, m, sizeTrain, index)
          
        etatS = Codages.Blocs3Plus(dictEtatS, L-2)

        #print(dictEtatS)
        #print(len(dictEtatS))
        
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

            #print(dictEtatS)
            #s' devient s
            dictEtatS = etatSuivantS[indexSPrime]
            etatS = Codages.Blocs3Plus(dictEtatS, L-2)
        
            #print(steps)
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
            f.writelines(str(e) + "\t" + str(steps) + "\t" + str(loss.item())+ "\t" + str(explo/steps)+ "\t" + str(seed))

        
        if(e == onChange):
            #Changing samples
            random.seed(e + no_mod)
            index = random.sample(indexTrain, k = sizeTrain)
            onChange = onChange + int(sizeTrain/m)

            #Saving model
            nomModele = 'model_m' + str(m) + 'ALL_new_' + str(e) + '_' + str(seed) + '.pth'
            torch.save(model.state_dict(), nomModele)

            #Saving time
            TimeEnd = time.time()
            temps = TimeEnd - TimeBegin
            with open(nomFichierTemps, 'a') as f:
                f.writelines('\n')
                f.writelines(str(e) + "\t" + str(temps))

        e = e + 1

    #Saving final model
    #torch.save(model.state_dict(), nomModeleFinal)
















