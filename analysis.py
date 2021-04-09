#！/usr/bin/env python3
#-*-coding:utf-8-*-
# import numpy as np
'''
    算法的平均竞争比、平均运行时间
'''
import pandas as pd
from pandas import Series, DataFrame

import matplotlib as mpl
mpl.use('Agg')
# mpl.use('TkAgg')
import matplotlib.pyplot as plt


def show_results(data_path):
    data = pd.read_csv(data_path, index_col="Algorithm")
    print(data)

    print(data.index)


    # algorithms = set()
    algorithms = set(data.index)
    print("algorithms =",algorithms)

    time = {}
    for algorithm in algorithms:
       # time[algorithm] = sum(list(data[" Runtime (s)"][algorithm]))/(len(list(data[" Runtime (s)"][algorithm]))+1)
       time[algorithm] = sum(data[" Runtime(s)"][algorithm]) / (len(data[" Runtime(s)"][algorithm]))

    print("time =",time)

    competitive_ratio = {}

    for algorithm in algorithms:
        competitive_ratio[algorithm] = sum(data[" SOL/OPT"][algorithm])/len(data[" SOL/OPT"][algorithm])
    print("competitive_ratio=",competitive_ratio)

    # # time
    plt.figure(figsize=(20, 10))
    plt.subplot(1, 3, 1)
    time = Series(time)
    time.plot(kind = 'barh', rot = 0,title = 'Runtime')

    competitive_ratio = Series(competitive_ratio)
    plt.subplot(1, 3, 2)
    competitive_ratio.plot(kind = 'barh', rot = 0, title = 'competitive_ratio ['+data_path.split('_')[3].split('.')[0]+']')

    plt.subplot(1, 3, 3)
    plt.axis('off')
    # plt.text(0.01, 0.01, '\ncompetitive_ratio\n'+str(competitive_ratio), size=10)
    plt.text(0.01, 0.01, 'Runtime:\n' + str(time) + '\ncompetitive_ratio\n' + str(competitive_ratio), size=10)
    # bbox=dict(facecolor="r", alpha=0.2)  family="fantasy", color="r", style="italic", weight="light"
    plt.savefig(data_path + '.png')



if __name__ == '__main__':
    show_results('./results/bin-pack_08-09_08-55-55_bin1data.csv')







