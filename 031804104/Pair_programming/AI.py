'''
AI实现模块,作用可自己编写测试用例进行测试,不需要进行图像识别
使用时可根据需要更换不同的测试样例
'''

import numpy as np
import pickle
import json
import requests


def show_table(table):
    '''表状态的可视化'''
    for i in range(0,9,3):
        print(table[i:i+3])
    print()


def get_stepmethod(table):
    '''输入为一个表,返回这个表到答案的走法（字符串序列）'''
    return transform_ans(dic[str(table)])
def transform_ans(way_method):
    ans = ''
    for i in range(len(way_method)-1,0,-1):  # 逆序遍历
        now = way_method[i]
        before = way_method[i-1]
        d_value = now-before
        if d_value == 3:
            ans += 'w'
        elif d_value == -3:
            ans += 's'
        elif d_value == 1:
            ans += 'a'
        elif d_value == -1:
            ans += 'd'
    return ans


def get_movedtable(move_process,table):
    '''根据移动序列返回按照移动序列移动后的表'''
    for move in move_process:  # 正序遍历
        index = table.index(0)
        if move == 'a':
            table[index],table[index-1] = table[index-1],table[index]
        elif move == 'd':
            table[index], table[index+1] = table[index+1], table[index]
        elif move == 'w':
            table[index],table[index-3] = table[index-3], table[index]
        elif move == 's':
            table[index], table[index+3] = table[index+3], table[index]
        show_table(table)  # 打印每一步的表状态
    return table


def force_swap(swap,bfs_tables):
    '''根据交换规则和当前所有表返回强制交换之后的所有表'''
    swaped_tables = []  # 在函数中对列表元素的处理并不会改变原列表
    print("进行强制交换")
    for table in bfs_tables:
        table = eval(table)
        table[swap[0]-1],table[swap[1]-1] = table[swap[1]-1],table[swap[0]-1]  # 一定要注意下标从0开始,swap-1
        swaped_tables.append(table)
    return swaped_tables  # 二维列表,每个元素是列表


def transform_operation(index,go):  #index是空格
    if index-go == 1:
        operation = 'a'
    elif index-go == -1:
        operation = 'd'
    elif index-go == 3:
        operation = 'w'
    else:
        operation = 's'
    return operation


def move(table): #传入为9个数值元素编码的列表
    newtables = []
    orgin_table = table[:]
    index = orgin_table.index(0)  # 空格
    # up,down,left,right = index-3,index+3,index-1,index+1
    if index % 3 == 0:
        direction = [index - 3, index + 3, index + 1]
    elif index % 3 == 2:
        direction = [index - 3, index + 3, index-1]
    else:
        direction = [index - 3, index + 3, index - 1, index + 1]
    for go in direction:  # 上下左右
        if go>=0 and go<=8:  # 可移动的位置下标
            table = orgin_table[:] #原始表交换!,若没有[:]只是复制引用
            table[index], table[go] = table[go], table[index]  # 交换
            newtables.append(str(table))  # 列表的列表
            if str(orgin_table) in dic_path:  # 每一个新增加的表状态路径都在列表里
                dic_path[str(table)] = dic_path[str(orgin_table)] + transform_operation(index,go)
            else:
                dic_path[str(table)] = transform_operation(index,go)
    return newtables


def bfs_execute(tables,stepnum):  # 默认参数
    '''输入元素为表状态的列表(二维列表),输出为走stepnum步后的所有可能状态'''
    for i in range(stepnum):
        current_tables = []  # 遗忘之前的
        for table in tables:
            try:
                table = eval(table)
            except:  # 否则就是列表
                table = table
            newtables = move(table)
            current_tables.extend(newtables)
        current_tables = list(set(current_tables))  #去重
        tables = current_tables[:]
    return current_tables


def find_solvable_optimal(swaped_tables):  # 输入为二维列表，每个元素是列表
    cost = 35 # max_cost == 32
    optimal_table = []
    unsolvable_tables = []
    for table in swaped_tables:
        if str(table) in dic:  # 有解
            if len(dic[str(table)])<cost:  # 更优
                cost = len(dic[str(table)])
                optimal_table = table

                if cost == 1:  # 答案
                    return optimal_table,cost,unsolvable_tables
        else:  # 无解
            unsolvable_tables.append(table)
    return optimal_table, cost, unsolvable_tables


