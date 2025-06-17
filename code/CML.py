import numpy as np
import heapq
import copy

# CML方法，直接调用
def cml_simulation(matrix_flow: np.ndarray, matrix_distance: np.ndarray, node_list: list, miu: tuple, k_neibor_num: int, r: float, alpha: float, ccc: float):
    result_dict = {}
    c, cl = 1, len(node_list)
    for node in node_list:
        print('当前总进度：' + str(ccc) + '%      ' + '当前进度：' + str(round(c/cl * 100, 5)) + str('%'))
        c += 1
        result_list = []
        matrix_f, matrix_d = copy.deepcopy(matrix_flow), copy.deepcopy(matrix_distance)
        node_state_dict = func_init_node_state(matrix_f, node_list, alpha)
        node_state_dict[node] += r
        pause_set_0 = set()
        fail_nodes_index_list = [node_list.index(node)]
        eq = True
        while eq:
            pause_set_1 = copy.deepcopy(pause_set_0)
            node_state_dict = func_renew_node_state(matrix_f, node_state_dict, node_list, miu)
            matrix_f = func_flow_assignment(matrix_f, matrix_d, fail_nodes_index_list, k_neibor_num)
            matrix_d = func_distance_renew(matrix_d, fail_nodes_index_list)
            for i in fail_nodes_index_list:
                pause_set_0.add(node_list[i])
            for i in fail_nodes_index_list:
                node_state_dict[node_list[i]] = 0
            for i in node_state_dict.keys():
                if node_state_dict[i] >= 1:
                    fail_nodes_index_list.append(node_list.index(i))
            if len(pause_set_0) == len(pause_set_1):
                eq = False
        for k in list(set(fail_nodes_index_list)):
            result_list.append(node_list[k])
        result_dict[node] = result_list
    return result_dict

def cml_simulation_robustness(matrix_flow: np.ndarray, matrix_distance: np.ndarray, node_list: list, miu: tuple, k_neibor_num: int, r: float, alpha: float, ccc: float):
    result_dict = {}
    c, cl = 1, len(node_list)
    for node in node_list:
        print('当前总进度：' + str(ccc) + '%      ' + '当前进度：' + str(round(c/cl * 100, 5)) + str('%'))
        c += 1
        result_list = []
        matrix_f, matrix_d = copy.deepcopy(matrix_flow), copy.deepcopy(matrix_distance)
        node_state_dict = func_init_node_state(matrix_f, node_list, alpha)
        node_state_dict[node] += r
        pause_set_0 = set()
        fail_nodes_index_list = [node_list.index(node)]
        eq = True
        while eq:
            pause_set_1 = copy.deepcopy(pause_set_0)
            node_state_dict = func_renew_node_state(matrix_f, node_state_dict, node_list, miu)
            matrix_f = func_flow_assignment_robustness(matrix_f, matrix_d, fail_nodes_index_list, k_neibor_num)
            matrix_d = func_distance_renew(matrix_d, fail_nodes_index_list)
            for i in fail_nodes_index_list:
                pause_set_0.add(node_list[i])
            for i in fail_nodes_index_list:
                node_state_dict[node_list[i]] = 0
            for i in node_state_dict.keys():
                if node_state_dict[i] >= 1:
                    fail_nodes_index_list.append(node_list.index(i))
            if len(pause_set_0) == len(pause_set_1):
                eq = False
        for k in list(set(fail_nodes_index_list)):
            result_list.append(node_list[k])
        result_dict[node] = result_list
    return result_dict

def cml_simulation_enhance(matrix_flow: np.ndarray, matrix_distance: np.ndarray, node_list: list, miu: tuple, k_neibor_num: int, r: float, alpha: float, ccc: float, enhance_nodes_list: list):
    result_dict = {}
    c, cl = 1, len(node_list)
    for node in node_list:
        print('当前总进度：' + str(ccc) + '%      ' + '当前进度：' + str(round(c/cl * 100, 5)) + str('%'))
        c += 1
        result_list = []
        if node in enhance_nodes_list:
            result_list.append(node)
        else:
            matrix_f, matrix_d = copy.deepcopy(matrix_flow), copy.deepcopy(matrix_distance)
            node_state_dict = func_init_node_state(matrix_f, node_list, alpha)
            node_state_dict[node] += r
            pause_set_0 = set()
            fail_nodes_index_list = [node_list.index(node)]
            eq = True
            while eq:
                pause_set_1 = copy.deepcopy(pause_set_0)
                node_state_dict = func_renew_node_state(matrix_f, node_state_dict, node_list, miu)
                for enhance_node in enhance_nodes_list:
                    node_state_dict[enhance_node] = 0.1
                matrix_f = func_flow_assignment(matrix_f, matrix_d, fail_nodes_index_list, k_neibor_num)
                matrix_d = func_distance_renew(matrix_d, fail_nodes_index_list)
                for i in fail_nodes_index_list:
                    pause_set_0.add(node_list[i])
                for i in fail_nodes_index_list:
                    node_state_dict[node_list[i]] = 0
                for i in node_state_dict.keys():
                    if node_state_dict[i] >= 1:
                        fail_nodes_index_list.append(node_list.index(i))
                if len(pause_set_0) == len(pause_set_1):
                    eq = False
            for k in list(set(fail_nodes_index_list)):
                result_list.append(node_list[k])
        result_dict[node] = result_list
    return result_dict

