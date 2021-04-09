import math

import os
import random
import time
import re

import bin_pack
from bin_pack import pack_print_all, pack_and_print, first_fit, set_epsilon, ptas_awfd, almost_worst_fit
from analysis import show_results


def random_int_list(min, max, length):
    result = []
    for x in range(0, length):
        result.append(random.randint(min, max))

    return result


def random_list(length):
    result = []
    for x in range(0, length):
        r = 0
        # No zero-weight items
        while r == 0:
            #r = random.random()
            pass
        result.append(r)

    return result


def test_all(items,outfile):
#    for i in range(128):
#        pack_print_all(items,outfile)
    pack_print_all(items,outfile)


def test_ptas(input_size, outfile):
    epses = [0.5, 0.25, 0.1, 0.05, 0.01, 0.001]

    for eps in epses:
        set_epsilon(eps)

        with open(outfile, 'a') as f:
            f.write('Doing PTAS, eps={}\n'.format(eps))
        for i in range(64):
            pack_and_print(random_list(input_size), ptas_awfd, outfile, True)


def worst_case_nf(input_size, outfile):
    print('Running a worst case for Next Fit')
    with open(outfile, 'a') as f:
        f.write('Running a worst case for Next Fit\n')

    bad_input_nf = [1 / 2, 1 / (2 * input_size)] * int(math.ceil(input_size / 2))
    pack_print_all(bad_input_nf, outfile)
    pack_and_print(bad_input_nf, first_fit, outfile, False)
    pack_and_print(bad_input_nf, first_fit, outfile, True)


def worst_case_ff(input_size, outfile):
    print('Running a worst case for First Fit')
    with open(outfile, 'a') as f:
        f.write('Running a worst case for First Fit\n')

    one_third = int(math.ceil(input_size / 3))
    bad_input_ff = [1 / 7 + 0.001] * one_third + [1 / 3 + 0.001] * one_third + [1 / 2 + 0.001] * one_third
    pack_print_all(bad_input_ff, outfile)
    pack_and_print(bad_input_ff, first_fit, outfile, False)
    pack_and_print(bad_input_ff, first_fit, outfile, True)


# INPUT_SIZE = 100000
# OUTFILE = 'bin-pack_' + time.strftime("%m-%d_%H-%M-%S", time.gmtime()) + ".csv"
# with open(OUTFILE, 'a') as F:
#     F.write('Algorithm, Descending?, n, Runtime (s), SOL, OPT, SOL/OPT\n')

#test_all(INPUT_SIZE, OUTFILE)
#test_ptas(INPUT_SIZE, OUTFILE)

#for x in range(128):
#    pack_and_print(random_list(INPUT_SIZE), almost_worst_fit, OUTFILE, True)
#    pack_and_print(random_list(INPUT_SIZE), almost_worst_fit, OUTFILE, False)

