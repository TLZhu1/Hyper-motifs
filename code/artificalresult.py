import pickle
import numpy as np
import matplotlib.pyplot as plt
import sklearn.cluster
import xgi

def _func_file_name_list_gen(mode: str):
    r, m, cascad_list, net_list = 0.05, 1, [], []
    if mode == 'r' or mode == 'ws':
        for _ in range(4):
            for count in range(10):
                cascad_list.append(str(round(r, 2)) + '_' + str(count + 1) + '.txt')
                net_list.append(str(round(r, 2)) + '_' + str(count + 1) + '.pkl')
            r += 0.05
    elif mode == 'ba':
        for _ in range(4):
            for count in range(10):
                cascad_list.append(str(round(m, 2)) + '_' + str(count + 1) + '.txt')
                net_list.append(str(round(m, 2)) + '_' + str(count + 1) + '.pkl')
            m += 1
    return cascad_list, net_list

def _func_artifical_data_process(data_path: str, mode: str):
    cascading_result, net_data_result = [], []
    cascad_result_file_name_list, net_result_file_name_list = _func_file_name_list_gen(mode)
    for i in range(len(cascad_result_file_name_list)):
        with open(data_path + mode + '/' + cascad_result_file_name_list[i], mode = 'r', encoding = 'UTF-8') as file:
            data = eval(file.read())
            cascading_result.append(data)
        with open(data_path + mode + '/' + net_result_file_name_list[i], 'rb') as file_x:
            data_x = pickle.load(file_x)
            net_data_result.append(data_x)
    return cascading_result, net_data_result

def _func_cardinality_merge(cascading_result: list):
    temp_1, temp_2, temp_3, temp_4 = {}, {}, {}, {}
    temp_l1, temp_l2, temp_l3, temp_l4 = [], [], [], []
    for item in cascading_result[0:10]:
        t = list(item.values())
        for itemm in t: temp_l1.append(itemm)
    for item in cascading_result[10:20]:
        t = list(item.values())
        for itemm in t: temp_l2.append(itemm)
    for item in cascading_result[20:30]:
        t = list(item.values())
        for itemm in t: temp_l3.append(itemm)
    for item in cascading_result[30:40]:
        t = list(item.values())
        for itemm in t: temp_l4.append(itemm)
    for i in range(len(temp_l1)):
        temp_1[i] = temp_l1[i]
        temp_2[i] = temp_l2[i]
        temp_3[i] = temp_l3[i]
        temp_4[i] = temp_l4[i]
    return [temp_1, temp_2, temp_3, temp_4]

def _func_p_gen(cardinality_list: list):
    size_list = np.unique(np.array(cardinality_list))
    p_sum = len(size_list)
    p_list = []
    for i in range(p_sum):
        c = 0
        for j in cardinality_list:
            if size_list[i] == j:
                c += 1
        p_list.append(c/len(cardinality_list))
    return size_list, p_list

def _func_line_fit(size_list: np.ndarray, p_list: list):
    lg_x, lg_y = np.log10(size_list), np.log10(np.array(p_list))
    a, b = np.polyfit(lg_x, lg_y, 1)
    # print(a)
    result_x, result_y = [], []
    fit_list = np.linspace(0, max(lg_x), 10)
    for i in fit_list:
        result_x.append(10**i)
        result_y.append(10**(a*i + b))
    return result_x, result_y, a

def _cardinality_cluster(hyperedge_dict: dict):
    data = np.array([[len(item) for item in hyperedge_dict.values()]])
    data = np.reshape(data, (-1, 1))
    km = sklearn.cluster.KMeans(n_clusters = 2, init = [[np.min(data)], [np.max(data)]]).fit(data)
    re_d = []
    for i in range(len(data)):
        re_d.append((int(data[i][0]), list(km.labels_)[i]))
    # print(sorted(re_d, reverse = True, key = lambda x: x[0]))
    return min([item[0] for item in sorted(re_d, reverse = True, key = lambda x: x[0]) if item[1] == 1])

