import networkx as nx
import numpy as np
import copy
from collections import Counter
import heapq
import pickle as pkl
import matplotlib.pyplot as plt
import sklearn
from scipy.stats import mannwhitneyu

from CML import cml_simulation, cml_simulation_robustness

def func_scalefree_heter_flow(edge_num: int):
    result_list = np.random.randint(1, 100, size = edge_num, dtype = np.int64)
    result_list = np.exp(-100/(result_list ** 1))
    result_list /= np.max(result_list)
    return result_list

def generate_scalefree_net(m: int, N = 200):
    matrix_flow, node_list = np.zeros((N, N), dtype = np.float64), list(range(N))
    net = nx.barabasi_albert_graph(N, m)
    flow_list = func_scalefree_heter_flow(nx.number_of_edges(net))
    np.random.shuffle(flow_list)
    for i, edge in enumerate(net.edges):
        u, v = edge
        matrix_flow[u, v] = flow_list[i]
    matrix_distance = copy.deepcopy(matrix_flow)
    m_max = np.max(matrix_distance)
    matrix_distance = (m_max - matrix_distance)/m_max
    m_max = np.max(matrix_distance)
    for i in range(len(node_list)):
        matrix_distance[i, i] = m_max
    return matrix_flow, matrix_distance, node_list

k = 103 # 3, 13, 103
re_pval = []
for i in range(10):
    matrix_flow, matrix_distance, node_list = generate_scalefree_net(3)
    with open(f'D:/桌面/k_robustness_test/1.network_data/net_{i}.pkl', 'wb') as f: pkl.dump((matrix_flow, matrix_distance, node_list), f)
    cascading_result = cml_simulation(matrix_flow, matrix_distance, node_list, (0.4, 0.4), k, 1.2, 1.1, 0)
    with open(f'D:/桌面/k_robustness_test/2.cascading_result/cas_{i}.pkl', 'wb') as f: pkl.dump(cascading_result, f)
    cascading_result_r = cml_simulation_robustness(matrix_flow, matrix_distance, node_list, (0.4, 0.4), k, 1.2, 1.1, 0)
    with open(f'D:/桌面/k_robustness_test/3.cascading_result_r/cas_{i}.pkl', 'wb') as f: pkl.dump(cascading_result_r, f)
    stat, p = mannwhitneyu([len(item) for item in cascading_result.values()], [len(item) for item in cascading_result_r.values()])
    re_pval.append(p)
    print(stat, p)
print(re_pval)