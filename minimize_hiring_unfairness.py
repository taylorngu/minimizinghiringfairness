import numpy as np
import itertools
import pandas as pd
from statistics import stdev

data = pd.read_csv('hiringnewteachers.csv')
r_students = 1.67

data['total2020'] = data['10th']*r_students + data['11th']+ data['12th']
data['total2021'] = data['10th']+ data['11th']*r_students + data['12th']
data['total2022'] = data['10th']+ data['11th'] + data['12th']*r_students 

def partitions(n, k):
    for c in itertools.combinations(range(n+k-1), k-1):
        yield [b-a-1 for a, b in zip((-1,)+c, c+(n+k-1,))]

min_stddev = [1000, 2000, 3000, 4000, 5000, 6000, 7000]
min_range = [1000, 2000, 3000, 4000, 5000, 6000, 7000]
min_stddev_permutations = [1, 2, 3, 4, 5, 6, 7]
min_ran_permutations = [1, 2, 3, 4, 5, 6, 7]

fulldata = np.array([[0]*13])

count = 0
for p in partitions(7, 11):
    count = count + 1
    print(count)
    data_adj = data.copy()
    french = p[7]
    p[7] += p[8]
    p[8] += french
    data_adj['Number of teachers'] = data_adj['Number of teachers'] + np.array(p)
    data_adj['ratio2020'] = data_adj['total2020'] / data_adj['Number of teachers']
    data_adj['ratio2021'] = data_adj['total2021'] / data_adj['Number of teachers']
    data_adj['ratio2022'] = data_adj['total2022'] / data_adj['Number of teachers']
    data_adj['averageratio'] = (data_adj['ratio2020'] + data_adj['ratio2021'] + data_adj['ratio2022'])/3
    ratios = data_adj['averageratio'].tolist()
    stddev = stdev(ratios)
    ran = max(ratios) - min(ratios)
    fulldata = np.append(fulldata, [p + [stddev, ran]], axis=0)
    if stddev < max(min_stddev):
        idx = min_stddev.index(max(min_stddev))
        min_stddev.remove(max(min_stddev))
        min_stddev.append(stddev)
        min_stddev_permutations.pop(idx)
        min_stddev_permutations.append(p)
    if ran < max(min_range):
        idx = min_range.index(max(min_range))
        min_range.remove(max(min_range))
        min_range.append(ran)
        min_ran_permutations.pop(idx)
        min_ran_permutations.append(p)
    
    
print(min_range, min_ran_permutations)
print(min_stddev, min_stddev_permutations)

np.savetxt('outputs.csv', fulldata, delimiter=',')
