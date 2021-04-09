__author__ = 'Airren'
__date__ = '2018/7/13 7:48 AM'


import pandas as pd
workbench1 = pd.read_table("./WAE_GAU1.Z",sep='\s+')
column_name1 = workbench1.columns.tolist()
index1 = ["Name","MTPmod"]
workbench1 = workbench1[index1]
column1= workbench1
column1.columns = ["Name","KnownOptimalSOL"]
# column.to_csv("../WAE_GAU1_KOS.csv", index=False)

workbench2 = pd.read_table("./WAE_GAU2.Z",sep='\s+')
column_name2 = workbench2.columns.tolist()
index2 = ["Name","MTPmod"]
workbench2 = workbench2[index2]
column2= workbench2
column2.columns = ["Name","KnownOptimalSOL"]

column = pd.concat([column1, column2], axis=0).dropna()
column.to_csv("../WAE_GAU_KOS.csv", index=False)