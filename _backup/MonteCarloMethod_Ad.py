#-*-coding:utf-8-*-
__author__ = 'Airren'
__date__ = '2018/7/12 10:20 AM'

import random
import numpy as np
import matplotlib.pyplot as plt

def calculate_score(candidates, stop_time, ratio_threshold):
    for i in range(stop_time, len(candidates)):
        observations = np.array(candidates[:i])
        threshold = np.percentile(observations, 100 - ratio_threshold)
        if candidates[i] >= threshold or i == len(candidates) -1:
            return candidates[i]


# stop_time = 5
# ratio_threshold = 0.05

lifes = [[random.uniform(0,1) for i in range(20)] for i in range(10000)]
strategies =[(stop_time, ratio_threshold) for stop_time in range(1,20) for ratio_threshold in range(2, 20, 1)]
scores = [0 for i in range(len(strategies))]
for i in range(len(strategies)):
    print(i)
    for life in lifes:

        scores[i] += calculate_score(life, strategies[i][0], strategies[i][1])
index_max = int(np.argmax(scores))
print(strategies[index_max])


max_score = max(scores)
min_score = min(scores)

colors = [1 - ((scores[i] - min_score) / (max_score - min_score) * 0.9 + 0.1) for i in range(100) ]


for i in range(len(scores)):
        plt.plot(strategies[i][0], strategies[i][1], 'o', color = str(colors))

plt.plot(strategies[index_max][0], strategies[index_max][1], 'ro', markesize=1)
plt.xlim([-1, 20])
plt.ylim([-1, 20])
plt.show()