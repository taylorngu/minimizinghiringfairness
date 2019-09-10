import numpy as np
import itertools

t_d_array = [1]*7 + [0]*9

print(t_d_array)

for permutation in itertools.permutations(t_d_array):
    print(permutation)