# FF is slow, reduce input size by order of mag.
# worst_case_nf(math.ceil(INPUT_SIZE/10), OUTFILE)
# worst_case_ff(math.ceil(INPUT_SIZE/10), OUTFILE)
###########################################################################################################
if __name__ == '__main__':
    path_name = os.getcwd()
    data_num = 0
    while data_num not in range(1, 9):
        data_num = int(input('''Please choose a num of data instance from the list:
                        1. bin1data
                        2. bin2data
                        3. bin3data
                        4. hard28
                        5. instances
                        6. schwerin
                        7. waescher
                        8. test(use for debug)
        Input your num:'''))

    # define dictionary of the data sets

    data_name = {1: 'bin1data', 2: 'bin2data', 3: 'bin3data', 4: 'hard28', 5: 'instances', 6: 'schwerin', 7: 'waescher',8:'test_set'}

    # get the file name of the data
    data_file_name = os.listdir(data_name[data_num])

    print(data_file_name)
    try:

        counter_flag = int(input('Please input a counter_flag[1-'+str(len(data_file_name))+']:'))
    except:
        counter_flag = 9999999
    # make a .csv to save the result

    OUTFILE = './results/bin-pack_' + time.strftime("%m-%d_%H-%M-%S", time.gmtime()) + "_" + data_name[data_num] + ".csv"
    with open(OUTFILE, 'a') as F:
        F.write('Algorithm, Descending?, n, Runtime (s), SOL, OPT, SOL/OPT,result_bins,capacity\n')

    # execute the bin packing algorithms use the data set
    counter = 1
    for data_file in data_file_name:

        if counter > counter_flag:
            break
        counter +=1


        print("./bindata/" + data_name[data_num] + "/" + data_file)

        data = open(data_name[data_num] + "/" + data_file, 'r+')

        if data_name[data_num] == 'bin1data':

            items = []
            for item in data:
                # if item.strip() =='':
                #     continue
                # else:

                items.append(int(item.strip()))  # strip 除去空格

            # print("the total items is:", len(items))

            # N = data_file[1]
            # C = data_file[3]
            # W = data_file[5]
            # num = {'1': 50, '2': 100, '3': 200, '4': 500}
            # capacity = {'1': 100, '2': 120, '3': 150, '4': 0, '5': 0}
            # weight = {'1': '[1,100]', '2': '[20,100]', '4': '[30,100]'}
            # print(num[N], capacity[C], weight[W])

            num = items[0]  # the first item is the items' number
            capacity = items[1]  # the second item is the bins' capacity
            bin_pack.Bin.CAPACITY = capacity
            # print(bin_pack.Bin.CAPACITY,"+++++++++++++++++++++++++++++++++++++++++")
            print('num={num},capacity={capacity}'.format(num=str(num), capacity=str(capacity)))
            del items[0:2]

            print("the total items is:", len(items))
            print(items)
            test_all(items, OUTFILE)

            #     print(data_file)
        elif data_name[data_num] == 'bin2data':

            items = []
            for item in data:
                items.append(int(item.strip()))  # strip 除去空格

            # print("the total items is:", len(items))

            num = items[0]  # the first item is the items' number
            capacity = items[1]  # the second item is the bins' capacity
            bin_pack.Bin.CAPACITY = capacity
            print('num={num},capacity={capacity}'.format(num=str(num), capacity=str(capacity)))
            del items[0:2]

            print("the total items is:", len(items))
            print(items)
            test_all(items, OUTFILE)

        elif data_name[data_num] == 'bin3data':

            items = []
            for item in data:
                items.append(int(item.strip()))  # strip 除去空格

            # print("the total items is:", len(items))

            num = items[0]  # the first item is the items' number
            capacity = items[1]  # the second item is the bins' capacity
            bin_pack.Bin.CAPACITY = capacity
            print('num={num},capacity={capacity}'.format(num=str(num), capacity=str(capacity)))
            del items[0:2]

            print("the total items is:", len(items))
            print(items)
            test_all(items, OUTFILE)

        elif data_name[data_num] == 'hard28':
            print(data)
            items = []
            for item in data:
                items.append(item.strip())
            # print(items)
            data_dic = {}
            # dic_key='0'

            for item in items:
                # print(item)
                if re.match('\'BPP\s+\d{0,9}\'', item):
                    # print(item)
                    # print(data_dic[dic_key])
                    dic_key = re.sub('\'', '', re.sub('\s+', '_', item))

                    # print(dic_key)
                    data_dic[dic_key] = []

                elif item == '':
                    pass
                else:
                    item = item.split(' ')
                    data_dic[dic_key].append(int(item[0]))

            # 遍历字典进行测试
            for item in data_dic:
                items = data_dic[item][2:]
                bin_pack.Bin.CAPACITY = data_dic[item][1]
                print(bin_pack.Bin.CAPACITY,"+++++++++++++++++++++++++++++++++++++++++")
                print(item)
                print(items)
                test_all(items, OUTFILE)
                # print(data_dic)

                # else:
                #     #print("no")
                #     pass


        elif data_name[data_num] == 'instances':
            print(data)
            items = []
            for item in data:
                items.append(item.strip())
            # print(items[1:])
            items = items[1:]
            data_dic = {}
            # dic_key='0'

            for item in items:
                # print(item)
                if re.match('\w\d{0,4}_\d{0,4}', item):
                    print(item)
                    # print(data_dic[dic_key])
                    dic_key = item

                    # print(dic_key)
                    data_dic[dic_key] = []
                #
                elif item == '':
                    pass
                elif re.match('\d{0,4}\s+\d{0,4}\s+\d{0,4}', item):
                    print(item)
                    item = item.split(' ')
                    data_dic[dic_key].append(int(item[0]))
                    # bin_pack.Bin.CAPACITY = int(item[0])
                    # print(bin_pack.Bin.CAPACITY, "+++++++++++++++++++++++++++++++++++++++++")

                elif re.match(r'\d{0,4}.0\s+\d{0,4}\s+\d{0,4}', item):
                    print(item)
                    item = item.split(' ')
                    data_dic[dic_key].append(float(item[0]))
                    # bin_pack.Bin.CAPACITY = float(item[0])
                    # print(bin_pack.Bin.CAPACITY, "+++++++++++++++++++++++++++++++++++++++++")
                    continue
                else:
                    # item = item.split(' ')
                    if re.match('\d{0,4}\.\d{1,4}', item):
                        data_dic[dic_key].append(float(item))
                    else:
                        data_dic[dic_key].append(int(item))

            # 遍历字典进行测试

            for item in data_dic:
                bin_pack.Bin.CAPACITY = data_dic[item][0]
                print(bin_pack.Bin.CAPACITY, "+++++++++++++++++++++++++++++++++++++++++")
                items = data_dic[item][1:]
                print(item)
                print(items)
                test_all(items, OUTFILE)
                # print(data_dic)

                # else:
                #     #print("no")
                #     pass

        elif data_name[data_num] == 'schwerin':
            if not re.match(r'SCH_WAE\d.BPP', data_file):
                print("------------------" + data_file)
                continue
            print(data)
            items = []
            for item in data:
                items.append(item.strip())
            # print(items)
            data_dic = {}
            # dic_key='0'

            for item in items:
                # print(item)
                if re.match('\'BPP\s+\d{0,9}\'', item):
                    # print(item)
                    # print(data_dic[dic_key])
                    dic_key = re.sub('\'', '', re.sub('\s+', '_', item))

                    # print(dic_key)
                    data_dic[dic_key] = []

                elif item == '':
                    pass
                else:
                    item = item.split(' ')
                    data_dic[dic_key].append(int(item[0]))

            # 遍历字典进行测试
            for item in data_dic:
                items = data_dic[item][2:]
                print(item)
                print(items)
                bin_pack.Bin.CAPACITY = data_dic[item][1]
                print(bin_pack.Bin.CAPACITY, "+++++++++++++++++++++++++++++++++++++++++")
                test_all(items, OUTFILE)



        elif data_name[data_num] == 'waescher':
            if not re.match(r'WAE_GAU\d.BPP', data_file):
                print("------------------" + data_file)
                continue
            print(data)
            items = []
            for item in data:
                items.append(item.strip())
            # print(items)
            data_dic = {}
            # dic_key='0'

            for item in items:
                # print(item)
                if re.match('\'TEST\d{0,4}\'', item):
                    # print(item)
                    # print(data_dic[dic_key])
                    # dic_key = re.sub('\'', '', re.sub('\s+', '_', item))
                    dic_key = item
                    # print(dic_key)
                    data_dic[dic_key] = []

                elif item == '':
                    continue
                else:
                    item = item.split(' ')
                    data_dic[dic_key].append(int(item[0]))

            # 遍历字典进行测试
            for item in data_dic:
                items = data_dic[item][2:]
                print(item)
                print(items)
                bin_pack.Bin.CAPACITY = data_dic[item][1]
                # print(bin_pack.Bin.CAPACITY,"+++++++++++++++++++++++++++++++++++++++++")
                test_all(items, OUTFILE)
        if data_name[data_num] == 'test_set':

            # items = []
            # for item in data:
            #     items.append(int(item.strip()))  # strip 除去空格
            #
            #
            #
            # num = items[0]  # the first item is the items' number
            # capacity = items[1]  # the second item is the bins' capacity
            # bin_pack.Bin.CAPACITY = capacity
            # # print(bin_pack.Bin.CAPACITY,"+++++++++++++++++++++++++++++++++++++++++")
            # print('num={num},capacity={capacity}'.format(num=str(num), capacity=str(capacity)))
            # del items[0:2]
            #
            # print("the total items is:", len(items))
            # # print(items)
            ########################### single instance ##################################
            # bin_pack.Bin.CAPACITY = 17
            # items = [17,9,7,6,5,5,4,4,4,4,4,4,4,4,4]
            # #
            bin_pack.Bin.CAPACITY = 61

            items =[44,24,24,22,21,17,8,8,6,6]

            # items = "[25]， [31]， [36]， [37]， [42]， [42]， [43]， [43]， [47]， [47]， [50]， [51]，\
            #  [51]， [52]， [52]， [52]， [56]， [56]， [56]， [56]， [60]， [67]， [68]， [71]， [72]，\
            #   [72]， [78]， [78]， [79]， [83]， [84]"
            #
            # items = "[25]， [31]， [36]， [37]， [42]， [42]， [43]， [43]"
            # items = items.split('，')
            # new_item = []
            # for i in items:
            #     new_item.append(int(i.strip(' [').strip(']')))
            # bin_pack.Bin.CAPACITY = 100
            # items = new_item


            test_all(items, OUTFILE)
        else:
            print("Input Error")

    # show_results(OUTFILE)