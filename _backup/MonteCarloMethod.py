#-*-coding:utf-8-*-
__author__ = 'Airren'
__date__ = '2018/7/12 10:20 AM'

import random
import matplotlib.pyplot as plt

def check_success(candidates, stop_time):
    max_in_observation = max(candidates[:stop_time])
    chosen = 0
    for i in range(stop_time, len(candidates)):
        if candidates[i] >= max_in_observation:
            chosen = candidates[i]
            break
    max_in_all = max(candidates)
    if chosen == max_in_all:
        return True
    else:
        return False



lifes = [[random.uniform(0,1) for i in range(20)] for i in range(100000)]
success_count = [0 for i in range(20)]
for stop_time in range(1,20):
    for life in lifes:
        if check_success(life, stop_time):
            success_count[stop_time] +=1
print(success_count[1:20])
plt.plot(range(1,20), success_count[1:20], 'ro-', linewidth=2.0)
plt.show()