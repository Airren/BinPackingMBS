#-*-coding:utf-8-*-
import math
from timeit import default_timer as timer
from copy import deepcopy
import time
from copy import *
import random

from binary_tree import BinaryTree

opt = 0

class Bin(object):

    CAPACITY = 1
    DATA_FILE_NAME = ''

    def __init__(self, name):
        # Items contains a list of (name, weight) tuples representing items packed into this bin
        self.items = []
        self.weight = 0
        self.name = name
        #self.CAPACITY = CAPACITY


    def get_residual_capacity(self, item_weight):
        """
        Returns the amount of space left in this bin if the given item_weight was added.
        If the result is >= zero, the item fits into the bin.
        """
        return self.CAPACITY - (self.weight + item_weight)

    def has_room(self, item_weight):
        return self.get_residual_capacity(item_weight) >= 0

    def try_add_item(self, item_name, item_weight):
        """
        Try and add the given item. Returns success status.
        :param item_name:
        :param item_weight:
        :return: true and adds the item if there is room, false if there is no room.
        """

        if not self.has_room(item_weight):
            return False

        self.weight += item_weight
        self.items.append((item_name, item_weight))
        return True

    def __str__(self):
        result = 'Bin {}: '.format(self.name)
        total_w = 0
        for item in self.items:
            result += 'Item {} w={}, '.format(item[0], round(item[1], 6))
            total_w += item[1]
        result = result.strip()
        result += " Total: " + str(round(total_w, 6))
        return result


def next_fit(items, decreasing):
    """
    Runtime: O(n)
    :param items: List of integer item weights, each less than Bin.CAPACITY
    :param decreasing: Whether or not to sort the items by non-increasing weights before packing
    :return: A list of 'bins', each a list of items contained in that bin.
    """

    # With next fit, sorting can actually make the solution considerably worse.
    if decreasing:
        items.sort(reverse=True)

    bins = []
    bin_index = 0
    b = Bin(bin_index)
    bin_index += 1
    bins.append(b)
    for item, weight in enumerate(items):
        if not b.try_add_item(item, weight):
            b = Bin(bin_index)
            bin_index += 1
            if not b.try_add_item(item, weight):
                raise Exception('Error! Could not add item into empty bin. Is the item larger than the bin?')
            bins.append(b)

    return bins

def first_fit(items, decreasing, existing_bins=None):
    """
    Runtime: O(n**2)
    :param items: List of integer item weights, each less than Bin.CAPACITY
    :param decreasing: Whether or not to sort the items by non-increasing weights before packing
    :return: A list of 'bins', each a list of items contained in that bin.
    """

    if decreasing:
        items.sort(reverse=True)

    if existing_bins is None:
        bins = []
    else:
        bins = existing_bins

    bin_index = 0
    for index, item in enumerate(items):
        packed = False
        for b in bins:
            if b.try_add_item(index, item):
                packed = True
                break
        if not packed:
            b = Bin(bin_index)
            bin_index += 1
            if not b.try_add_item(index, item):
                print('Error! Could not add item into empty bin. Is the item larger than the bin?')
            bins.append(b)
    return bins


def set_epsilon(eps):
    global epsilon
    epsilon = eps


def ptas_awfd(items, descending):     # Descending is ignored, but we accept it because pack_and_print will pass it
    print('Running ' + ptas_awfd.__name__ + ' with epsilon={}'.format(epsilon))

    small_items = []
    large_items = []
    for item in items:
        if item > epsilon / 2:
            large_items.append(item)
        else:
            small_items.append(item)

    large_packed = almost_worst_fit(large_items, True)
    return almost_worst_fit(small_items, True, large_packed)


def worst_fit(items, decreasing, existing_bins=None):
    return _worst_fit(items, decreasing, False, existing_bins)

def almost_worst_fit(items, decreasing, existing_bins=None):
    return _worst_fit(items, decreasing, True, existing_bins)

