import msprime
import json

#Module to simulate population for generalization method

n = 15_500 #population size
L = 10 #number of SNPs
s = 987654 #seed

ts = msprime.sim_ancestry(
        samples=n/2,
        recombination_rate= 5e-6,
        sequence_length= 10_000,
        population_size= 1_000_000,
        random_seed = s,
        model = 'hudson')

mts = msprime.sim_mutations(ts, rate= 5e-7, model = 'binary', random_seed = s)
mts = mts.simplify(reduce_to_site_topology = True)

i = 1
for var in mts.variants():
    if i == L:
        borne = var.site.position + 50
    i = i+1

mts = mts.keep_intervals([[0,borne]])

liste_pop = [] 
for i in range(n):
    individu = [0] * L
    for j in range(L):
        individu[j] = int(mts.genotype_matrix()[j][i])
       
    individu = tuple(individu)
    liste_pop.append(individu)

with open("pop1", "w") as fp:
    json.dump(liste_pop, fp)