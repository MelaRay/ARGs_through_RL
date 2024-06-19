import itertools
import torch
import math

#Module with functions to code feature vector
#by blocks of markers, with a matrix of haplotypes 

#blocks of 2 and 3 markers
ALL_marqueurs = [0,1,9]
BLOCS_2 = list(itertools.product(ALL_marqueurs, repeat = 2))
BLOCS_3 = list(itertools.product(ALL_marqueurs, repeat = 3))
BLOCS_4 = list(itertools.product(ALL_marqueurs, repeat = 4))
BLOCS_5 = list(itertools.product(ALL_marqueurs, repeat = 5))
BLOCS_2_19= list(itertools.product([0,1], repeat = 2))

#Codage blocs de 1
#Parametres : dictEtatS, dictionnaire des sequences a l'etat s,
#           k, nombre de blocs

def Blocs1(dictEtatS, k):
    d = len(ALL_marqueurs) #nbr total blocs differents
    etatS = [0] * k * d

    for seq1 in dictEtatS: #pour chaque sequence etat s
        for j in range(d): #pour chaque bloc j possible
            i = 0
            #on verifie si bloc position p de seq1 est egal au bloc j
            for p in range(k):
                if (seq1[i] == ALL_marqueurs[j]):
                    etatS[j*k + p] = etatS[j*k + p] + dictEtatS[seq1]

                i = i + 1

    return etatS

#Codage blocs de 2 SANS chevauchements
#Parametres : dictEtatS, dictionnaire des sequences a l'etat s,
#           k, nombre de blocs

def Blocs2(dictEtatS, k):
    d = len(BLOCS_2) #nbr total blocs differents
    etatS = [0] * k * d

    for seq1 in dictEtatS: #pour chaque sequence etat s
        for j in range(d): #pour chaque bloc j possible
            i = 0
            #on verifie si bloc position p de seq1 est egal au bloc j
            for p in range(k):
                if (seq1[i:(i+2)] == BLOCS_2[j]):
                    etatS[j*k + p] = etatS[j*k + p] + dictEtatS[seq1]

                i = i + 2

    return etatS

#Codage blocs de 2 AVEC chevauchements
#Parametres : dictionnaire des sequences a l'etat s,
#           k, nombre de blocs

def Blocs2Plus(dictEtatS, k):
    d = len(BLOCS_2) #nbr total blocs differents
    etatS = [0] * k * d

    for seq1 in dictEtatS: #pour chaque sequence etat s
        for j in range(d): #pour chaque bloc j possible
            #on verifie si bloc position p de seq1 est egal au bloc j
            for p in range(k):
                if (seq1[p:(p+2)] == BLOCS_2[j]):
                    etatS[j*k + p] = etatS[j*k + p] + dictEtatS[seq1]

    return etatS

#Codage blocs de 2 AVEC chevauchements mais seulement avec allele mineur et marqueurs non ancestraux
#Parametres : dictionnaire des sequences a l'etat s,
#           k, nombre de blocs

def Blocs2Moins(dictEtatS, k):
    d = len(BLOCS_2_19) #nbr total blocs differents
    etatS = [0] * k * d

    for seq1 in dictEtatS: #pour chaque sequence etat s
        for j in range(d): #pour chaque bloc j possible
            #on verifie si bloc position p de seq1 est egal au bloc j
            for p in range(k):
                if (seq1[p:(p+2)] == BLOCS_2_19[j]):
                    etatS[j*k + p] = etatS[j*k + p] + dictEtatS[seq1]

    return etatS

#Codage blocs de 3 AVEC chevauchements
#Parametres : dictionnaire des sequences a l'etat s,
#           k, nombre de blocs

def Blocs3Plus(dictEtatS, k):
    d = len(BLOCS_3) #nbr total blocs differents
    etatS = [0] * k * d

    for seq1 in dictEtatS: #pour chaque sequence etat s
        for j in range(d): #pour chaque bloc j possible
            #on verifie si bloc position p de seq1 est egal au bloc j
            for p in range(k):
                if (seq1[p:(p+3)] == BLOCS_3[j]):
                    etatS[j*k + p] = etatS[j*k + p] + dictEtatS[seq1]

    return etatS

#Codage blocs de 4 AVEC chevauchements
#Parametres : dictionnaire des sequences a l'etat s,
#           k, nombre de blocs

def Blocs4Plus(dictEtatS, k):
    d = len(BLOCS_4) #nbr total blocs differents
    etatS = [0] * k * d

    for seq1 in dictEtatS: #pour chaque sequence etat s
        for j in range(d): #pour chaque bloc j possible
            #on verifie si bloc position p de seq1 est egal au bloc j
            for p in range(k):
                if (seq1[p:(p+4)] == BLOCS_4[j]):
                    etatS[j*k + p] = etatS[j*k + p] + dictEtatS[seq1]

    return etatS

#Codage blocs de 4 AVEC chevauchements
#Parametres : dictionnaire des sequences a l'etat s,
#           k, nombre de blocs

def Blocs5Plus(dictEtatS, k):
    d = len(BLOCS_5) #nbr total blocs differents
    etatS = [0] * k * d

    for seq1 in dictEtatS: #pour chaque sequence etat s
        for j in range(d): #pour chaque bloc j possible
            #on verifie si bloc position p de seq1 est egal au bloc j
            for p in range(k):
                if (seq1[p:(p+5)] == BLOCS_5[j]):
                    etatS[j*k + p] = etatS[j*k + p] + dictEtatS[seq1]

    return etatS

#Codage avec une matrice de tous les haplotypes à l'état s
#lignes de 2 pour représenter des lignes vides
#Parametres : dictionnaire des sequences a l'etat s,
#             k, nombre de lignes dans la matrice
#             L, nombre de colonnes dans la matrice

def MatHap(dictEtatS, k, L):
    #matrice vide
    dictSorted = dict(sorted(dictEtatS.items()))
    etatS = torch.zeros((sum(dictSorted.values()), L), dtype = torch.float32)

    #on ajoute les sequences a l'etat s dans la matrice
    l = 0
    for seq in dictSorted:
        for r in range(dictSorted[seq]):
            etatS[l,] = torch.tensor(list(seq), dtype = torch.float32)
            l = l + 1   

    #On remplit les lignes vides
    #up = math.floor((k - l)/2)
    #down = math.ceil((k - l)/2)
    pad = torch.nn.ConstantPad2d((0, 0, 0, k-l), -1)
    etatS = pad(etatS)

    #return torch.transpose(etatS, 0, 1)
    return etatS