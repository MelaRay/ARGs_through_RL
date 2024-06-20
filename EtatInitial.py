import random

#Module with functions to create initial state from a set of sequences

#function to create initial state from a set of sequences keeping all sequences
#parameters: pop, list of all sequences from the population
#           e, number of the episode
#           m, sample size
#           taillePop, population size
#           index, list of indexes from 0 to population size, random order
# (population size)/(sample size) first indexes are sequences in first sample, 
# (population size)/(sample size) next indexes are sequences in second sample and so on.
#
# return: dictionnary of state s (all sequences)

def S0(pop, e, m, taillePop, index):
    
    e_mod = e % (taillePop/m)
    r = int(m*(e_mod - 1))
    dict = {}
    for i in range(r, r + m):
        indice = index[i]
        individu = tuple(pop[indice])
        if(individu not in dict):
            dict[individu] = 1 
        else:
            dict[individu] = dict[individu] + 1

    return dict

#function to create initial state from a set of sequences keeping one sequence of each type
#parameters: pop, list of all sequences from the population
#           r, index for first sequence in sample
#           m, sample size
#           taillePop, population size
#           index, list of indexes from 0 to population size
#
# return: dictionnary of state s (one sequence of each type)

def S0_x(pop, r, m, index):
    
    dict = {}
    for i in range(r, r + m):
        indice = index[i]
        individu = tuple(pop[indice])
        if(individu not in dict):
            dict[individu] = 1 

    return dict
