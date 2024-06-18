import random

#Fonctions permettant d'identifier les actions possibles
#Avec le codage des marqueurs par 0, 1, 9
#Les fonctions retournent une liste avec : liste etats suivants possibles, 
#liste des actions menant a ces etats 

#Ancêtre commun
ANC_COMMUN = (0,0,0,0,0,0,0,0,0,0)

#Fonction pour identifier si coalescence identique possible
#parametres : dictEtatS, dictionnaire avec sequences etat S comme clé et nombre de cette séquence comme valeur
#retourne : liste de dictionnaires des etats suivants possibles
def coalID(dictEtatS):
    etatSuivant = []
    A_t = []
    for seq1 in dictEtatS: #pour chaque sequence a etat s
        if dictEtatS[seq1] > 1: #on verifie si plus de 2 sequences du meme type
            dictEtatSPrime = dictEtatS.copy()
            dictEtatSPrime[seq1] = dictEtatSPrime[seq1] - 1 #cree nouvel etat
            etatSuivant.append(dictEtatSPrime) #mise a jour etats suivants possibles
            A_t.append([1, seq1]) 
           
    return [etatSuivant, A_t]
 
#Fonction pour identifier si mutation possible
#parametres : dictEtatS, dictionnaire avec sequences etat S comme clé et nombre de cette séquence comme valeur
#             L, nombre de marqueurs par sequence
#retourne : liste de dictionnaires des etats suivants possibles
def Mutation(dictEtatS, L):
    etatSuivant = []
    A_t = []
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
            A_t.append([2, seqAMuter[0], seqMutee])
   
    return [etatSuivant, A_t]
 
#Fonction pour identifier coalescence de type different
#parametres : dictEtatS, dictionnaire avec sequences etat S comme clé et nombre de cette séquence comme valeur
#retourne : liste de dictionnaires des etats suivants possibles
def coalDif(dictEtatS):
    etatSuivant = []
    A_t = []
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
            # On verifie si les marqueurs sont des -1 et 1 ou 1 et -1
            onArrete = False
            for x in indexDiff:
                onArrete = (seqI[x] == 1 and seqJ[x] == 0) or (seqI[x] == 0 and seqJ[x] == 1)
                if onArrete:
                    break
               
            #Si coalescence differente possible
            if not onArrete:
                seqK = seqI[:] #copie de la sequence I
                indexNonAncI = [x for x in range(len(seqI)) if seqI[x] == 9] #identifie marqueurs non ancestraux de I
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
                A_t.append([3, seqI, seqJ, seqK])
 
    return [etatSuivant, A_t]
 
