import xgi
import numpy as np
import copy

# 外部方法，直接调用
def fw_percolation_flow(file_path: str, matrix_flow: np.ndarray, node_list: list):
    result_list = []
    hypergraph = func_hyperedge_read(file_path)
    l = len(node_list)
    node_states = func_node_flow(matrix_flow, node_list)
    failure_node_list = []
    q = 0
    while q <= 1:
        temp_list1 = []
        for item in node_states:
            if item[0] <= q:
                temp_list1.append(item[1])
        for item in temp_list1:
            if item not in failure_node_list:
                hypergraph.remove_edge(item)
                failure_node_list.append(item)
        component_list = xgi.algorithms.connected.connected_components(hypergraph)
        temp_list2 = []
        for item in component_list:
            temp_list2.append(len(item))
        temp_list2.sort(reverse = True)
        if len(temp_list2) <= 1:
            result_list.append((q, 0, 1))
            # result_list.append((1-(len(hypergraph.edges)/l), 0, 1)) # 更改横坐标轴为failure的比例
        else:
            result_list.append((q, temp_list2[1]/l, temp_list2[0]/l))
            # result_list.append((1-(len(hypergraph.edges)/l), temp_list2[1]/l, temp_list2[0]/l)) # 更改横坐标轴为failure的比例
        q += 0.01
    return result_list

def fw_percolation_degree(file_path: str, node_list: list):
    result_list = []
    hypergraph = func_hyperedge_read(file_path)
    l = len(node_list)
    node_states = func_node_degree(hypergraph)
    failure_node_list = []
    q = 0
    while q <= 1:
        temp_list1 = []
        for item in node_states:
            if item[0] <= q:
                temp_list1.append(item[1])
        for item in temp_list1:
            if item not in failure_node_list:
                hypergraph.remove_edge(item)
                failure_node_list.append(item)
        component_list = xgi.algorithms.connected.connected_components(hypergraph)
        temp_list2 = []
        for item in component_list:
            temp_list2.append(len(item))
        temp_list2.sort(reverse = True)
        if len(temp_list2) <= 1:
            result_list.append((q, 0, 1))
            # result_list.append((1-(len(hypergraph.edges)/l), 0, 1)) # 更改横坐标轴为failure的比例
        else:
            result_list.append((q, temp_list2[1]/l, temp_list2[0]/l))
            # result_list.append((1-(len(hypergraph.edges)/l), temp_list2[1]/l, temp_list2[0]/l)) # 更改横坐标轴为failure的比例
        q += 0.01
    return result_list

def fw_percolation_random(file_path: str, node_list: list):
    result_list = []
    hypergraph = func_hyperedge_read(file_path)
    remain_hyperedge_list = copy.deepcopy(node_list)
    l = len(node_list)
    count = 0
    for i in range(l):
        random_core = np.random.choice(a = remain_hyperedge_list, size = 1)[0]
        remain_hyperedge_list.remove(random_core)
        hypergraph.remove_edge(random_core)
        component_list = xgi.algorithms.connected.connected_components(hypergraph)
        component_len_list = []
        for item in component_list:
            component_len_list.append(len(item))
        component_len_list.sort(reverse=True)
        count += 1
        if len(component_len_list) <= 1:
            result_list.append((count/l, 0, 1))
        else:
            result_list.append((count/l, component_len_list[1]/l, component_len_list[0]/l))
    return result_list

def fw_percolation_cluster_list(file_path: str, matrix_flow: np.ndarray, node_list: list):
    result_list = []
    hypergraph = func_hyperedge_read(file_path)
    l = len(node_list)
    node_states = func_node_flow(matrix_flow, node_list)
    failure_node_list = []
    q = 0
    while q <= 1:
        temp_list1 = []
        for item in node_states:
            if item[0] <= q:
                temp_list1.append(item[1])
        for item in temp_list1:
            if item not in failure_node_list:
                hypergraph.remove_edge(item)
                failure_node_list.append(item)
        component_list = xgi.algorithms.connected.connected_components(hypergraph)
        temp_list2 = []
        for item in component_list:
            temp_list2.append(len(item))
        temp_list2.sort(reverse = True)
        result_list.append((q, temp_list2))
        q += 0.01
    return result_list