def _worst_fit(items, decreasing, almost, existing_bins=None):
    """
    Runtime: O(n*logn)
    :param almost: True to run AlmostWorstFit, False to run WorstFit
    :param items: List of integer item weights, each less than Bin.CAPACITY
    :param decreasing: Whether or not to sort the items by non-increasing weights before packing
    :return: A list of 'bins', each a list of items contained in that bin.
    """

    if decreasing:
        items.sort(reverse=True)

    if existing_bins:
        bins = existing_bins
    else:
        bins = []
    # The tree nodes' VALUES are the bin weight (this is what it is sorted by)
    # Each node's NAME is the bin index (in bins[]) that has that weight
    bin_weights = BinaryTree()

    bin_counter = 0
    for item, weight in enumerate(items):
        packed = False

        light_bin_node = None
        if almost:
            light_bin_node = bin_weights.second_min()

        if not almost or light_bin_node is None:        # Fallback for AWF - If there is no second_min(), use min()
            light_bin_node = bin_weights.min()

        if light_bin_node:
            lightest_bin = bins[light_bin_node.key.name]
            packed = lightest_bin.try_add_item(item, weight)

        if not packed:
            b = Bin(bin_counter)
            bin_counter += 1
            if not b.try_add_item(item, weight):
                raise Exception('Error! Could not add item into empty bin. Is the item larger than the bin?')
            bins.append(b)
            bin_weights.insert(b.weight, b.name)
        else:
            # Update the tree by removing the old bin weight, and adding the new one, still pointing to the same
            # index in the list of bins.
            bin_weights.remove(light_bin_node.key)
            bin_weights.insert(lightest_bin.weight, lightest_bin.name)

    return bins


def best_fit(items, decreasing, existing_bins=None):
    """
    Runtime: O(nlogn)
    :param items: List of integer item weights, each less than Bin.CAPACITY
    :param decreasing: Whether or not to sort the items by non-increasing weights before packing
    :param existing_bins: The algorithm can run on an already-packed set of bins, for supporting the PTAS.
    :return: A list of 'bins', each a list of items contained in that bin.
    """

    # Sort - so this is actually best fit decreasing
    if decreasing:
        items.sort(reverse=True)

    if existing_bins:
        bins = existing_bins
    else:
        bins = []

    bin_counter = 0
    # The tree nodes' VALUES are the bin weight (this is what it is sorted by)
    # Each node's NAME is the bin index (in bins[]) that has that weight
    bin_weights = BinaryTree()

    for item, weight in enumerate(items):
        # The current weight of an optimal bin (ie, if this item is weight 6, we want a bin with weight 4)
        optimal_weight = Bin.CAPACITY - weight
        best_bin_node = bin_weights.find_largest_lessthan(optimal_weight)

        if not best_bin_node:
            new_bin = Bin(bin_counter)
            bin_counter += 1

            if not new_bin.try_add_item(item, weight):
                raise Exception('Error! Could not add item into empty bin. Is the item larger than the bin?')
            bins.append(new_bin)
            bin_weights.insert(new_bin.weight, new_bin.name)
        else:
            best_bin = bins[best_bin_node.key.name]
            if not best_bin.try_add_item(item, weight):
                pass
                raise Exception('Error! Best bin did not have room for item!')
            else:
                bin_weights.remove(best_bin_node.key)
                bin_weights.insert(best_bin.weight, best_bin.name)
                #print('Update: name {}, weight {}, to name {}, weight {}'
                #      .format(best_bin_node.key.name, best_bin_node.key.value, best_bin.name, best_bin.weight))

    return bins


#-----------------MBSV1.1 algorithm----------------------------