#Fonction pour identifier les recombinaisons possibles
#Ne permet pas la recombinaison de la séquence avec seulement des 0
#parametres : dictEtatS, dictionnaire avec sequences etat S comme clé et nombre de cette séquence comme valeur
#retourne : liste de dictionnaires des etats suivants possibles
def recombin(dictEtatS, L):
    etatSuivant = []
    A_t = []
    dict2 = dictEtatS.copy()
    longSharedEnd = 0
    for seq1 in dictEtatS: #Pour chaque sequence etat S
        dict2.pop(seq1)
        for seq2 in dict2: #On compare avec les autres sequences etat S
            #sequences i et j a comparer
            seqI = list(seq1)
            seqJ = list(seq2)
            onContinue = True
            g = 0
            marNAg = 0 #non ancestral markers from the left
            while onContinue and (g < L):
                onContinue = (seqI[g] == seqJ[g] or seqI[g] == 9 or 9 == seqJ[g])
                marNAg = marNAg + (seqI[g] == seqJ[g] and seqI[g] != 9)
                g = g + 1

            onContinue = True
            r = 0
            marNAr = 0 #non ancestral markers from the right
            while onContinue and (r < L):
                m = L - r - 1
                onContinue = (seqI[m] == seqJ[m] or seqI[m] == 9 or 9 == seqJ[m])
                marNAr = marNAr + (seqI[m] == seqJ[m] and seqI[m] != 9)
                r = r + 1

            if marNAg == 0:
                g = 0
            if marNAr == 0:
                r = 0

            if (g != 0 or r != 0):
                if(g > r):
                    if(g == longSharedEnd):
                        A_t.append([seqI, seqJ, 'G', g-1])
                    elif (g > longSharedEnd):
                        A_t = [[seqI, seqJ, 'G', g-1]]
                        longSharedEnd = g
                elif(g < r):
                    if(r == longSharedEnd):
                        A_t.append([seqI, seqJ, 'R', r-1])
                    elif (r > longSharedEnd):
                        A_t = [[seqI, seqJ, 'R', r-1]]
                        longSharedEnd = r
                else:
                    if(r == longSharedEnd):
                        A_t.append([seqI, seqJ, 'R', r-1])
                        A_t.append([seqI, seqJ, 'G', g-1])
                    elif (r > longSharedEnd):
                        A_t = [[seqI, seqJ, 'R', r]]
                        A_t.append([seqI, seqJ, 'G', g-1])
                        longSharedEnd = r

    indexRecombin = random.randint(0, len(A_t) - 1)
    actionChoisie = A_t[indexRecombin]

    if(actionChoisie[2] == 'G'):
        seqI = actionChoisie[0]
        seqJ = actionChoisie[1]
        MNAseqI = 0
        MNAseqJ = 0
        #On compte nbr marqueurs non ancestraux dans extremite commune
        for b in range(actionChoisie[3]):
            MNAseqI = MNAseqI + seqI[b] == 9
            MNAseqJ = MNAseqJ + seqI[b] == 9
        
        if (MNAseqI < MNAseqJ):
            seqI = actionChoisie[0] #sequence qui recombine
            seqJ = actionChoisie[1] #sequence qui coalesce
        else:
            seqI = actionChoisie[1] #sequence qui recombine
            seqJ = actionChoisie[0] #sequence qui coalesce

        seqK1 = seqI[:] #sequence issue recombinaison
        seqK2 = seqJ[:] #sequence apres coalescence
        indexNonAncI = [x for x in range(actionChoisie[3]) if seqJ[x] == 9] #identifie marqueurs non ancestraux de J
        for i in indexNonAncI: #remplace les marqueurs non ancestraux de i par marqueurs de j
            seqK2[i] = seqI[i]
        for b in range(actionChoisie[3]):
            seqK1[b] = 9
    else:
        seqI = actionChoisie[0]
        seqJ = actionChoisie[1]
        MNAseqI = 0
        MNAseqJ = 0
        #On compte nbr marqueurs non ancestraux dans extremite commune
        for b in range(actionChoisie[3]):
            MNAseqI = MNAseqI + seqI[L - b - 1] == 9
            MNAseqJ = MNAseqJ + seqI[L - b - 1] == 9
        
        if (MNAseqI > MNAseqJ):
            seqI = actionChoisie[0] #sequence qui recombine
            seqJ = actionChoisie[1] #sequence qui coalesce
        else:
            seqI = actionChoisie[1] #sequence qui recombine
            seqJ = actionChoisie[0] #sequence qui coalesce

        seqK1 = seqI[:] #sequence issue recombinaison
        seqK2 = seqJ[:] #sequence apres coalescence
        indexNonAncI = [x for x in range(actionChoisie[3]) if seqJ[L - x - 1] == 9] #identifie marqueurs non ancestraux de J
        for i in indexNonAncI: #remplace les marqueurs non ancestraux de i par marqueurs de j
            seqK2[L - i - 1] = seqI[L - i -1]
        for b in range(actionChoisie[3]):
            seqK1[L - b - 1] = 9
            
    dictEtatSPrime = dictEtatS.copy()
    seqI = tuple(seqI)
    seqJ = tuple(seqJ)
    seqK1 = tuple(seqK1)
    seqK2 = tuple(seqK2)
    dictEtatSPrime[seqI] = dictEtatSPrime[seqI] - 1 #nouvel etat sans sequences i
    dictEtatSPrime[seqJ] = dictEtatSPrime[seqJ] - 1 #nouvel etat sans sequences j
    #nouvel etat avec sequences k1
    if(seqK1 in dictEtatSPrime):
        dictEtatSPrime[seqK1] = dictEtatSPrime[seqK1] + 1
    else:
        dictEtatSPrime[seqK1] = 1

    #nouvel etat avec sequences k2
    if(seqK2 in dictEtatSPrime):
        dictEtatSPrime[seqK2] = dictEtatSPrime[seqK2] + 1
    else:
        dictEtatSPrime[seqK2] = 1

    if dictEtatSPrime[seqI] == 0:
        dictEtatSPrime.pop(seqI)
    if dictEtatSPrime[seqJ] == 0:
        dictEtatSPrime.pop(seqJ)

    return dictEtatSPrime