def _fig_cardinality_distribution(data_path: str, mode: str):
    cascading_result, _ = _func_artifical_data_process(data_path, mode)
    cardinality_result = _func_cardinality_merge(cascading_result)
    for name, item in enumerate(cardinality_result):
        dict_value = item.values()
        cardinality_list = []
        for i in dict_value:
            cardinality_list.append(len(i))
        cardinality_list.sort(reverse=False)
        cut_num = len(cardinality_list) - cardinality_list.index(_cardinality_cluster(item))
        size_list1, p_list1 = _func_p_gen(cardinality_list)
        size_list2, p_list2 = _func_p_gen(cardinality_list[:-cut_num]) # 剪切大势超边
        try: x2, y2, a = _func_line_fit(size_list2, p_list2)
        except: x2, y2 = 0, 0
        plt.rcParams['font.sans-serif'] = 'Arial'
        plt.rcParams['font.size'] = 14
        axes = plt.axes([0, 0, 1.6*0.35*0.7, 0.9*0.35])
        axes.set_xscale('log')
        axes.set_yscale('log')
        l = len([item for item in size_list1 if item < cardinality_list[-cut_num]])
        axes.scatter(size_list1[:l], p_list1[:l], marker = 'o', color = '#4091B2', s = 40)
        axes.scatter(size_list1[l:], p_list1[l:], marker = 's', color = '#FF7182', s = 40, label = 'Outliers')
        # axes.plot(x1, y1, linewidth = 4, linestyle = '--', color = '#FF7182', label = 'With outliers', alpha = 0.7)
        axes.plot(x2, y2, linewidth = 4, linestyle = '-', color = '#7FAA7C', label = 'Without outliers', alpha = 0.7)
        # plt.legend(fontsize = 20, ncols = 2, frameon = False, loc = 'upper right', bbox_to_anchor = (1, 3))
        plt.savefig('C:/Users/Lenovo/Desktop/1.cardinality_' + str(name) + '_' + str(round(float(a), 2)) + '.svg', bbox_inches = 'tight', pad_inches = 0.08)
        plt.clf()

def _func_flowdegree_distribution_plot(net_flow_list: list, mode: str, name: str):
    flow_, degree_, l = [], [], len(net_flow_list[0])
    temp_dict = {'r': ('#75fffc', 100), 'ba': ('#81c2ff', 100), 'ws': ('#6f71ff', 100)}
    e_c, ss = temp_dict[mode]
    for origin_flow in net_flow_list:
        for i in range(l):
            flow_.append(np.sum(origin_flow[:, i]) + np.sum(origin_flow[i, :]))
            count = 0
            for j in origin_flow[:, i]:
                if j != 0: count += 1
            for j in origin_flow[i, :]:
                if j != 0: count += 1
            degree_.append(count)
    print(np.max(flow_))
    plt.rcParams['font.sans-serif'] = 'Arial'
    fig = plt.figure()
    ax = fig.add_axes([0.1, 0.1, 0.6, 0.8])
    if mode == 'r':
        ax.set_xlim(0, 2.1)
        ax.set_ylim(0, 24)
    elif mode == 'ba':
        ax.set_xlim(0, 12)
        ax.set_ylim(0, 105)
    elif mode == 'ws':
        ax.set_xlim(0, 1.8)
        ax.set_ylim(0, 7.5)
    plt.xticks(fontsize = 20, rotation = 45) # urt, economic: rotation = 45
    plt.yticks(fontsize = 20)
    plt.xlabel('Flow', fontsize = 20)
    plt.ylabel('Degree', fontsize = 20)
    ax.scatter(flow_, degree_, s = 180, facecolor = 'None', edgecolors = e_c, alpha = 0.7)
    plt.savefig('C:/Users/Lenovo/Desktop/2.flowdegree_' + mode + name + '_fdc.svg', bbox_inches = 'tight', pad_inches = 0)
    plt.clf()

def _fig_flowdegree_distribution(data_path: str, mode: str):
    _, net_data_result = _func_artifical_data_process(data_path, mode)
    net1_data, net2_data, net3_data, net4_data = net_data_result[0:10], net_data_result[10:20], net_data_result[20:30], net_data_result[30:40]
    net1_flow, net2_flow, net3_flow, net4_flow = [item[0] for item in net1_data], [item[0] for item in net2_data], [item[0] for item in net3_data], [item[0] for item in net4_data]
    _func_flowdegree_distribution_plot(net1_flow, mode, '1')
    _func_flowdegree_distribution_plot(net2_flow, mode, '2')
    _func_flowdegree_distribution_plot(net3_flow, mode, '3')
    _func_flowdegree_distribution_plot(net4_flow, mode, '4')

def _func_hyperedge_read(hyperedge_dict: dict):
    node_list = hyperedge_dict.keys()
    hypergraph = xgi.Hypergraph()
    hypergraph.add_nodes_from(node_list)
    for id in node_list:
        hypergraph.add_edge(hyperedge_dict[id], id=id)
    return hypergraph