def fw_hm_emergence(file_path: str, matrix_flow: np.ndarray, node_list: list):
    result_list = []
    hypergraph = func_hyperedge_read(file_path)
    l = len(node_list)
    node_states = func_node_flow(matrix_flow, node_list)
    failure_node_list = []
    q = 0
    while q <= 1:
        temp_list1 = []
        for item in node_states:
            if item[0] <= q:
                temp_list1.append(item[1])
        for item in temp_list1:
            if item not in failure_node_list:
                hypergraph.remove_edge(item)
                failure_node_list.append(item)
        hm_m_list = func_hypermofits(hypergraph)
        file_1 = open('D:/桌面/' + str(q) + '.txt', mode = 'w+', encoding = 'UTF-8')
        for item in hm_m_list:
            print(str(item), file = file_1)
        file_1.close()
        input('当前q值: ' + str(q) + '    按任意键进入下一次循环')
        q += 0.01
    return result_list

def fw_t_hyperedge_num(file_path: str, matrix_flow: np.ndarray, node_list: list, qc_value: float, t_value = 4):
    hypergraph = func_hyperedge_read(file_path)
    node_states = func_node_flow(matrix_flow, node_list)
    hyperedge_dict = hypergraph.edges.ids
    result_list = [item[1] for item in node_states if item[0] >= qc_value and 1 < len(hyperedge_dict[item[1]]) <= t_value]
    print(len(result_list))
    return result_list

# 内部方法，请勿直接调用
def func_hyperedge_read(file_path: str):
    file = open(file_path, mode='r+', encoding='UTF8')
    hyperedge_dict = eval(file.read())
    file.close()
    node_list = hyperedge_dict.keys()
    hypergraph = xgi.Hypergraph()
    hypergraph.add_nodes_from(node_list)
    # c = 0
    for id in node_list:
        hypergraph.add_edge(hyperedge_dict[id], id=id)
    #     c += len(hyperedge_dict[id])
    # print(c/len(node_list))
    return hypergraph

def func_node_degree(hypergraph: xgi.Hypergraph):
    node_list = hypergraph.nodes
    result_dict = xgi.stats.nodestats.degree(hypergraph, node_list)

    # # 节点度越大，越容易被破坏
    # temp_arr = 1 - np.array(list(result_dict.values()))/max(result_dict.values()) + 0.0001
    # return sorted(zip(temp_arr/np.max(temp_arr), result_dict.keys()), reverse=True)

    # 节点度越小，越容易被破坏
    temp_arr = np.array(list(result_dict.values()))/max(result_dict.values())
    temp_arr = temp_arr - np.min(temp_arr)
    return sorted(zip(temp_arr/np.max(temp_arr), result_dict.keys()), reverse=True)

def func_node_flow(matrix_flow: np.ndarray, node_list: list):
    result_list = []
    for i in range(len(node_list)):
        result_list.append(np.sum(matrix_flow[:, i]) + np.sum(matrix_flow[i, :]))

    # 节点流量越大，越容易被破坏
    result_list = 1 - np.array(result_list)/np.max(result_list) + 0.0001
    return sorted(zip(result_list/np.max(result_list), node_list), reverse=True)

    # # 节点流量越小，越容易被破坏
    # result_list = np.array(result_list)/np.max(result_list)
    # result_list = result_list - np.min(result_list)
    # return sorted(zip(result_list/np.max(result_list), node_list), reverse=True)

def func_hypermofits(hypergraph: xgi.Hypergraph):
    result_list = []
    component_list = xgi.connected_components(hypergraph)
    # print(list(component_list))
    edge_dict = hypergraph.edges.ids
    edge_id_dict = list(edge_dict.keys())
    # print(edge_dict)
    for component in component_list:
        commponent_size = len(component)
        if commponent_size > 1:
            temp_list_1 = []
            for node in component:
                for item in edge_id_dict:
                    if (node in edge_dict[item]) and (len(edge_dict[item]) > 1) and ((item, edge_dict[item]) not in temp_list_1): temp_list_1.append((item, edge_dict[item]))
            result_list.append((component, temp_list_1))
    result_list.sort(key = lambda x: len(x[0]), reverse = False)
    result_list = [item for item in result_list if len(item[1]) > 1]
    return result_list

    # for component in component_list:
    #     commponent_size = len(component)
    #     if (commponent_size > 1) and (commponent_size < 8):
    #         temp_list_1 = []
    #         for core in component:
    #             if core in edge_dict.keys():
    #                 if len(edge_dict[core]) > 1: temp_list_1.append(len(edge_dict[core]))
    #         result_list.append((commponent_size, temp_list_1))
    # result_list = sorted(result_list, key=lambda x: x[0])
    # return result_list