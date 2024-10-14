import heapq
import numpy as np
import networkx as nx

def enhance_nodes_list_cml(hyperedge_dict: dict, enhance_num: int):
    '''
    按照cml规则, 给出要加强的节点数量
    '''
    ss_list = []
    for item in list(hyperedge_dict.keys()):
        ss_list.append((item, len(hyperedge_dict[item])))
    ss_list.sort(reverse = True, key = lambda x: x[1])
    result_list = [item[0] for item in ss_list[: enhance_num]]
    return result_list

def enhance_nodes_list_flow(matrix_flow: np.ndarray, node_list: list, enhance_num: int):
    result_list = []
    node_flow_sum_list = []
    for i in range(len(node_list)):
        node_flow_sum_list.append(np.sum(matrix_flow[i, :]) + np.sum(matrix_flow[:, i]))
    node_flow_sum_list.sort(reverse=True)
    threshold = min(node_flow_sum_list[: enhance_num])
    for i in range(len(node_list)):
        if len(result_list) < enhance_num:
            if np.sum(matrix_flow[i, :]) + np.sum(matrix_flow[:, i]) >= threshold: result_list.append(node_list[i])
    return result_list

def enhance_nodes_list_degree(matrix_flow: np.ndarray, node_list: list, enhance_num: int):
    result_list = []
    net = nx.from_numpy_array(matrix_flow)
    node_degree_list = list(nx.degree(net))
    node_degree_list.sort(reverse=True, key= lambda x: x[1])
    for item in node_degree_list:
        if len(result_list) < enhance_num: result_list.append(item[0])
    return result_list

def enhance_nodes_list_random(node_list: list, enhance_num: int):
    return list(np.random.choice(node_list, enhance_num, replace = False))