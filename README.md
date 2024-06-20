# ARGs_through_RL

This repository contains all code, files, and models used for the article "Constructing Ancestral Recombination Graphs through Reinforcement Learning". Here is a description of each file.

## json files
1. pop1: file with all the sequences used as a population for the generalization method.
2. pop2: file wih all the samples used for the approximation method with the same initial state (20 samples of 40 sequences, 20 samples of 60 sequences, and 20 samples of 100 sequences).

## python files
1. ARG4WG_memeS0.py: code to use the algorithm ARG4WG to build ARGs for the 60 samples in pop2.
2. ARG4WG_test.py: code to use the algorithm ARG4WG to build ARGs on the test set in pop1.
3. ARG_8blocs3.py: code to build ARGs (with RL) on the validation set in pop1 with 13 different agents. Code to select the best model for each agent.
4. ARG_8blocs3_ensMaj.py: code to build ARGs on the test set in pop1 using the ensemble method 'Majority'.
5. ARG_8blocs3_ensMean.py: code to build ARGs on the test set in pop1 using the ensemble method 'Mean'.
6. ARG_8blocs3_memeS0.py: code to build ARGs with RL for the 60 samples in pop2 after the learning process.
7. ARG_8blocs3_test.py: code to build ARGs on the test set in pop1 with 13 different agents and then use the ensemble method 'Minimum'.
8. Actions2.py: code to identify possible actions and next states in a state *s*.
9. Actions5.py: code to identify possible actions and next states in a state *s* according to the algorithm ARG4WG (recombinations are coded as defined in ARG4WG).
10. Codages.py: code to get the feature vector according to different representation by blocks of markers.
11. Echantillons.py: code to simulate the population used in the generalization method. Code that generated pop1.
12. Echantillons_memeS0.py: code to simulate the samples used in the approximation method with the same initial state. Code that generated pop2.
13. EtatInitial.py: code to return an initial state from one of the json files.
14. MyModelNN.py: code to build the neural network used to approximate the value function.
15. NN_MC_8blocs3_ensemble.py: code to train different agents using the RL Monte Carlo algorithm for the generalization method.
16. NN_MC_8blocs3_memeS0.py: code to train an agent using the RL Monte Carlo algorithm when learning with the same initial state.

## pth files
1. model_echant*no*_new.pth: learned model, always using sample *no* as initial state.
2. model_m5All_new_*no episode*_*seed*.pth: models saved during training for 13 different agents using the generalization method with samples of 5 sequences as initial state. The model was saved after *no episode* episodes and using *seed* as seed (each seed corresponds to one agent).
