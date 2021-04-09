#-*-coding:utf-8-*-
__author__ = 'Airren'
__date__ = '2018/7/12 5:36 PM'

"""
    统计实现已知最优结果的数目
"""
import  numpy as np
import pandas as pd

def compare_with_kol(data_path,benchmark):
    # bench_mark="./workbench/bin1data_KOS.csv"
    # bench_mark="./workbench/SCH_WAE2_KOS.csv"
    column = pd.read_csv(benchmark)
    pack_result = pd.read_csv(data_path)

    to_analysis_data = pd.merge(column, pack_result, on="Name",how="left")
    # to_analysis_data.to_csv("./results/bin1data.csv", index=False)

    # 是否是精确装箱 、实际装箱结果

    to_analysis_data["is_exact"] = to_analysis_data["KnownOptimalSOL"] /to_analysis_data[" OPT"]
    to_analysis_data["ratio"] = to_analysis_data[" SOL"] /to_analysis_data["KnownOptimalSOL"]

    column_name = to_analysis_data.columns.tolist()
    # print(column_name)
    # 'Name', 'KnownOptimalSOL', 'Algorithm', ' Descending?', ' Runtime(s)', ' n', ' SOL', ' OPT', ' SOL/OPT', ' capacity', ' result_bins', 'is_exact', 'ratio'

    list = ['Name', 'KnownOptimalSOL', 'Algorithm', ' Descending?', ' Runtime(s)', ' n', ' SOL', ' OPT', ' SOL/OPT', 'is_exact', 'ratio',' capacity', ' result_bins']
    to_analysis_data =to_analysis_data[list]
    path_kol = "./compare_kol/"+ data_path.split("/")[2]
    # to_analysis_data.to_csv(path_kol)
    # column_name = to_analysis_data.columns.tolist()
    # 统计数据集中精确装装箱问题的个数
    is_exact = to_analysis_data.drop_duplicates("Name")
    # print(len(is_exact))
    number_of_exact = int(is_exact[is_exact.is_exact == 1][["is_exact"]].apply(sum))
    # 统计实现了多少已知解法
    algorithms = set(to_analysis_data["Algorithm"].dropna())
    lunwen_result = {}
    for algorithm in algorithms:
        result = to_analysis_data[to_analysis_data.Algorithm==algorithm]
        # result =


        lunwen_result[algorithm]= [sum(result[result.ratio==1]["ratio"])]
        lunwen_result[algorithm].append(sum(result[result.ratio > 1]["ratio"].apply(lambda x: int(x))))
        lunwen_result[algorithm].append(sum(result[result.ratio > 1]["ratio"].apply(lambda x: int(x)))+sum(result[result.ratio==1]["ratio"]))


    lunwen_result = pd.DataFrame(lunwen_result, index=["is_exact","not_exact","total"]).T
    lunwen_result.to_csv(path_kol)



if __name__ == '__main__':
    compare_with_kol("./results/bin-pack_08-09_08-55-55_bin1data.csv")