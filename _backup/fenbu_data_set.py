__author__ = 'Airren'
__date__ = '2018/5/23 4:51 PM'


import numpy as np

data_num = 0
while data_num not in range(1, 9):
    data_num = int(input('''Please choose a num of data instance from the list:
                    1. Normal Distribution
                    2. Poisson Distribution
                    3. Uniform distribution
                    4. Exponential Distribution
                    5. Binomial Distribution
                    6. 
                    7. 
                    8. test(use for debug)
    Input your num:'''))

    # define dictionary of the data sets

data_name = {1: 'ND', 2: 'PD', 3: 'UD', 4: 'ED', 5: 'BD', 6: '', 7: '',8:'test_set'}

random_seed =  50

if data_name[data_num] == 'ND':
    capacity = 100

    for i in range(random_seed):

        np.random.seed(i)
        sampleNo = 100;
        mu = 50
        sigma = 15


        s = np.random.normal(mu, sigma, sampleNo )


        for i in range(len(s)):
            s[i] = int(s[i])

        s = list(s)
        for i in s:
            if i > capacity or i <1:
                s.remove(i)

        with open('./fenbu_set/ND_BPS.set', 'a+') as ND:
            ND.write(str(capacity)+','+str(s).strip("[|]")+'\n')

elif data_name[data_num] == 'PD':
    capacity = 100

    for i in range(random_seed):
        np.random.seed(i)
        sampleNo = 100;
        lam = 70

        s = np.random.poisson(lam ,size = sampleNo)


        for i in range(len(s)):
            s[i] = int(s[i])

        s = list(s)
        for i in s:
            if i > capacity or i <1:
                s.remove(i)
        with open('./fenbu_set/PD_BPS.set', 'a+') as ND:
            ND.write(str(capacity)+','+str(s).strip("[|]")+'\n')

elif data_name[data_num] == 'UD':
    capacity = 100

    for i in range(random_seed):
        np.random.seed(i)
        sampleNo = 100;
        low = 1
        height = 100

        s = np.random.randint(low ,height ,sampleNo)


        for i in range(len(s)):
            s[i] = int(s[i])

        s = list(s)
        for i in s:
            if i > capacity or i <1:
                s.remove(i)
        with open('./fenbu_set/UD_BPS.set', 'a+') as ND:
            ND.write(str(capacity)+','+str(s).strip("[|]")+'\n')

elif data_name[data_num] == 'ED':
    capacity = 100

    for i in range(random_seed):
        np.random.seed(i)
        sampleNo = 100
        lam = 10


        s = np.random.exponential(10 ,size = sampleNo)


        for i in range(len(s)):
            s[i] = int(s[i])

        s = list(s)
        for i in s:
            if i > capacity or i <1:
                s.remove(i)
        with open('./fenbu_set/ED_BPS.set', 'a+') as ND:
            ND.write(str(capacity)+','+str(s).strip("[|]")+'\n')

elif data_name[data_num] == 'BD':
    capacity = 100

    for i in range(random_seed):
        np.random.seed(i)
        sampleNo = 100
        p = 0.5


        s = np.random.binomial(capacity,0.5,size = sampleNo)


        for i in range(len(s)):
            s[i] = int(s[i])

        s = list(s)
        for i in s:
            if i > capacity or i <1:
                s.remove(i)
        with open('./fenbu_set/BD_BPS.set', 'a+') as ND:
            ND.write(str(capacity)+','+str(s).strip("[|]")+'\n')




##########################
 # # excute the bin packing algorithms use the data set
    # if data_name[data_num] == 'ED':
    #     # sampleNo, mu,sigma = list(filter(lambda x: int(x), input('请输入数据规模sampleNo、期望、方差，用空格隔开，默认100，50，15').split()))
    #     sampleNo, lamda,capacity = input('请输入数据规模sampleNo、lamda、容量，用空格隔开，例如1000 10 100').split()
    #     sampleNo = int(sampleNo)
    #     lamda = float(lamda)
    #     capacity = int(capacity)
    #
    #     for i in range(5):
    #         np.random.seed(i)
    #         items = np.random.exponential(lamda ,size = sampleNo)
    #
    #         items = list(items)
    #
    #         for i in range(sampleNo):
    #             items[i] = int(items[i])
    #
    #         for i in items:
    #             if i > capacity:
    #                 items.remove(i)
    #
    #         bin_pack.Bin.CAPACITY = capacity
    #
    #         print("the total items is:", len(items))
    #         print(items)
    #         test_all(items, OUTFILE)
    #
    # elif data_name[data_num] == 'BID':
    #     # sampleNo, mu,sigma = list(filter(lambda x: int(x), input('请输入数据规模sampleNo、期望、方差，用空格隔开，默认100，50，15').split()))
    #     sampleNo, p,capacity = input('请输入数据规模sampleNo、p、容量，用空格隔开，例如10 0.2 50').split()
    #     sampleNo = int(sampleNo)
    #     p = float(p)
    #     capacity = int(capacity)
    #
    #     for i in range(5):
    #         print(i)
    #         np.random.seed(i)
    #         items = np.random.binomial(capacity, p, size=sampleNo)
    #
    #         items = list(items)
    #
    #         for i in range(sampleNo):
    #             items[i] = int(items[i])
    #
    #         for i in items:
    #             if i > capacity:
    #                 items.remove(i)
    #
    #         bin_pack.Bin.CAPACITY = capacity
    #
    #         print("the total items is:", len(items))
    #         print(items)
    #
    #         test_all(items, OUTFILE)
    #
    #
    #
    # elif data_name[data_num] == 'PD':
    #     # sampleNo, mu,sigma = list(filter(lambda x: int(x), input('请输入数据规模sampleNo、期望、方差，用空格隔开，默认100，50，15').split()))
    #     sampleNo, mu, sigma,capacity = input('请输入数据规模sampleNo、期望、方差、容量，用空格隔开，整数例如1000，50，15，1000').split()
    #     sampleNo = int(sampleNo)
    #     mu = int(sampleNo)
    #     sigma = int(sampleNo)
    #     capacity = int(capacity)
    #     # sampleNo = 100;
    #     # mu = 50
    #     # sigma = 15
    #     np.random.seed(0)
    #     items = np.random.normal(mu, sigma, sampleNo)
    #     items = list(items)
    #
    #     for i in range(sampleNo):
    #         items[i] = int(items[i])
    #
    #     for i in items:
    #         if i > capacity:
    #             items.remove(i)
    #
    #     bin_pack.Bin.CAPACITY = capacity
    #     # print(bin_pack.Bin.CAPACITY,"++++++++++++++++++
    # else:
    #     print("Input Error")