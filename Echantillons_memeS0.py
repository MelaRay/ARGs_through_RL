import msprime
import json
import EtatInitial

N = [30, 40, 50] #sample size
RHO = [1.2e-8, 0.6e-8] #recombination rate
mu =  1.2e-8 #mutation rate
nbrSample = 10 #number of samples per combination n and rho
L = 10
s = 3

liste_pop = [] 
for n in N:
    for rho in RHO:
        s = s + s
        for sample in range(nbrSample):

            s = s + sample
            ts = msprime.sim_ancestry(
                    samples=n/2,
                    recombination_rate= rho,
                    sequence_length= 25_000,
                    population_size= 10_000,
                    random_seed = s,
                    model = 'hudson')

            #print(ts)

            mts = msprime.sim_mutations(ts, rate= mu, model = 'binary', random_seed = s)
            mts = mts.simplify(reduce_to_site_topology = True)

            i = 1
            for var in mts.variants():
                if i == L:
                    borne = var.site.position + 50
                i = i+1

            #print(len(mts.genotype_matrix()))

            mts = mts.keep_intervals([[0,borne]])

            #dict = {}
            for i in range(n):
                individu = [0] * L
                for j in range(L):
                    individu[j] = int(mts.genotype_matrix()[j][i])
                
                individu = tuple(individu)
                liste_pop.append(individu)

            #     if(individu not in dict):
            #         dict[individu] = 1 #nouvel etat avec seq. individu
            #     else:
            #         dict[individu] = dict[individu] + 1

            # print(dict)

            #print(len(liste_pop))

with open("pop3", "w") as fp:
    json.dump(liste_pop, fp)
                

            