def mbs(items,decreasing,exiting_bins=None):
    if decreasing:
        items.sort(reverse=True)
    if exiting_bins is None:
        bins = []
    else:
        bins = exiting_bins
    # bin index number start from 0 箱子编号
    bin_index = 0
    s = len(items)
    # alpha is a flag of the best of the past bins packing results
    # 过去装箱最好结果
    alpha = 0
    # pi_index begin with 1 in the algorithm description, so when use as index in list should -1
    # 算法描述中索引是从1开始的，使用过程中记得减去1
    j = 1
    temp_index = []
    # 所有物体索引
    sigma_index = list(range(0, s))
    # 临时索引
    pi_index = sigma_index[0:j]
    # 临时的重量
    pi_weight = 0
    # print("bin_capacity =", Bin.CAPACITY)
    for index in pi_index:
        pi_weight += items[index]
    # 标志符号
    exit_flag = False

    b = Bin(bin_index)
    bin_index += 1
    # 判断是否还有未装的物体
    while sigma_index != []:
        # 如果当前临时的重量刚好等于容量
        while pi_weight != Bin.CAPACITY:

            flag = False
            # 判断临时物体中的最后一个物体的编号是   物体中的第几个
            for q in range(0, len(sigma_index)):
                if sigma_index[q] == pi_index[j-1]:
                    break
            # 如果临时物体的重量 小于 箱子容量
            if pi_weight < Bin.CAPACITY:

                # 临时物体多加一个物体
                j += 1
                flag = True

                # 如果临时物体的重量 大于 之前的重量
                if pi_weight > alpha:
                    alpha = pi_weight
                    # #  temp_index decision #

                    # 准备装入箱子
                    temp_index = deepcopy(pi_index)

            # 判断 q 是不是 物体序列中的最后一个物体
            while not q < s-1:

                # 如果是物体序列中的最后一个物体 ，并且前面多加了物体
                if flag == True:
                    j -=1

                # 如果只剩一个物体
                if j == 1 or j == s:
                    exit_flag = True
                    break

                else:
                    j -= 1
                    if j > len(pi_index):
                        j = len(pi_index)-1
                    try:
                        pi_index.pop()
                    except:
                        pass

                    for q in range(0, len(sigma_index)):
                        try:
                            if sigma_index[q] == pi_index[j-1]:
                                break
                        except:
                            print('Error')

                if exit_flag == True:
                    break
            # 如果q不是最后一个物体，
            if exit_flag != True:
                # 如果前面新增了物体，就增加一个
                if j > len(pi_index):
                    pi_index.append(8888)
                # 如果前面没有新曾物体就替换一个
                pi_index[j-1]= sigma_index[q+1]
                pi_weight = 0
                for index in pi_index:
                    pi_weight += items[index]
            # 如果到了最后一个物体就直接装箱
            else:
                exit_flag = False
                break

        if pi_weight == Bin.CAPACITY:
            temp_index = deepcopy(pi_index)


        for index in temp_index:
            b.items.append((items[index]))
        # print("add successful**", b.items)

        bins.append(b)
        b = Bin(bin_index)
        bin_index += 1

        items_back = deepcopy(items)
        if temp_index :
            for i in temp_index:
                value = items_back[i]
                items.remove(value)

            # print("items",items)
        pi_weight = 0
        alpha = 0
        j = 1
        s = len(items)
        temp_index = []
        sigma_index = list(range(0, s))
        pi_index = sigma_index[0:j]



        for index in pi_index:
            pi_weight += items[index]
        # print("pi_weight =", pi_weight)
    return bins






#---------------------------------------------
#-------------------IMBS--------------------------
def imbs(items,decreasing,exiting_bins=None):
    if decreasing:
        items.sort(reverse=True)
    if exiting_bins is None:
        bins = []
    else:
        bins = exiting_bins
    # bin index number start from 0
    bin_index = 0
    s = len(items)
    min_value = items[s - 1]
    # alpha is a flag of the best of the past bins packing results
    alpha = 0
    # pi_index begin with 1 in the algorithm description, so when use as index in list should -1
    j = 1
    temp_index = []
    sigma_index = list(range(0, s))
    pi_index = sigma_index[0:j]
    pi_weight = 0
    # print("bin_capacity =", Bin.CAPACITY)
    for index in pi_index:
        pi_weight += items[index]
    exit_flag = False

    b = Bin(bin_index)
    bin_index += 1
    while sigma_index != []:
        # random.seed(timer())

        x = random.randint(0, int(min_value*(1-0.368)))

        while not ((pi_weight < Bin.CAPACITY or pi_weight == Bin.CAPACITY) and
                   (pi_weight > Bin.CAPACITY- x or pi_weight == Bin.CAPACITY- x ) and
                   pi_weight != 0):
            flag = False
            for q in range(0, len(sigma_index)):
                if sigma_index[q] == pi_index[j-1]:
                    break
            if pi_weight < Bin.CAPACITY:
                j += 1
                flag = True
                if pi_weight > alpha:
                    alpha = pi_weight
                    # #  temp_index decision # #
                    temp_index = deepcopy(pi_index)
            while not q < s-1:
                if flag == True:
                    j -=1
                if j == 1 or j == s:
                    exit_flag = True
                    break
                else:
                    j -= 1
                    if j > len(pi_index):
                        j = len(pi_index)-1
                    try:
                        pi_index.pop()
                    except:
                        pass

                    for q in range(0, len(sigma_index)):
                        try:
                            if sigma_index[q] == pi_index[j-1]:
                                break
                        except:
                            print('Error')

                if exit_flag == True:
                    break
            if exit_flag != True:
                if j > len(pi_index):
                    pi_index.append(8888)
                pi_index[j-1]= sigma_index[q+1]
                pi_weight = 0
                for index in pi_index:
                    pi_weight += items[index]

            else:
                exit_flag = False
                break
            x = random.randint(0, int(min_value * (1 - 0.368)))

        if ((pi_weight < Bin.CAPACITY or pi_weight == Bin.CAPACITY)
                and (pi_weight > Bin.CAPACITY- x or pi_weight == Bin.CAPACITY- x )
                and pi_weight != 0):
            temp_index = deepcopy(pi_index)


        for index in temp_index:
            b.items.append((items[index]))
        # print("add successful**", b.items)

        bins.append(b)
        b = Bin(bin_index)
        bin_index += 1

        items_back = deepcopy(items)
        if temp_index :
            for i in temp_index:
                value = items_back[i]
                items.remove(value)

            # print("items",items)
        pi_weight = 0
        alpha = 0
        j = 1
        s = len(items)
        if s > 1:
            min_value = items[s - 1]
        else:
            min_value = 0
        temp_index = []
        sigma_index = list(range(0, s))
        pi_index = sigma_index[0:j]



        for index in pi_index:
            pi_weight += items[index]
        # print("pi_weight =", pi_weight)
    return bins
