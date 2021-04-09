__author__ = 'Airren'
__date__ = '2018/7/13 7:48 AM'


import pandas as pd
workbench1 = pd.read_table("./SCH_WAE1.Z.txt",sep='\s+')

column1_name = workbench1.columns.tolist()

index1 = ["Name","MTPmod"]

workbench1 = workbench1[index1]
column1= workbench1
column1.ix[:,0] = column1.ix[:,0].apply(lambda x: "SCH_WAE1_BPP_"+str(x))
column1.columns = ["Name","KnownOptimalSOL"]
# column1.to_csv("../SCH_WAE1_KOS.csv", index=False)

workbench2 = pd.read_table("./SCH_WAE2.Z.txt",sep='\s+')

column2_name = workbench2.columns.tolist()

index2 = ["Name","MTPmod"]

workbench2 = workbench2[index1]
column2= workbench2
column2.ix[:,0] = column2.ix[:,0].apply(lambda x: "SCH_WAE2_BPP_"+str(x))
column2.columns = ["Name","KnownOptimalSOL"]


column = pd.concat([column1, column2], axis=0).dropna()
column.to_csv("../SCH_WAE_KOS.csv", index=False)