def find_whole_optimal(cost, unsolvable_tables):
    target_table = []  # 自由交换之后的表状态
    free_swap = []  # 自由交换方法
    orgin_table = []  # 原强制交换表
    for table in unsolvable_tables:  # 遍历无解情况
        arr_table = np.array(table)
        for key in dic.keys():
            if len(dic[key]) >= cost:  # 不必往更深遍历
                break
            arr_target = np.array(eval(key))
            if len(arr_table[arr_table != arr_target]) == 2:  # 交换完之后可以一样
                cost = len(dic[key])  # 维护最小cost
                (d_index,) = np.where(arr_table != arr_target)
                d_index = (d_index + 1)  # 下标从0开始，位置从1开始
                orgin_table = table[:]
                target_table = eval(key)
                free_swap = list(d_index)
                break  # 不必往更深遍历
    return orgin_table,target_table,free_swap


def special_free_swap(table):
    free_swap = []  # 自由交换方法
    arr_table = np.array(table)
    for key in dic.keys():
        arr_target = np.array(eval(key))
        if len(arr_table[arr_table != arr_target]) == 2:  # 交换完之后可以一样
            (d_index,) = np.where(arr_table != arr_target)
            d_index = (d_index + 1)  # 下标从0开始，位置从1开始
            target_table = eval(key)
            free_swap = list(d_index)
            break  # 不必往更深遍历
    return target_table,free_swap


def write_test_sample():
    exclude = 9
    challenge = [1,7,3,0,6,8,5,4,2]  # 一维列表
    step = 15
    swap = [2, 7]
    return exclude,challenge,step,swap


def main(exclude,challenge,step,swap):
    global dic,dic_path,free_swap

    target_file = 'dic' + str(exclude) + '.pkl'
    pkl_file = open(target_file, 'rb')  # 图像识别挖去的是第几块
    dic = pickle.load(pkl_file)
    pkl_file.close()

    # 变量初始化
    dic_path = {}
    # 提交变量初始化
    operations = ''
    free_swap = []

    table = challenge[:]
    ## 特判
    if step == 0:
        table[swap[0] - 1], table[swap[1] - 1] = table[swap[1] - 1], table[swap[0] - 1]
        if str(table) in dic:  # 有解
            operations = get_stepmethod(table)
        else:  # 无解
            target_table, free_swap = special_free_swap(table)
            operations = get_stepmethod(target_table)

    else:
        ## 第一种情况
        if str(table) in dic and len(dic[str(table)]) - 1 <= step:  # 有解且可以在强制交换之前走完
            operations = get_stepmethod(table)
        ## 第二种情况
        else:  # 无解或者有解但在强制交换前走不完
            bfs_tables = bfs_execute([table], stepnum=step)
            swaped_tables = force_swap(swap, bfs_tables)  # 所有进行强制交换
            optimal_table, cost, unsolvable_tables = find_solvable_optimal(swaped_tables)  # 有解中的最优
            orgin_table, target_table, free_swap = find_whole_optimal(cost, unsolvable_tables)  # 无解中的更优(全局最优“)

            if len(free_swap) == 0:  # 无解中没有更优
                orgin_table = optimal_table[:]  # 为了接下来获取强制交换之前的原始表路径
                orgin_table[swap[0] - 1], orgin_table[swap[1] - 1] = orgin_table[swap[1] - 1], orgin_table[swap[0] - 1]
                operations = dic_path[str(orgin_table)] + get_stepmethod(optimal_table)

            else:  # 无解中有更优
                orgin_table[swap[0] - 1], orgin_table[swap[1] - 1] = orgin_table[swap[1] - 1], orgin_table[swap[0] - 1]
                operations = dic_path[str(orgin_table)] + get_stepmethod(target_table)

    print('operations:{},len(operations){},free_swap:{}'.format(operations, len(operations), free_swap))


if __name__ == "__main__":

    exclude, challenge, step, swap = write_test_sample()
    main(exclude, challenge, step, swap)
    ## 读取对应答案类型的答案文件







