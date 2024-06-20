import random

#Module with functions to identify possible actions and do recombinations as defined by ARG4WG
#SNPs are coded as 0, 1, 9

#MRCA
ANC_COMMUN = (0,0,0,0,0,0,0,0,0,0)

#Function to identify coalescence between identical sequences
#parameters: dictEtatS, dictionnary with type of sequences in state s as key and number of sequences of key type as value
#return: list of dictionnaries of possible next states
def coalID(dictEtatS):
    etatSuivant = []
    A_t = []
    for seq1 in dictEtatS: #for each sequence in state s
        if dictEtatS[seq1] > 1: #if more than 2 sequences of the same type
            dictEtatSPrime = dictEtatS.copy()
            dictEtatSPrime[seq1] = dictEtatSPrime[seq1] - 1 #new state after coalescence
            etatSuivant.append(dictEtatSPrime) #update possible next states
            A_t.append([1, seq1]) 
           
    return [etatSuivant, A_t]
 
#Function to identify possible mutations
#parameters: dictEtatS, dictionnary with type of sequences in state s as key and number of sequences of key type as value
#             L, numbers of SNPs per sequence
#return: list of dictionnaries of possible next states
def Mutation(dictEtatS, L):
    etatSuivant = []
    A_t = []
    for i in range(L):
        somme = 0
        for seq1 in dictEtatS: #for each sequence in state s
            if(seq1[i] == 1): #if there is a mutation on the ith marker
                somme = somme + dictEtatS[seq1] #number of sequences with a mutation on the ith marker
        
        if somme == 1:
            seqAMuter = [seq for seq in dictEtatS if seq[i] == 1] #sequence with mutation
            dictEtatSPrime = dictEtatS.copy()
            dictEtatSPrime.pop(seqAMuter[0]) #new state without the sequence with mutation
            seqMutee = list(seqAMuter[0])
            seqMutee[i] = 0 #new sequence without mutation
            seqMutee = tuple(seqMutee)
            #new state with sequence without mutation
            if(seqMutee in dictEtatSPrime):
                dictEtatSPrime[seqMutee] = dictEtatSPrime[seqMutee] + 1
            else:
                dictEtatSPrime[seqMutee] = 1

            etatSuivant.append(dictEtatSPrime) #update possible next states
            A_t.append([2, seqAMuter[0], seqMutee])
   
    return [etatSuivant, A_t]
 
#Function to identify coalescence between sequences of different types
#parameters: dictEtatS, dictionnary with type of sequences in state s as key and number of sequences of key type as value
#return: list of dictionnaries of possible next states
def coalDif(dictEtatS):
    etatSuivant = []
    A_t = []
    dict2 = dictEtatS.copy()
    for seq1 in dictEtatS: #for each sequence in state s
        dict2.pop(seq1)
        for seq2 in dict2: #comparison with other sequences in state s
            #sequences i and j to compare
            seqI = list(seq1)
            seqJ = list(seq2)
            indexDiff = []
            #different markers between seq i and seq j
            for m in range(len(seqI)):
                if seqI[m] != seqJ[m]:
                    indexDiff.append(m)
               
            # where the markers are different
            # check if markers are 1 and 0 or 0 and 1
            onArrete = False
            for x in indexDiff:
                onArrete = (seqI[x] == 1 and seqJ[x] == 0) or (seqI[x] == 0 and seqJ[x] == 1)
                if onArrete:
                    break
               
            #if coalescence possible
            if not onArrete:
                seqK = seqI[:] #copy sequence i
                indexNonAncI = [x for x in range(len(seqI)) if seqI[x] == 9] #non ancestral markers in seq i
                for i in indexNonAncI: #replace non ancestral markers of seq i by markers of seq j
                    seqK[i] = seqJ[i]

                #new state after coalescence
                dictEtatSPrime = dictEtatS.copy()
                seqI = tuple(seqI)
                seqJ = tuple(seqJ)
                seqK = tuple(seqK)
                dictEtatSPrime[seqI] = dictEtatSPrime[seqI] - 1 #new state without seq i
                dictEtatSPrime[seqJ] = dictEtatSPrime[seqJ] - 1 #new state without seq j
                #new state with seq k
                if(seqK in dictEtatSPrime):
                    dictEtatSPrime[seqK] = dictEtatSPrime[seqK] + 1
                else:
                    dictEtatSPrime[seqK] = 1
                
                if dictEtatSPrime[seqI] == 0:
                    dictEtatSPrime.pop(seqI)
                if dictEtatSPrime[seqJ] == 0:
                    dictEtatSPrime.pop(seqJ)

                etatSuivant.append(dictEtatSPrime) #update possible next states
                A_t.append([3, seqI, seqJ, seqK])
 
    return [etatSuivant, A_t]
 