def _func_node_flow(matrix_flow: np.ndarray, node_list: list):
    result_list = []
    for i in range(len(node_list)):
        result_list.append(np.sum(matrix_flow[:, i]) + np.sum(matrix_flow[i, :]))
    # 节点流量越大，越容易被破坏
    result_list = 1 - np.array(result_list)/np.max(result_list) + 0.0001
    return sorted(zip(result_list/np.max(result_list), node_list), reverse=True)

def _fw_percolation_flow(hyperedge_dict: dict, matrix_flow: np.ndarray, node_list: list):
    result_list = []
    hypergraph = _func_hyperedge_read(hyperedge_dict)
    l = len(node_list)
    node_states = _func_node_flow(matrix_flow, node_list)
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
        else:
            result_list.append((q, temp_list2[1]/l, temp_list2[0]/l))
        q += 0.01
    return result_list, [item[1] for item in result_list].index(max([item[1] for item in result_list]))

def _fig_critical_percolation_threshold(data_path: str, mode: str):
    cascading_result, net_data_result = _func_artifical_data_process(data_path, mode)
    cas1, cas2, cas3, cas4, data1, data2, data3, data4 = cascading_result[0:10], cascading_result[10:20], cascading_result[20:30], cascading_result[30:40], net_data_result[0:10], net_data_result[10:20], net_data_result[20:30], net_data_result[30:40]
    re1, re2, re3, re4 = [], [], [], []
    for i in range(len(cas1)):
        _, re = _fw_percolation_flow(cas1[i], data1[i][0], data1[i][2])
        re1.append(re)
    for i in range(len(cas2)):
        _, re = _fw_percolation_flow(cas2[i], data2[i][0], data2[i][2])
        re2.append(re)
    for i in range(len(cas3)):
        _, re = _fw_percolation_flow(cas3[i], data3[i][0], data3[i][2])
        re3.append(re)
    for i in range(len(cas4)):
        _, re = _fw_percolation_flow(cas4[i], data4[i][0], data4[i][2])
        re4.append(re)
    x = list(range(1, 5))
    y = [sum(re1) / len(re1), sum(re2) / len(re2), sum(re3) / len(re3), sum(re4) / len(re4)]
    r_xtick = ['0.05', '0.10', '0.15', '0.20']
    ba_xtick = ['1', '2', '3', '4']
    plt.rcParams['font.sans-serif'] = 'Arial'
    plt.rcParams['font.size'] = 18
    axes = plt.axes([0, 0, 0.45, 0.9])
    axes.set_ylim(0, 45)
    plt.ylabel('$q_c$')
    if mode == 'r':
        axes.plot(x, y, color = '#75fffc', marker = 'o', markersize = 17)
        plt.xticks(x, r_xtick)
        plt.xlabel('r')
    elif mode == 'ba':
        axes.plot(x, y, color = '#81c2ff', marker = 'o', markersize = 17)
        plt.xticks(x, ba_xtick)
        plt.xlabel('m')
    elif mode == 'ws':
        axes.plot(x, y, color = '#6f71ff', marker = 'o', markersize = 17)
        plt.xticks(x, r_xtick)
        plt.xlabel('p')
    plt.savefig('C:/Users/Lenovo/Desktop/3.qc_' + str(mode) + '.svg', bbox_inches = 'tight', pad_inches = 0.08)
    plt.clf()
    return re1 + re2 + re3 + re4

def _func_after_percolation_hypergraph_matrix(hyperedge_dict: dict, matrix_flow: np.ndarray, node_list: list, qc, hypergraph_list: list):
    hypergraph = _func_hyperedge_read(hyperedge_dict)
    node_states = _func_node_flow(matrix_flow, node_list)
    for item in node_states:
        if item[0] <= qc * 0.01:
            hypergraph.remove_edge(item[1])
    hypergraph_matrix = xgi.incidence_matrix(hypergraph, sparse = False).T
    hypergraph_list.append(hypergraph_matrix)

