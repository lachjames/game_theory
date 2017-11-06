import numpy as np
import matplotlib.pyplot as plt

import itertools

import json

result_sets = {}

x = open("results.json", "r").read()
data = json.loads(x)

#print(data)

results = {}

p_s = set()
n_s = set()

for test in data:
    p = test["p"]
    g = test["game"]
    n = test["n_strats"]
    rankings = test["rankings"]
    
    p_s.add(p)
    n_s.add(n)

    k = (p, n)
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

#if len(w_s) == 1:
#    f, axarr = plt.subplots(len(p_s))
#else:
#    f, axarr = plt.subplots(len(w_s), len(p_s))

plots = []

for j, p in enumerate(sorted(p_s)):
    X = []
    Y = []
    for n in n_s:
        X += [n]
        Y += [1 - key_proportions[(p, n)]]
    print(X)
    print(Y)
    idx = tuple([j])
    lbl = "n={}".format(p)
    plots += plt.plot(X, Y, label=lbl)
    x1, x2, y1, y2 = plt.axis()
    plt.axis([x1, x2, -0.1, 1.1])
    ax = plt.gca()
    ax.set_xticks(np.arange(0, 10, 1))
    ax.set_yticks(np.arange(0, 1, 0.1))
    plt.grid()
    #axarr[idx].plot(X, Y)
    #axarr[idx].set_ylim([-0.1, 1.1])

print(plots)

plt.legend(handles=plots)

plt.show()