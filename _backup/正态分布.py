import numpy as np
from pandas import Series, DataFrame
from numpy.linalg import cholesky
import matplotlib as mpl
import matplotlib.pyplot as plt
# mpl.use('TkAgg')

sampleNo = 1000;
mu = 50
sigma = 15
np.random.seed(0)
s = np.random.normal(mu, sigma, sampleNo )


for i in range(1000):
    s[i] = int(s[i])




# plt.scatter(s, list(range(1000)))
# # # 可以过滤掉一部分脏数据
# # plt.xlim(30, 160)
# # plt.ylim(5, 50)
# plt.axis()
# # 设置title和x，y轴的label
# plt.title("BinPackingSet")
# plt.xlabel("items_weight")
# plt.ylabel("num")
# # 保存图片到指定路径
# # plt.savefig("../data/HeightAndWeight.png")
# # 展示图片 *必加
#
# plt.show()

# 给定一个序列t：
t = list(s)
hist = {}
for x in t:
    hist[x] = hist.get(x,0)+1
# 得到的结果是一个将值映射到其频数的字典。将其除以n即可把频数转换成频率，这称为归一化：
n = float(len(t))
pmf = {}
for x, freq in hist.items():
    pmf[x] = freq/n
# 绘制直方图：


vals= hist.keys()
freq = []
for k in pmf:
    freq.append(pmf[k])
count = []
for i in hist:
    count.append(hist[i])

plt.title("BinPackingSet")
plt.xlabel("items_weight")
plt.ylabel("num")

rectangle = plt.bar(vals, count)
# plt.title("BinPackingSet")
# plt.xlabel("items_weight")
# plt.ylabel("density")
# rectangles = plt.bar(vals, freq)
plt.show()

