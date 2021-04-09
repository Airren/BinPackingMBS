__author__ = 'Airren'
__date__ = '2018/6/1 9:28 AM'

file_name = './results/bin-pack_06-01_01-26-16_waescher.csv'

import pandas as pd
file = pd.read_csv(file_name)
result = file['result_bins']
capacity = file['capacity']


for i in result:
    i = i.split(']，')

    def delpp(k):
        c = k.strip(' [[').strip(']]').strip('[').strip(']')
        return c

    x = list(map(delpp,i))
    for j in x:
        j = j.split('，')
        j = list(int(v) for v in j)
        s = sum(j)
        if s > 10000:
            print('Error', s)


print('hello')