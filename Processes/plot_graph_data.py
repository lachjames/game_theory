from many import Many, random_game, r
from wright_fisher import Wright_Fisher
from moran import Moran

import numpy as np
import matplotlib.pyplot as plt

import itertools

import json

result_sets = {}

x = open("results.json", "r").read()
data = json.loads(x)

#print(data)

results = {}

w_s = set()
p_s = set()
n_s = set()

for test in data:
    w = test["w"]
    p = test["p"]
    g = test["game"]
    n = test["n_strats"]
    rankings = test["rankings"]
    
    w_s.add(w)
    p_s.add(p)
    n_s.add(n)

    k = (w, p, n)
    if k not in results.keys():
        results[k] = []
    results[k] += [rankings]

key_proportions = {}

for k in results.keys():
    matchings = 0
    for run in results[k]:
        orderings = set()
        for model_name, ordering in run.items():
            orderings.add(tuple(ordering))
        if len(orderings) == 1:
            matchings += 1
    
    match_prop = matchings / len(results[k])
    #print("Key {} has matching proportion {}".format(k, match_prop))
    key_proportions[k] = match_prop

print(key_proportions)

f, axarr = plt.subplots(len(w_s), len(p_s))

for i, w in enumerate(sorted(w_s)):
    for j, p in enumerate(sorted(p_s)):
        X = []
        Y = []
        for n in n_s:
            X += [n]
            Y += [key_proportions[(w, p, n)]]
        axarr[i, j].plot(X, Y)
        axarr[i, j].set_title("w={}, p={}".format(w, p))

plt.show()