#---------------------------------------------
#-------------------IIMBS--------------------------
def iimbs(items,decreasing,exiting_bins=None):
    global opt
    if decreasing:
        items.sort(reverse=True)
    if exiting_bins is None:
        bins = []
    else:
        bins = exiting_bins
    # bin index number start from 0
    results = {}

    mbs_bins = mbs(deepcopy(items),decreasing,exiting_bins=None)
    print(opt)
    if len(mbs_bins) == opt:
        bins = mbs_bins

    else:
        for i in range(10):
            bin = imbs(deepcopy(items), decreasing, exiting_bins=None)
            results[len(bin)] = bin

        iimbs_bins = results[min(results.keys())]

        if len(iimbs_bins) <= len(mbs_bins):
            bins = iimbs_bins
        else:
            bins = mbs_bins



    return bins
#---------------------------------------------
#------------------mbs'---------------------------
def mbs_(items,decreasing,exiting_bins=None):
    if decreasing:
        items.sort(reverse=True)
    if exiting_bins is None:
        bins = []
    else:
        bins = exiting_bins
    # bin index number start from 0
    bin_index = 0

    # alpha is a flag of the best of the past bins packing results
    alpha = 0
    # pi_index begin with 1 in the algorithm description, so when use as index in list should -1
    j = 1
    temp_index = []


    first_seed = items[0]
    remain_space = Bin.CAPACITY - items[0]
    items.pop(0)
    s = len(items)
    sigma_index = list(range(0, s))

    pi_index = sigma_index[0:j]
    pi_weight = 0
    # print("bin_capacity =", Bin.CAPACITY)
    for index in pi_index:
        pi_weight += items[index]
    exit_flag = False

    b = Bin(bin_index)
    bin_index += 1
    while sigma_index != []:
        while pi_weight != remain_space:
            flag = False
            for q in range(0, len(sigma_index)):
                if sigma_index[q] == pi_index[j-1]:
                    break
            if pi_weight < remain_space:
                j += 1
                flag = True
                if pi_weight > alpha:
                    alpha = pi_weight
                    # #  temp_index decision # #
                    temp_index = deepcopy(pi_index)
            while not q < s-1:
                if flag == True:
                    j -=1
                if j == 1 or j == s:
                    exit_flag = True
                    break
                else:
                    j -= 1
                    if j > len(pi_index):
                        j = len(pi_index)-1
                    try:
                        pi_index.pop()
                    except:
                        pass

                    for q in range(0, len(sigma_index)):
                        try:
                            if sigma_index[q] == pi_index[j-1]:
                                break
                        except:
                            print('Error')

                if exit_flag == True:
                    break
            if exit_flag != True:
                if j > len(pi_index):
                    pi_index.append(8888)
                pi_index[j-1]= sigma_index[q+1]
                pi_weight = 0
                for index in pi_index:
                    pi_weight += items[index]
            else:
                exit_flag = False
                break

        if pi_weight == remain_space:
            temp_index = deepcopy(pi_index)

        b.items.append(first_seed)
        for index in temp_index:
            b.items.append((items[index]))
        # print("add successful**", b.items)
        sss = 0
        for i in b.items:
            sss += i
        if sss > Bin.CAPACITY:
            print('Error')
        bins.append(b)
        b = Bin(bin_index)
        bin_index += 1

        items_back = deepcopy(items)
        if temp_index :
            for i in temp_index:
                value = items_back[i]
                items.remove(value)

            # print("items",items)
        pi_weight = 0
        alpha = 0
        j = 1
        if len(items) != 0:
            first_seed = items[0]
            remain_space = Bin.CAPACITY - items[0]
            items.pop(0)
            if len(items) == 0:
                b.items.append(first_seed)
                bins.append(b)

            temp_index = []
            s = len(items)
            sigma_index = list(range(0, s))
            pi_index = sigma_index[0:j]



            for index in pi_index:
                pi_weight += items[index]
        else:
            break
        # print("pi_weight =", pi_weight)
    return bins

