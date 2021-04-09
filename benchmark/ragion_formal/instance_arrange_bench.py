__author__ = 'Airren'
__date__ = '2018/8/13 3:38 PM'

import os
import pandas as pd
import re

data_file_name_list = os.listdir("../../binpacking_data_set/instances/")
optimal_SOL = {}
for file in data_file_name_list:
    data  = open("../../binpacking_data_set/instances/"+file,'r')
    items = []
    for item in data:
        items.append(item.strip())
    items = items[1:]
    for item in items:
        if re.match('\w\d{0,4}_\d{0,4}', item):
            dic_key = item
            optimal_SOL[dic_key] = []
        elif item == '':
            pass
        elif re.match('\d{0,4}\s+\d{0,4}\s+\d{0,4}', item):
            item = item.split(' ')
            optimal_SOL[dic_key].append(int(item[2]))
        elif re.match(r'\d{0,4}.0\s+\d{0,4}\s+\d{0,4}', item):
            item = item.split(' ')
            optimal_SOL[dic_key].append(int(item[2]))
        else:
            pass




optimal_SOL = pd.DataFrame(optimal_SOL).T


optimal_SOL.to_csv("../instances_KOS.csv")
