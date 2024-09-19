import networkx as nx
import numpy as np
from copy import deepcopy
#--------------------
# Motter-Lai 模型
#--------------------
def ML_simulation(matrix_flow: np.ndarray, redundancy_index: float, K: int, echo_num: int):
    net = _func_net_gen(matrix_flow, redundancy_index)

#--------------------
# SIR 模型
#--------------------
def SIR_simulation(matrix_flow: np.ndarray, redundancy_index: float, K: int, prob: tuple, echo_num: int):
    result_dict, l = {}, len(matrix_flow)
    net = _func_net_gen(matrix_flow, redundancy_index)
    for i, node in enumerate(list(net.nodes)):
        temp_net = deepcopy(net)
        temp_net.nodes[node]['sirstate'] = 1
        for j in range(echo_num):
            print('当前总进度：' + str(round((i * 100) / l, 5)) + '%     当前进度：' + str(round((j * 100) / echo_num, 5)) + '%' + '    ' + str(prob))
            fail_node_list = _get_fail_node(temp_net, 'sir')
            fail_neibor_list = _func_select_neibor(temp_net, fail_node_list, K, 'sir')
            for fail_neibor in fail_neibor_list:
                if np.random.random() <= prob[0]: temp_net.nodes[fail_neibor]['sirstate'] = 1
            for fail_node in _get_fail_node(temp_net, 'sir'):
                if np.random.random() <= prob[1]: temp_net.nodes[fail_node]['sirstate'] = -1
            j += 1
        result_dict[node] = [item for item in temp_net.nodes if (temp_net.nodes[item]['sirstate'] == 1) or (temp_net.nodes[item]['sirstate'] == -1)]
    return result_dict

#--------------------
# 公有方法
#--------------------
def _func_net_gen(matrix_flow: np.ndarray, redundancy_index: float):
    # 读取并生成网络
    net = nx.DiGraph()
    for i in range(len(matrix_flow)): net.add_node(i, mlstate = 0, sirstate = 0) # mlstate为Motter-Lai状态，0为正常，1为破坏；sirstate中0为S，1为I，-1为R
    for i in range(matrix_flow.shape[0]):
        for j in range(matrix_flow.shape[1]):
            if matrix_flow[i, j] > 0: net.add_edge(i, j, flow = matrix_flow[i, j], capacity = matrix_flow[i, j] * redundancy_index)
    return net

def _get_fail_node(net: nx.DiGraph, mode: str):
    # 找到所有失效/感染节点
    if mode == 'sir': return[node for node in net.nodes if nx.get_node_attributes(net, 'sirstate')[node] == 1]
    elif mode == 'ml': return[node for node in net.nodes if nx.get_node_attributes(net, 'mlstate')[node] == 1]

def _func_select_neibor(net: nx.DiGraph, node_list: list, K: int, mode: str):
    # 失效节点邻居
    if mode == 'sir':
        result_list = []
        for node in node_list:
            temp_neibor_list = list(nx.neighbors(net, node))
            if len(temp_neibor_list) <= K: result_list += temp_neibor_list
            else: result_list += list(np.random.choice(temp_neibor_list, K, replace = False))
        return result_list
    elif mode == 'ml':
        result_dict = {} # 待完成