#------------------imbs'---------------------------
def imbs_(items,decreasing,exiting_bins=None):
    if decreasing:
        items.sort(reverse=True)
    if exiting_bins is None:
        bins = []
    else:
        bins = exiting_bins
    # bin index number start from 0
    bin_index = 0

    # alpha is a flag of the best of the past bins packing results
    alpha = 0
    # pi_index begin with 1 in the algorithm description, so when use as index in list should -1
    j = 1
    temp_index = []


    first_seed = items[0]
    remain_space = Bin.CAPACITY - items[0]
    items.pop(0)
    s = len(items)
    sigma_index = list(range(0, s))
    min_value = items[s - 1]

    pi_index = sigma_index[0:j]
    pi_weight = 0
    # print("bin_capacity =", Bin.CAPACITY)
    for index in pi_index:
        pi_weight += items[index]
    exit_flag = False

    b = Bin(bin_index)
    bin_index += 1
    while sigma_index != []:
        random.seed(timer)
        x = random.randint(0, min_value)
        # print(x)
        while not ((pi_weight < remain_space or pi_weight == remain_space)
                   and (pi_weight > remain_space- x or pi_weight == remain_space- x )
                   and pi_weight != 0):
            flag = False
            for q in range(0, len(sigma_index)):
                if sigma_index[q] == pi_index[j-1]:
                    break
            if pi_weight < remain_space:
                j += 1
                flag = True
                if pi_weight > alpha:
                    alpha = pi_weight
                    # #  temp_index decision # #
                    temp_index = deepcopy(pi_index)
            while not q < s-1:
                if flag == True:
                    j -=1
                if j == 1 or j == s:
                    exit_flag = True
                    break
                else:
                    j -= 1
                    if j > len(pi_index):
                        j = len(pi_index)-1
                    try:
                        pi_index.pop()
                    except:
                        pass

                    for q in range(0, len(sigma_index)):
                        try:
                            if sigma_index[q] == pi_index[j-1]:
                                break
                        except:
                            print('Error')

                if exit_flag == True:
                    break
            if exit_flag != True:
                if j > len(pi_index):
                    pi_index.append(8888)
                pi_index[j-1]= sigma_index[q+1]
                pi_weight = 0
                for index in pi_index:
                    pi_weight += items[index]
            else:
                exit_flag = False
                break

        if ((pi_weight < remain_space or pi_weight == remain_space)
                   and (pi_weight > remain_space- x or pi_weight == remain_space- x )
                   and pi_weight != 0):
            temp_index = deepcopy(pi_index)

        b.items.append(first_seed)
        for index in temp_index:
            b.items.append((items[index]))
        # print("add successful**", b.items)

        bins.append(b)
        b = Bin(bin_index)
        bin_index += 1

        items_back = deepcopy(items)
        if temp_index :
            for i in temp_index:
                value = items_back[i]
                items.remove(value)

            # print("items",items)
        pi_weight = 0
        alpha = 0
        j = 1
        if len(items) > 0:
            first_seed = items[0]
            remain_space = Bin.CAPACITY - items[0]
            items.pop(0)
            if len(items) == 0:
                b.items.append(first_seed)
                bins.append(b)


            temp_index = []
            s = len(items)
            if s > 1:
                min_value = items[s - 1]
            else:
                min_value = 0
            sigma_index = list(range(0, s))
            pi_index = sigma_index[0:j]



            for index in pi_index:
                pi_weight += items[index]
        else:
            break
        # print("pi_weight =", pi_weight)
    return bins
