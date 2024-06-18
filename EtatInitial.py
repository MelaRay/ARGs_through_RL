import random

### fonction pour creer un etat initial a partir d'une population
#parametres : pop, liste de toutes les sequences dans la population
#           e, numero de l'episode
#           m, taille des echantillons
#           taille,Pop, taille de la population
#           index, liste d'indices de 0 a taille de la population,
# le premier echantillon est compose des individus correspondant aux 
# (taille de la population)/(taille échantillon) premiers indices, le 2e, 
# les (taille de la population)/(taille échantillon) suivants et ainsi de suite.
#
# retourne un dictionnaire de l'etat initial (une sequence de chaque type echantillonne)

def S0(pop, e, m, taillePop, index):
    
    e_mod = e % (taillePop/m)
    r = int(m*(e_mod - 1))
    dict = {}
    for i in range(r, r + m):
        indice = index[i]
        individu = tuple(pop[indice])
        if(individu not in dict):
            dict[individu] = 1 #nouvel etat avec seq. individu
        else:
            dict[individu] = dict[individu] + 1

    return dict

### fonction pour creer un etat initial a partir d'une population
#renvoie x fois le meme echantillon avant de changer
#parametres : pop, liste de toutes les sequences dans la population
#           r, indice (de index) du premier individu de l'echantillon
#           m, taille des echantillons
#           index, liste d'indices de 0 a taille de la population,
# le premier echantillon est compose des individus correspondant aux 
# (taille de la population)/(taille échantillon) premiers indices, le 2e, 
# les (taille de la population)/(taille échantillon) suivants et ainsi de suite.
#
# retourne un dictionnaire de l'etat initial (une sequence de chaque type echantillonne)

def S0_x(pop, r, m, index):
    
    dict = {}
    for i in range(r, r + m):
        indice = index[i]
        individu = tuple(pop[indice])
        if(individu not in dict):
            dict[individu] = 1 #nouvel etat avec seq. individu

    return dict

def S0_all(pop, r, m, index):
    
    dict = {}
    for i in range(r, r + m):
        indice = index[i]
        individu = tuple(pop[indice])
        if(individu not in dict):
            dict[individu] = 1 #nouvel etat avec seq. individu
        else:
            dict[individu] = dict[individu] + 1

    return dict
