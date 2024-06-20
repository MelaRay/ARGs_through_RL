import itertools
import torch
import math

#Module with functions to code feature vector
#Representation by blocks of markers

#blocks of 2, 3, 4, and 5 markers
ALL_marqueurs = [0,1,9]
BLOCS_2 = list(itertools.product(ALL_marqueurs, repeat = 2))
BLOCS_3 = list(itertools.product(ALL_marqueurs, repeat = 3))
BLOCS_4 = list(itertools.product(ALL_marqueurs, repeat = 4))
BLOCS_5 = list(itertools.product(ALL_marqueurs, repeat = 5))
BLOCS_2_19= list(itertools.product([0,1], repeat = 2))

#Coding blocks of 1
#Parameters: dictEtatS, dictionnary with sequences in state s
#           k, number of blocks
#Return: Feature vector for state s

def Blocs1(dictEtatS, k):
    d = len(ALL_marqueurs) #number different blocks
    etatS = [0] * k * d

    for seq1 in dictEtatS: #for each sequence in state s
        for j in range(d): #for each possible block j
            i = 0
            #check if block at position p in seq1 is block j
            for p in range(k):
                if (seq1[i] == ALL_marqueurs[j]):
                    etatS[j*k + p] = etatS[j*k + p] + dictEtatS[seq1]

                i = i + 1

    return etatS

#Coding blocks of 2 SNPs without overlap
#Parameters: dictEtatS, dictionnary with sequences in state s
#           k, number of blocks
#Return: Feature vector for state s

def Blocs2(dictEtatS, k):
    d = len(BLOCS_2) #number different blocks
    etatS = [0] * k * d

    for seq1 in dictEtatS: #for each sequence in state s
        for j in range(d): #for each possible block j
            i = 0
            #check if block at position p in seq1 is block j
            for p in range(k):
                if (seq1[i:(i+2)] == BLOCS_2[j]):
                    etatS[j*k + p] = etatS[j*k + p] + dictEtatS[seq1]

                i = i + 2

    return etatS

#Coding blocks of 2 SNPs with overlap
#Parameters: dictEtatS, dictionnary with sequences in state s
#           k, number of blocks
#Return: Feature vector for state s

def Blocs2Plus(dictEtatS, k):
    d = len(BLOCS_2) #number different blocks
    etatS = [0] * k * d

    for seq1 in dictEtatS: #for each sequence in state s
        for j in range(d): #for each possible block j
            #check if block at position p in seq1 is block j
            for p in range(k):
                if (seq1[p:(p+2)] == BLOCS_2[j]):
                    etatS[j*k + p] = etatS[j*k + p] + dictEtatS[seq1]

    return etatS

#Coding blocks of 2 SNPs with overlap, blocks with only mutations and non ancestral markers
#Parameters: dictEtatS, dictionnary with sequences in state s
#           k, number of blocks
#Return: Feature vector for state s

def Blocs2Moins(dictEtatS, k):
    d = len(BLOCS_2_19) #number different blocks
    etatS = [0] * k * d

    for seq1 in dictEtatS: #for each sequence in state s
        for j in range(d): #for each possible block j
            #check if block at position p in seq1 is block j
            for p in range(k):
                if (seq1[p:(p+2)] == BLOCS_2_19[j]):
                    etatS[j*k + p] = etatS[j*k + p] + dictEtatS[seq1]

    return etatS

#Coding blocks of 3 SNPs with overlap
#Parameters: dictEtatS, dictionnary with sequences in state s
#           k, number of blocks
#Return: Feature vector for state s

def Blocs3Plus(dictEtatS, k):
    d = len(BLOCS_3) #number different blocks
    etatS = [0] * k * d

    for seq1 in dictEtatS: #for each sequence in state s
        for j in range(d): #for each possible block j
            #check if block at position p in seq1 is block j
            for p in range(k):
                if (seq1[p:(p+3)] == BLOCS_3[j]):
                    etatS[j*k + p] = etatS[j*k + p] + dictEtatS[seq1]

    return etatS

#Coding blocks of 4 SNPs with overlap
#Parameters: dictEtatS, dictionnary with sequences in state s
#           k, number of blocks
#Return: Feature vector for state s

def Blocs4Plus(dictEtatS, k):
    d = len(BLOCS_4) #number different blocks
    etatS = [0] * k * d

    for seq1 in dictEtatS: #for each sequence in state s
        for j in range(d): #for each possible block j
            #check if block at position p in seq1 is block j
            for p in range(k):
                if (seq1[p:(p+4)] == BLOCS_4[j]):
                    etatS[j*k + p] = etatS[j*k + p] + dictEtatS[seq1]

    return etatS

#Coding blocks of 5 SNPs with overlap
#Parameters: dictEtatS, dictionnary with sequences in state s
#           k, number of blocks
#Return: Feature vector for state s

def Blocs5Plus(dictEtatS, k):
    d = len(BLOCS_5) #number different blocks
    etatS = [0] * k * d

    for seq1 in dictEtatS: #for each sequence in state s
        for j in range(d): #for each possible block j
            #check if block at position p in seq1 is block j
            for p in range(k):
                if (seq1[p:(p+5)] == BLOCS_5[j]):
                    etatS[j*k + p] = etatS[j*k + p] + dictEtatS[seq1]

    return etatS
