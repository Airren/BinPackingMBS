import math
import numpy as np

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



if __name__ == '__main__':
    path_name = os.getcwd()
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

    # for data_num in range(1,6):
    for i in range(0,1):

        OUTFILE = './results/bin-pack_' + time.strftime("%m-%d_%H-%M-%S", time.gmtime()) + "_" + data_name[data_num] + ".csv"
        with open(OUTFILE, 'a') as F:
            F.write('Algorithm, Descending?, n, Runtime (s), SOL, OPT, SOL/OPT, result_bins, capacity\n')

        if data_name[data_num] == 'ND':
            with open('./fenbu_set/ND_BPS.set', 'r') as ND:
                for i in ND:
                    items = i.split(',')
                    items = list(map(float, items))
                    items = list(map(int, items))
                    capacity = items[0]  # the second item is the bins' capacity
                    bin_pack.Bin.CAPACITY = capacity
                    # print(bin_pack.Bin.CAPACITY,"+++++++++++++++++++++++++++++++++++++++++")
                    print('num={num},capacity={capacity}'.format(num=str(len(items)-1), capacity=str(capacity)))
                    del items[0]

                    print("the total items is:", len(items))
                    print(items)
                    test_all(items, OUTFILE)
                show_results(OUTFILE)

        elif data_name[data_num] == 'PD':
            with open('./fenbu_set/PD_BPS.set', 'r') as ND:
                for i in ND:
                    items = i.split(',')
                    items = list(map(float, items))
                    items = list(map(int, items))
                    capacity = items[0]  # the second item is the bins' capacity
                    bin_pack.Bin.CAPACITY = capacity
                    # print(bin_pack.Bin.CAPACITY,"+++++++++++++++++++++++++++++++++++++++++")
                    print('num={num},capacity={capacity}'.format(num=str(len(items)-1), capacity=str(capacity)))
                    del items[0]

                    print("the total items is:", len(items))
                    print(items)
                    test_all(items, OUTFILE)
                show_results(OUTFILE)

        elif data_name[data_num] == 'UD':
            with open('./fenbu_set/UD_BPS.set', 'r') as ND:
                for i in ND:
                    items = i.split(',')
                    items = list(map(float, items))
                    items = list(map(int, items))
                    capacity = items[0]  # the second item is the bins' capacity
                    bin_pack.Bin.CAPACITY = capacity
                    # print(bin_pack.Bin.CAPACITY,"+++++++++++++++++++++++++++++++++++++++++")
                    print('num={num},capacity={capacity}'.format(num=str(len(items)-1), capacity=str(capacity)))
                    del items[0]

                    print("the total items is:", len(items))
                    print(items)
                    test_all(items, OUTFILE)
                show_results(OUTFILE)

        elif data_name[data_num] == 'ED':
            with open('./fenbu_set/ED_BPS.set', 'r') as ND:
                for i in ND:
                    items = i.split(',')
                    items = list(map(float, items))
                    items = list(map(int, items))
                    capacity = items[0]  # the second item is the bins' capacity
                    bin_pack.Bin.CAPACITY = capacity
                    # print(bin_pack.Bin.CAPACITY,"+++++++++++++++++++++++++++++++++++++++++")
                    print('num={num},capacity={capacity}'.format(num=str(len(items)-1), capacity=str(capacity)))
                    del items[0]

                    print("the total items is:", len(items))
                    print(items)
                    test_all(items, OUTFILE)
                show_results(OUTFILE)

        elif data_name[data_num] == 'BD':
            with open('./fenbu_set/BD_BPS.set', 'r') as ND:
                for i in ND:
                    items = i.split(',')
                    items = list(map(float, items))
                    items = list(map(int, items))
                    capacity = items[0]  # the second item is the bins' capacity
                    bin_pack.Bin.CAPACITY = capacity
                    # print(bin_pack.Bin.CAPACITY,"+++++++++++++++++++++++++++++++++++++++++")
                    print('num={num},capacity={capacity}'.format(num=str(len(items)-1), capacity=str(capacity)))
                    del items[0]

                    print("the total items is:", len(items))
                    print(items)
                    test_all(items, OUTFILE)
                show_results(OUTFILE)