# 内部方法，请勿调用
def func_init_node_state(matrix_flow: np.ndarray, node_list: list, alpha: float):
    result_dict = {}
    node_flow_sum = np.array([])
    for i in range(len(node_list)):
        node_flow_sum = np.append(node_flow_sum, np.sum(matrix_flow[i, :]) + np.sum(matrix_flow[:, i]))
    node_flow_sum = node_flow_sum/(np.max(node_flow_sum)*alpha)
    for i in range(len(node_list)):
        result_dict[node_list[i]] = node_flow_sum[i]
    return result_dict

def func_flow_assignment(matrix_flow: np.ndarray, matrix_distance: np.ndarray, fail_nodes_index_list: list, k_neibor_num: int):
    result_arr = copy.deepcopy(matrix_flow)
    for i in fail_nodes_index_list:
        neibor_flow_in, neibor_flow_out = np.array([]), np.array([])
        neibor_list = func_k_neibor(matrix_distance, i, k_neibor_num)
        # print(neibor_list)
        for j in neibor_list:
            neibor_flow_in = np.append(neibor_flow_in, np.sum(result_arr[:, j]))
            neibor_flow_out = np.append(neibor_flow_out, np.sum(result_arr[j, :]))
        neibor_flow_in = neibor_flow_in/(np.sum(neibor_flow_in) + 0.0000001)
        neibor_flow_out = neibor_flow_out/(np.sum(neibor_flow_out) + 0.0000001)
        for j in range(len(result_arr)):
            ass_flow_in = result_arr[j, i] * neibor_flow_in
            ass_flow_out = result_arr[i, j] * neibor_flow_out
            for k in range(len(neibor_list)):
                result_arr[j, neibor_list[k]] += ass_flow_in[k]
                result_arr[neibor_list[k], j] += ass_flow_out[k]
        result_arr[i, :] = result_arr[i, :] * 0
        result_arr[:, i] = result_arr[:, i] * 0
    return result_arr

def func_flow_assignment_robustness(matrix_flow: np.ndarray, matrix_distance: np.ndarray, fail_nodes_index_list: list, k_neibor_num: int):
    result_arr = copy.deepcopy(matrix_flow)
    for i in fail_nodes_index_list:
        neibor_flow_in, neibor_flow_out = np.array([]), np.array([])
        neibor_list = func_k_neibor_robustness(matrix_distance, i, k_neibor_num)
        # print(neibor_list)
        for j in neibor_list:
            neibor_flow_in = np.append(neibor_flow_in, np.sum(result_arr[:, j]))
            neibor_flow_out = np.append(neibor_flow_out, np.sum(result_arr[j, :]))
        neibor_flow_in = neibor_flow_in/(np.sum(neibor_flow_in) + 0.0000001)
        neibor_flow_out = neibor_flow_out/(np.sum(neibor_flow_out) + 0.0000001)
        for j in range(len(result_arr)):
            ass_flow_in = result_arr[j, i] * neibor_flow_in
            ass_flow_out = result_arr[i, j] * neibor_flow_out
            for k in range(len(neibor_list)):
                result_arr[j, neibor_list[k]] += ass_flow_in[k]
                result_arr[neibor_list[k], j] += ass_flow_out[k]
        result_arr[i, :] = result_arr[i, :] * 0
        result_arr[:, i] = result_arr[:, i] * 0
    return result_arr

def func_distance_renew(matrix_distance: np.ndarray, fail_nodes_index_list: list):
    result_arr = copy.deepcopy(matrix_distance)
    max_num = np.max(result_arr) + 1
    for i in fail_nodes_index_list:
        result_arr[i, :] = result_arr[i, :] * 0 + max_num
        result_arr[:, i] = result_arr[:, i] * 0 + max_num
    return result_arr

def func_renew_node_state(matrix_flow: np.ndarray, node_state_dict: dict, node_list: list, miu: tuple):
    result_dict = {}
    for i in node_list:
        i_index = node_list.index(i)
        part1 = (1 - miu[0] - miu[1]) * 4 * node_state_dict[i] * (1 - node_state_dict[i])
        re_1, re_2, i_in_sum, i_out_sum = 0, 0, np.sum(matrix_flow[:, i_index]), np.sum(matrix_flow[i_index, :])
        for j in node_list:
            if i != j:
                temp_x, j_index = node_state_dict[j], node_list.index(j)
                if matrix_flow[i_index, j_index] != 0 and temp_x != 0:
                    re_1 += (matrix_flow[i_index, j_index] * 4 * temp_x * (1 - temp_x)) / (i_out_sum+0.0000001)
                if matrix_flow[j_index, i_index] != 0 and temp_x != 0:
                    re_2 += (matrix_flow[j_index, i_index] * 4 * temp_x * (1 - temp_x)) / (i_in_sum+0.0000001)
        part2, part3 = miu[0] * re_1, miu[1] * re_2
        ree = abs(part1 + part2 + part3)
        result_dict[i] = ree
    return result_dict

def func_k_neibor(matrix_distance: np.ndarray, node_index: int, k_neibor_num: int):
    result_list = []
    dis_list = list(matrix_distance[node_index, :])
    result_list = list(map(dis_list.index, heapq.nsmallest(k_neibor_num, dis_list)))
    return result_list

def func_k_neibor_robustness(matrix_distance: np.ndarray, node_index: int, k_neibor_num: int):
    result_list = []
    dis_list = list(matrix_distance[node_index, :])
    indexed_dis = [(val, idx) for idx, val in enumerate(dis_list)]
    smallest = heapq.nsmallest(k_neibor_num, indexed_dis, key=lambda x: x[0])
    result_list = [idx for (val, idx) in smallest]
    return result_list