#Function to do a recombinations according to ARG4WG
#parameters: dictEtatS, dictionnary with type of sequences in state s as key and number of sequences of key type as value
#             L, number of SNPs per sequence
#return: next state after recombination
def recombin(dictEtatS, L):
    etatSuivant = []
    A_t = []
    dict2 = dictEtatS.copy()
    longSharedEnd = 0
    for seq1 in dictEtatS: #for each sequence in state s
        dict2.pop(seq1)
        for seq2 in dict2: #comparison with other sequences in state s
            #sequences i et j to compare
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

            #pair of sequences with longest shared end
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
        #number of non ancestral markers in shared end
        for b in range(actionChoisie[3]):
            MNAseqI = MNAseqI + seqI[b] == 9
            MNAseqJ = MNAseqJ + seqI[b] == 9
        
        if (MNAseqI < MNAseqJ):
            seqI = actionChoisie[0] #sequence to recombine
            seqJ = actionChoisie[1] #sequence to coalesce
        else:
            seqI = actionChoisie[1] #sequence to recombine
            seqJ = actionChoisie[0] #sequence to coalesce

        seqK1 = seqI[:] #sequence after recombinaison
        seqK2 = seqJ[:] #sequence after coalescence
        indexNonAncI = [x for x in range(actionChoisie[3]) if seqJ[x] == 9] #non ancestral markers in seq j
        for i in indexNonAncI: #replace non ancestral markers in seq j by markers of seq i
            seqK2[i] = seqI[i]
        for b in range(actionChoisie[3]):
            seqK1[b] = 9
    else:
        seqI = actionChoisie[0]
        seqJ = actionChoisie[1]
        MNAseqI = 0
        MNAseqJ = 0
        #number of non ancestral markers in shared end
        for b in range(actionChoisie[3]):
            MNAseqI = MNAseqI + seqI[L - b - 1] == 9
            MNAseqJ = MNAseqJ + seqI[L - b - 1] == 9
        
        if (MNAseqI > MNAseqJ):
            seqI = actionChoisie[0] #sequence to recombine
            seqJ = actionChoisie[1] #sequence to coalesce
        else:
            seqI = actionChoisie[1] #sequence to recombine
            seqJ = actionChoisie[0] #sequence to coalesce

        seqK1 = seqI[:] #sequence after recombinaison
        seqK2 = seqJ[:] #sequence after coalescence
        indexNonAncI = [x for x in range(actionChoisie[3]) if seqJ[L - x - 1] == 9] #non ancestral markers in seq j
        for i in indexNonAncI: #replace non ancestral markers in seq j by markers of seq i
            seqK2[L - i - 1] = seqI[L - i -1]
        for b in range(actionChoisie[3]):
            seqK1[L - b - 1] = 9
            
    dictEtatSPrime = dictEtatS.copy()
    seqI = tuple(seqI)
    seqJ = tuple(seqJ)
    seqK1 = tuple(seqK1)
    seqK2 = tuple(seqK2)
    dictEtatSPrime[seqI] = dictEtatSPrime[seqI] - 1 #new state without seq i
    dictEtatSPrime[seqJ] = dictEtatSPrime[seqJ] - 1 #new state without seq j
    #new state with seq k1
    if(seqK1 in dictEtatSPrime):
        dictEtatSPrime[seqK1] = dictEtatSPrime[seqK1] + 1
    else:
        dictEtatSPrime[seqK1] = 1

    #new state with seq k2
    if(seqK2 in dictEtatSPrime):
        dictEtatSPrime[seqK2] = dictEtatSPrime[seqK2] + 1
    else:
        dictEtatSPrime[seqK2] = 1

    if dictEtatSPrime[seqI] == 0:
        dictEtatSPrime.pop(seqI)
    if dictEtatSPrime[seqJ] == 0:
        dictEtatSPrime.pop(seqJ)

    return dictEtatSPrime