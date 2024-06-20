#Module with functions to identify possible actions
#Each state is represented using a dictionnary
#SNPs are coded : 0, 1 et M_NA for non ancestral material

#Non ancestral SNPs
M_NA = 9

#SNPs for mutation
M_MUT = 1

#MRCA
ANC_COMMUN = (0,0,0,0,0,0,0,0,0,0)

#Function to identify coalescence between identical sequences
#parameters: dictEtatS, dictionnary with type of sequences in state s as key and number of sequences of key type as value
#return: list of dictionnaries of possible next states
def coalID(dictEtatS):
    etatSuivant = []
    for seq1 in dictEtatS: #for each sequence in state s
        if dictEtatS[seq1] > 1: #if more than 2 sequences of the same type
            dictEtatSPrime = dictEtatS.copy()
            dictEtatSPrime[seq1] = dictEtatSPrime[seq1] - 1 #new state after coalescence
            etatSuivant.append(dictEtatSPrime) #update possible next states
           
    return etatSuivant
 
#Function to identify possible mutations
#parameters: dictEtatS, dictionnary with type of sequences in state s as key and number of sequences of key type as value
#             L, numbers of SNPs per sequence
#return: list of dictionnaries of possible next states
def Mutation(dictEtatS, L):
    etatSuivant = []
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
   
    return etatSuivant
 
#Function to identify coalescence between sequences of different types
#parameters: dictEtatS, dictionnary with type of sequences in state s as key and number of sequences of key type as value
#return: list of dictionnaries of possible next states
def coalDif(dictEtatS):
    etatSuivant = []
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
                indexNonAncI = [x for x in range(len(seqI)) if seqI[x] == M_NA] #non ancestral markers in seq i
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
 
    return etatSuivant
 
#Function to identify possible recombinations
#parameters: dictEtatS, dictionnary with type of sequences in state s as key and number of sequences of key type as value
#return: list of dictionnaries of possible next states
def recombin(dictEtatS):
    etatSuivant = []
    for seq in dictEtatS: #for each sequence in state s
        indexAnc = [x for x in range(len(seq)) if seq[x] != M_NA] #ancestral markers
        if (len(indexAnc) > 1 and seq != ANC_COMMUN): #recombination possible if more than one ancestral marker and seq not MRCA
            indexAnc.pop(len(indexAnc)-1) #remove index last ancestral marker
            for m in indexAnc:
                seqJ = list(seq) #copy seq to recombine to create new seq j
                seqK = list(seq) #copy seq to recombine to create new seq k
                for i in range(m+1):
                    seqJ[i] = M_NA
 
                for j in range(m+1, len(seqK), 1):
                    seqK[j] = M_NA

                #new state after recombination
                dictEtatSPrime = dictEtatS.copy()
                seqI = tuple(seq)
                seqJ = tuple(seqJ)
                seqK = tuple(seqK)
                dictEtatSPrime[seqI] = dictEtatSPrime[seqI] - 1 #new state without seq i
                #new state with seq j
                if(seqJ in dictEtatSPrime):
                    dictEtatSPrime[seqJ] = dictEtatSPrime[seqJ] + 1
                else:
                    dictEtatSPrime[seqJ] = 1
                
                #new state with seq k
                if(seqK in dictEtatSPrime):
                    dictEtatSPrime[seqK] = dictEtatSPrime[seqK] + 1 
                else:
                    dictEtatSPrime[seqK] = 1 

                if dictEtatSPrime[seqI] == 0:
                    dictEtatSPrime.pop(seqI)

                etatSuivant.append(dictEtatSPrime) #update possible next states
 
    return etatSuivant