def _func_hypergraph_node_edge_dict(hypergraph: np.ndarray, t: int):
    # 生成超图中节点、超边字典，并筛选超边势符合满足的index {index: [relationship]}
    node_dict, edge_dict, edge_filter_index_list = {}, {}, []
    for node_index in range(hypergraph.shape[1]): node_dict[node_index] = []
    for edge_index in range(hypergraph.shape[0]): edge_dict[edge_index] = []
    for node_index in range(hypergraph.shape[1]):
        for edge_index in range(hypergraph.shape[0]):
            if hypergraph[edge_index, node_index] == 1: node_dict[node_index].append(edge_index)
    for edge_index in range(hypergraph.shape[0]):
        for node_index in range(hypergraph.shape[1]):
            if hypergraph[edge_index, node_index] == 1: edge_dict[edge_index].append(node_index)
    for key in edge_dict.keys():
        l = len(edge_dict[key])
        if l <= t and l >= 2: edge_filter_index_list.append(key)
    return node_dict, edge_dict, edge_filter_index_list

def _func_mining_one(hypergraph: np.ndarray, name: str, u: int, t: int, result_list: list):
    # 挖掘某个超图
    result_dict, repeat_filter_list = {}, []
    for i in range(2, t + 1):
        for j in range(2, t + 1):
            if j >= i:
                for k in range(1, min(i, j) + 1): result_dict[(i, j, k)] = []
    node_dict, edge_dict, edge_filter_index_list = _func_hypergraph_node_edge_dict(hypergraph, t)
    lll = len(edge_filter_index_list)
    for kkk, edge_index in enumerate(edge_filter_index_list):
        print(name + '网络  当前挖掘随机超图数量: ' + str(len(result_list)) + '  进度: ' + str(round(float((kkk + 1) / lll * 100), 2)) + '%')
        repeat_filter_list.append(edge_index)
        temp_list, node_list = [], edge_dict[edge_index]
        for node in node_list: temp_list += node_dict[node]
        for item in list(set(temp_list) - {edge_index}):
            if item not in repeat_filter_list and item in edge_filter_index_list:
                node_set_1, node_set_2 = edge_dict[edge_index], edge_dict[item]
                l1, l2, l3 = len(node_set_1), len(node_set_2), len([x for x in node_set_1 if x in node_set_2])
                if l1 <= l2: result_dict[(l1, l2, l3)].append((tuple(node_set_1), tuple(node_set_2)))
                elif l2 <= l1: result_dict[(l2, l1, l3)].append((tuple(node_set_2), tuple(node_set_1)))
    result_list.append(result_dict)

def _func_hypermotifs_sta(data_path: str, mode: str, qc_list: list):
    cascading_result, net_data_result = _func_artifical_data_process(data_path, mode)
    hypergraph_list, hypermotifs_result_list = [], []
    for i in range(len(cascading_result)):
        _func_after_percolation_hypergraph_matrix(cascading_result[i], net_data_result[i][0], net_data_result[i][2], qc_list[i], hypergraph_list)
    for name, hypegraph in enumerate(hypergraph_list):
        _func_mining_one(hypegraph, str(name), 2, 4, hypermotifs_result_list)
    # with open('C:/Users/Lenovo/Desktop/' + mode + '_hypermotifs_sta.pkl', 'wb') as file:
    #     pickle.dump(hypermotifs_result_list, file)
    re1, re2, re3, re4 = {}, {}, {}, {}
    for key in hypermotifs_result_list[0].keys():
        re1[key] = 0
        re2[key] = 0
        re3[key] = 0
        re4[key] = 0
    for item in hypermotifs_result_list[0:10]:
        for key in item.keys(): re1[key] += len(item[key])
    for item in hypermotifs_result_list[10:20]:
        for key in item.keys(): re2[key] += len(item[key])
    for item in hypermotifs_result_list[20:30]:
        for key in item.keys(): re3[key] += len(item[key])
    for item in hypermotifs_result_list[30:40]:
        for key in item.keys(): re4[key] += len(item[key])
    with open('C:/Users/Lenovo/Desktop/' + mode + '_hypermotifs_sta.pkl', 'wb') as file:
        pickle.dump([re1, re2, re3, re4], file)
    print([re1, re2, re3, re4])

def artifical_plot_sum(data_path: str, mode: str):
    _fig_cardinality_distribution(data_path, mode)
    _fig_flowdegree_distribution(data_path, mode)
    qc_list = _fig_critical_percolation_threshold(data_path, mode)
    _func_hypermotifs_sta(data_path, mode, qc_list)

mode = 'ws'
data_path = 'C:/Users/Lenovo/Desktop/F/2024.07.30-流量加权网络崩溃过程中超模体的涌现/result_fig/r6.artifical_result/'
artifical_plot_sum(data_path, mode)
