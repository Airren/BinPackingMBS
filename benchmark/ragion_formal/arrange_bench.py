__author__ = 'Airren'
__date__ = '2018/7/13 7:48 AM'


import pandas as pd
workbench = pd.read_table("./workbench_bin3data.txt")



# for i in range(len(workbench)):
#     name1 = workbench.ix[i,0]
#     name2 =workbench.ix[i,2]
#     name3 = workbench.ix[i,4]
#
#     mm1 = workbench.ix[i,1]
#     mm2 = workbench.ix[i,3]
#     mm3 = workbench.ix[i,5]
#
#
#     names.append(name1)
#     names.append(name2)
#     names.append(name3)
#
#     mms.append(mm1)
#     mms.append(mm2)
#     mms.append(mm3)
#
# all = {'Name':names, 'm*':mms}
# result = pd.DataFrame(all)
# print(result)
column_name = workbench.columns.tolist()
column_1 = workbench[column_name[0:2]]
column_1.columns = ["Name","KnownOptimalSOL"]
column_2 = workbench[column_name[2:4]]
# column_2.columns = column_name[0:2]
column_2.columns = ["Name","KnownOptimalSOL"]
column_3 = workbench[column_name[4:6]]
column_3.columns = ["Name","KnownOptimalSOL"]

column = pd.concat([column_1, column_2,column_3], axis=0).dropna()
column.ix[:,0] = column.ix[:,0].apply(lambda x: str(x)+".BPP")
column.to_csv("./bin3data_KOS.csv", index=False)