#----------------IIMBS_------------------------
def iimbs_(items,decreasing,exiting_bins=None):
    if decreasing:
        items.sort(reverse=True)
    if exiting_bins is None:
        bins = []
    else:
        bins = exiting_bins
    # bin index number start from 0
    results = {}
    mbs_bins = mbs(deepcopy(items),decreasing,exiting_bins=None)
    for i in range(10):
        bin = imbs_(deepcopy(items),decreasing,exiting_bins=None)
        results[len(bin)] = bin

    iimbs_bins  = results[min(results.keys())]

    if len(iimbs_bins) <= len(mbs_bins):
        bins = iimbs_bins
    else:
        bins = mbs_bins



    return bins



def pack_and_print(items, algorithm, outfile, descending):
    # print(items)
    global opt
    tw = round(sum(item for item in items),6)
    opt =int( math.ceil(tw / Bin.CAPACITY))
    print('Total weight is {} and capacity per-bin is {}, so an optimal solution would use at least {} bins'
          .format(round(tw, 6), Bin.CAPACITY, opt))

    name = algorithm.__name__
    print('Packing {} items using {}, descending={}'.format(len(items), name, descending))
    # Copy items so that the algorithm's changes to the list don't persist
    items_copy = deepcopy(items)

    t = timer()
    bins = algorithm(items_copy, descending)
    elapsed = round(timer() - t, 6)

    print('Took ' + str(elapsed) + "s")
    sol = len(bins)
    print('Used {} bins compared to a best-case optimal of {}'.format(sol, opt))
    ratio = round(sol / opt, 6)
    if ratio < 1:
        print('Error')
        count = 0
        # for i in bins:
        #     if sum(j for j in i.items) > i.CAPACITY:
        #         print('hello')
        for i in bins:
            if sum(j[1] for j in i.items) > i.CAPACITY:
                print('hello')

            count = count + len(i.items)

        print(count)
    print('{} approx ratio for this instance is {}'.format(name, ratio))
    actual_bins= []
    for b in bins:
        actual_bins.append(b.items)

    print("actual_bins",actual_bins)
    bin_results = []
    for i in bins:
        bin_results.append(i.items)

    bin_results = str(bin_results).replace(',', '，')

    with open(outfile, 'a',encoding="utf-8") as f:
        f.write("{0}, {1}, {2}, {3}, {4}, {5}, {6}, {7}, {8},{9}\n"
                .format(Bin.DATA_FILE_NAME, name, descending, elapsed, len(items), sol,opt, ratio, Bin.CAPACITY, bin_results))
"""
    for index, b in enumerate(bins):
        print(b)
"""


def pack_print_all(items, outfile):
    # 非降序算法，在线启发式算法
    # pack_and_print(items, next_fit, outfile, False)
    # pack_and_print(items, first_fit, outfile, False)
    # pack_and_print(items, worst_fit, outfile, False)
    # pack_and_print(items, almost_worst_fit, outfile, False)
    # pack_and_print(items, best_fit, outfile, False)

    # 降序算法，离线算法
    pack_and_print(items, next_fit, outfile, True)
    pack_and_print(items, first_fit, outfile, True)
    pack_and_print(items, worst_fit, outfile, True)
    pack_and_print(items, almost_worst_fit, outfile, True)
    pack_and_print(items, best_fit, outfile, True)

    # pack_and_print(items, mbs, outfile, True)
    # # mbs'
    # pack_and_print(items, mbs_, outfile, True)
    # # imbs对应AMBS
    # pack_and_print(items, imbs, outfile, True)
    # # iimbs对应IAMBS
    # pack_and_print(items, iimbs, outfile, True)
    # 随机+ mbs'
    # pack_and_print(items, imbs_, outfile, True)
    # pack_and_print(items, iimbs_, outfile, True)


