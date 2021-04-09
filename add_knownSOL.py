#!/usr/bin/env python3
# -*- coding:utf-8 -*-
__author__ = 'Airren'
__date__ = '2018/8/14 11:52 AM'

"""
    原始数据上增加对比已知最优解的渐进竞争比
"""
import pandas as pd
from pandas import Series, DataFrame

import matplotlib as mpl
mpl.use('Agg')
# mpl.use('TkAgg')
import matplotlib.pyplot as plt
import pandas as pd

from  analysis import show_results



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
        competitive_ratio[algorithm] = sum(data["SOL/KOS"][algorithm])/len(data["SOL/KOS"][algorithm])
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


def add_knownSOL(resutl, konwn_SOL):

    resutls = pd.read_csv(resutl)
    konwn_SOL = pd.read_csv(konwn_SOL)
    data = resutls.merge(konwn_SOL, on="Name",how="left")


    data["SOL/KOS"] = data[" SOL"]/data["KnownOptimalSOL"]

    data["SOL/KOS"] = data["SOL/KOS"].apply(lambda x: round(x,6))


    print(data.columns)

    data = data[['Name', 'Algorithm', ' Descending?', ' Runtime(s)', ' n', ' SOL',
       ' OPT', ' SOL/OPT', 'KnownOptimalSOL',
       'SOL/KOS',' capacity', ' result_bins']]

    a = resutl.split("/")[2]
    data.to_csv("./results_final/"+resutl.split("/")[2],index=False)

    show_results("./results_final/"+resutl.split("/")[2])

if __name__ == '__main__':
    add_knownSOL("./results/bin-pack_08-14_04-39-45_waescher.csv","./benchmark/WAE_GAU_KOS.csv")



