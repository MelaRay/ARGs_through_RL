#Fonctions permettant d'identifier les actions possibles
#Avec les dictionnaires des états
#Codage des marqueurs : 0, 1 et M_NA pour les marqueurs non ancestraux

#Codage des marqueurs non-ancestraux
M_NA = 9

#Codage des mutation
M_MUT = 1

#Ancêtre commun
ANC_COMMUN = (0,0,0,0,0,0,0,0,0,0)

#Fonction pour identifier si coalescence identique possible
#parametres : dictEtatS, dictionnaire avec sequences etat S comme clé et nombre de cette séquence comme valeur
#retourne : liste de dictionnaires des etats suivants possibles
def coalID(dictEtatS):
    etatSuivant = []
    for seq1 in dictEtatS: #pour chaque sequence a etat s
        if dictEtatS[seq1] > 1: #on verifie si plus de 2 sequences du meme type
            dictEtatSPrime = dictEtatS.copy()
            dictEtatSPrime[seq1] = dictEtatSPrime[seq1] - 1 #cree nouvel etat
            etatSuivant.append(dictEtatSPrime) #mise a jour etats suivants possibles
           
    return etatSuivant
 
#Fonction pour identifier si mutation possible
#parametres : dictEtatS, dictionnaire avec sequences etat S comme clé et nombre de cette séquence comme valeur
#             L, nombre de marqueurs par sequence
#retourne : liste de dictionnaires des etats suivants possibles
def Mutation(dictEtatS, L):
    etatSuivant = []
    for i in range(L):
        somme = 0
        for seq1 in dictEtatS: #Pour chaque sequences etat S
            if(seq1[i] == 1): #on verifie s'il y a une mutation au marqueurs i
                somme = somme + dictEtatS[seq1] #nombre de sequences avec une mutation au marqueur i
        
        if somme == 1:
            seqAMuter = [seq for seq in dictEtatS if seq[i] == 1] #sequence a muter
            dictEtatSPrime = dictEtatS.copy()
            dictEtatSPrime.pop(seqAMuter[0]) #nouvel etat sans sequences a muter
            seqMutee = list(seqAMuter[0])
            seqMutee[i] = 0 #sequence une fois mutation enlevee
            seqMutee = tuple(seqMutee)
            #nouvel etat avec sequence sans mutation
            if(seqMutee in dictEtatSPrime):
                dictEtatSPrime[seqMutee] = dictEtatSPrime[seqMutee] + 1
            else:
                dictEtatSPrime[seqMutee] = 1

            etatSuivant.append(dictEtatSPrime) #mise a jour etats suivants possibles
   
    return etatSuivant
 
#Fonction pour identifier coalescence de type different
#parametres : dictEtatS, dictionnaire avec sequences etat S comme clé et nombre de cette séquence comme valeur
#retourne : liste de dictionnaires des etats suivants possibles
def coalDif(dictEtatS):
    etatSuivant = []
    dict2 = dictEtatS.copy()
    for seq1 in dictEtatS: #Pour chaque sequence etat S
        dict2.pop(seq1)
        for seq2 in dict2: #On compare avec les autres sequences etat S
            #sequences i et j a comparer
            seqI = list(seq1)
            seqJ = list(seq2)
            indexDiff = []
            #identifie marqueurs differents entre i et j
            for m in range(len(seqI)):
                if seqI[m] != seqJ[m]:
                    indexDiff.append(m)
               
            # A chaque position ou les marqueurs sont differents
            # On verifie si les marqueurs sont des 1 et 0 ou 0 et 1
            onArrete = False
            for x in indexDiff:
                onArrete = (seqI[x] == 1 and seqJ[x] == 0) or (seqI[x] == 0 and seqJ[x] == 1)
                if onArrete:
                    break
               
            #Si coalescence differente possible
            if not onArrete:
                seqK = seqI[:] #copie de la sequence I
                indexNonAncI = [x for x in range(len(seqI)) if seqI[x] == M_NA] #identifie marqueurs non ancestraux de I
                for i in indexNonAncI: #remplace les marqueurs non ancestraux de i par marqueurs de j
                    seqK[i] = seqJ[i]

                #nouvel etat apres coalescence
                dictEtatSPrime = dictEtatS.copy()
                seqI = tuple(seqI)
                seqJ = tuple(seqJ)
                seqK = tuple(seqK)
                dictEtatSPrime[seqI] = dictEtatSPrime[seqI] - 1 #nouvel etat sans sequence i
                dictEtatSPrime[seqJ] = dictEtatSPrime[seqJ] - 1 #nouvel etat sans sequence j
                #nouvel etat avec sequence k
                if(seqK in dictEtatSPrime):
                    dictEtatSPrime[seqK] = dictEtatSPrime[seqK] + 1
                else:
                    dictEtatSPrime[seqK] = 1
                
                if dictEtatSPrime[seqI] == 0:
                    dictEtatSPrime.pop(seqI)
                if dictEtatSPrime[seqJ] == 0:
                    dictEtatSPrime.pop(seqJ)

                etatSuivant.append(dictEtatSPrime) #mise a jour etats suivants possibles
 
    return etatSuivant
 
#Fonction pour identifier les recomdinaisons possibles
#parametres : dictEtatS, dictionnaire avec sequences etat S comme clé et nombre de cette séquence comme valeur
#retourne : liste de dictionnaires des etats suivants possibles
def recombin(dictEtatS):
    etatSuivant = []
    for seq in dictEtatS: #pour chaque sequence etat s
        indexAnc = [x for x in range(len(seq)) if seq[x] != M_NA] #identifie les marqueurs ancestraux
        #indexMut = [x for x in range(len(seq)) if seq[x] == M_MUT] #identifie s'il y a une mutation
        if (len(indexAnc) > 1 and seq != ANC_COMMUN): #si plus qu'un marqeur ancestral et seq. diff. de (0,...,0), recombinaison possible
        #if (len(indexAnc) > 1 and len(indexMut) > 1): #si plus qu'un marqeur ancestral et au moins une mutation, recombinaison possible
            indexAnc.pop(len(indexAnc)-1) #enleve l'indice du dernier marqueur ancestral
            for m in indexAnc:
                seqJ = list(seq) #copie seq qui recombine pour créer nouvelle sequence j
                seqK = list(seq) #copie seq qui recombine pour créer nouvelle sequence k
                for i in range(m+1):
                    seqJ[i] = M_NA
 
                for j in range(m+1, len(seqK), 1):
                    seqK[j] = M_NA

                #nouvel etat apres recombinaison
                dictEtatSPrime = dictEtatS.copy()
                seqI = tuple(seq)
                seqJ = tuple(seqJ)
                seqK = tuple(seqK)
                dictEtatSPrime[seqI] = dictEtatSPrime[seqI] - 1 #nouvel etat sans sequences i
                #nouvel etat avec sequences j
                if(seqJ in dictEtatSPrime):
                    dictEtatSPrime[seqJ] = dictEtatSPrime[seqJ] + 1
                else:
                    dictEtatSPrime[seqJ] = 1
                
                #nouvel etat avec sequences k
                if(seqK in dictEtatSPrime):
                    dictEtatSPrime[seqK] = dictEtatSPrime[seqK] + 1 
                else:
                    dictEtatSPrime[seqK] = 1 

                if dictEtatSPrime[seqI] == 0:
                    dictEtatSPrime.pop(seqI)

                etatSuivant.append(dictEtatSPrime) #mise a jour etats suivants possibles
 
    return etatSuivant