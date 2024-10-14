import matplotlib.pyplot as plt
import numpy as np
import copy
import seaborn as sns
from os import listdir
from percolation import fw_percolation_flow
from percolation import cardinality_cluster
from datapackage import *

def func_p_gen(cardinality_list: list):
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

def func_line_fit(size_list: np.ndarray, p_list: list):
    lg_x, lg_y = np.log10(size_list), np.log10(np.array(p_list))
    a, b = np.polyfit(lg_x, lg_y, 1)
    # print(a)
    result_x, result_y = [], []
    fit_list = np.linspace(0, max(lg_x), 10)
    for i in fit_list:
        result_x.append(10**i)
        result_y.append(10**(a*i + b))
    return result_x, result_y, a

def func_eq_dict(origin_dict: dict, compare_dict: dict):
    big_result, small_result = 0, 0
    for key in origin_dict.keys():
        if origin_dict[key] > compare_dict[key]: small_result -= 1
        elif origin_dict[key] < compare_dict[key]: big_result += 1
        else: continue
    return big_result/len(origin_dict), small_result/len(origin_dict)

def func_degree_flow_correlation(origin_flow: np.ndarray, node_list: list, hyperedge_dict: dict, net_name: str):
    black_swan_node_list = []
    flow_, degree_, l, flow_b, degree_b = [], [], len(origin_flow), [], []
    temp_dict = {'social': ('#F05A56', 100), 'vote': ('#05BEFF', 100), 'urt': ('#7F7F7F', 100), 'economic': ('#BF9000', 100), 'ecowet': ('#34E076', 100), 'ecodry': ('#34E076', 100)}
    black_swan_node_dict = {'social': 977, 'vote': 215, 'urt': 317, 'economic': 487, 'ecowet': 128, 'ecodry': 128}
    for node in node_list:
        if len(hyperedge_dict[node]) >= black_swan_node_dict[net_name]: black_swan_node_list.append(node_list.index(node))
    e_c, ss = temp_dict[net_name]
    for i in range(l):
        if i not in black_swan_node_list:
            flow_.append(np.sum(origin_flow[:, i]) + np.sum(origin_flow[i, :]))
            count = 0
            for j in origin_flow[:, i]:
                if j != 0: count += 1
            for j in origin_flow[i, :]:
                if j != 0: count += 1
            degree_.append(count)
        else:
            flow_b.append(np.sum(origin_flow[:, i]) + np.sum(origin_flow[i, :]))
            count = 0
            for j in origin_flow[:, i]:
                if j != 0: count += 1
            for j in origin_flow[i, :]:
                if j != 0: count += 1
            degree_b.append(count)
    print(np.max(flow_))
    plt.rcParams['font.sans-serif'] = 'Arial'
    fig = plt.figure()
    ax = fig.add_axes([0.1, 0.1, 0.6, 0.8])
    plt.xticks(fontsize = 20, rotation = 45) # urt, economic: rotation = 45
    plt.yticks(fontsize = 20)
    plt.xlabel('Flow', fontsize = 20)
    plt.ylabel('Degree', fontsize = 20)
    ax.scatter(flow_, degree_, s = 180, facecolor = 'None', edgecolors = e_c, alpha = 0.7)
    ax.scatter(flow_b, degree_b, s = 180, facecolor = e_c, edgecolors = 'black', marker = '^')
    plt.savefig('D:/桌面/' + net_name + '_fdc.jpg', dpi = 2400, bbox_inches = 'tight', pad_inches = 0)
    plt.clf()

def fig_hyperedge_cardinality_p_distribution(hyperedge_dict: dict, name: str, linefit_list = []):
    dict_value = hyperedge_dict.values()
    cardinality_list = []
    for i in dict_value:
        cardinality_list.append(len(i))
    cardinality_list.sort(reverse=False)
    # print(cardinality_list)
    cut_num = len(cardinality_list) - cardinality_list.index(cardinality_cluster(hyperedge_dict))
    # print(len([item for item in cardinality_list if item >= 15]))
    size_list1, p_list1 = func_p_gen(cardinality_list)
    size_list2, p_list2 = func_p_gen(cardinality_list[:-cut_num]) # 剪切大势超边
    # try: x1, y1 = func_line_fit(size_list1, p_list1)
    # except: x1, y1 = 0, 0
    try: x2, y2, a = func_line_fit(size_list2, p_list2)
    except: x2, y2 = 0, 0
    plt.rcParams['font.sans-serif'] = 'Arial'
    plt.rcParams['font.size'] = 14
    axes = plt.axes([0, 0, 1.6*0.35*0.7, 0.9*0.2]) # fig2-0.35
    axes.set_xscale('log')
    axes.set_yscale('log')
    # axes.scatter(size_list1, p_list1, marker = 'o', color = '#4091B2', s = 40)
    l = len([item for item in size_list1 if item < cardinality_list[-cut_num]])
    axes.scatter(size_list1[:l], p_list1[:l], marker = 'o', color = '#4091B2', s = 40)
    axes.scatter(size_list1[l:], p_list1[l:], marker = 's', color = '#FF7182', s = 40, label = 'Outliers')
    # axes.plot(x1, y1, linewidth = 4, linestyle = '--', color = '#FF7182', label = 'With outliers', alpha = 0.7)
    axes.plot(x2, y2, linewidth = 4, linestyle = '-', color = '#7FAA7C', label = 'Without outliers', alpha = 0.7)
    # plt.legend(fontsize = 20, ncols = 2, frameon = False, loc = 'upper right', bbox_to_anchor = (1, 3))
    # plt.savefig('D:/桌面/F/2023.05.25-流量加权网络崩溃过程中超模体的涌现/result_fig/fig_1_result_SOCIAL/' + name + '.jpg', dpi = 2400, bbox_inches = 'tight', pad_inches = 0)
    plt.savefig(r'D:\桌面\F\2023.05.25-流量加权网络崩溃过程中超模体的涌现\result_fig\r8.k_exp\ECOWET_fig/' + name + '_' + str(round(float(a), 2)) + '.svg', bbox_inches = 'tight', pad_inches = 0.08)
    plt.clf()

def fig_percolation_transition(result_list: list, file_name: str):
    x, y1, y2 = [], [], []
    for item in result_list:
        x.append(item[0])
        y1.append(item[1])
        y2.append(item[2])
    # print(y1.index(max(y1)))
    plt.rcParams['font.sans-serif'] = 'Arial'
    plt.rcParams['font.size'] = 17
    ax1 = plt.axes((0, 0, 2*0.25, 1.5*0.4))
    # ax1.set_ylim(-0.05, 1.05)
    line1, = ax1.plot(x, y2, color = '#37A0AB', marker = 'o', markersize = 10, label = '$G$', markerfacecolor = 'none')
    ax1.set_xlabel('$q$')
    ax1.set_ylabel('$G$')
    ax1.tick_params(axis='both', size = 0, width = 0)
    ax2 = ax1.twinx()
    # ax2.set_ylim(-0.05, 1.05)
    line2, = ax2.plot(x, y1, color = '#DAB36C', marker = 's', markersize = 10, label = '$SG$', markerfacecolor = 'none')
    ax2.set_ylabel('$SG$')
    ax2.tick_params(axis='y', size = 0, width = 0)
    plt.legend([line1, line2], ['$G$', '$SG$'], loc = 'upper right', frameon = False, ncol = 2, bbox_to_anchor = (0.85, 1.2))
    plt.savefig('D:/桌面/' + str(file_name) + '_perco_' + str(y1.index(max(y1))) + '.svg', bbox_inches = 'tight', pad_inches = 0.1)
    plt.clf()

def fig_para_analysis_main(network_type: str):
    social = np.array([
        [0.99, 0.85, 0.99, 0.99, 0.99],
        [0.99, 0.01, 0.99, 0.99, 0.91],
        [0.95, 0.01, 0.95, 0.95, 0.90],
        [0.76, 0.01, 0.01, 0.01, 0.64],
        [0.49, 0.01, 0.01, 0.01, 0.01],
        [0.01, 0.01, 0.01, 0.01, 0.01],
        [0.01, 0.01, 0.01, 0.01, 0.01]
    ])
    vote = np.array([
        [0.98, 0.01, 0.98, 0.98, 0.98],
        [0.98, 0.01, 0.92, 0.98, 0.98],
        [0.86, 0.01, 0.86, 0.84, 0.86],
        [0.80, 0.01, 0.80, 0.80, 0.77],
        [0.25, 0.01, 0.01, 0.21, 0.25],
        [0.25, 0.01, 0.01, 0.09, 0.19],
        [0.01, 0.01, 0.01, 0.01, 0.01]
    ])
    urt = np.array([
        [0.83, 0.01, 0.82, 0.82, 0.79],
        [0.83, 0.01, 0.82, 0.82, 0.71],
        [0.83, 0.01, 0.63, 0.82, 0.67],
        [0.63, 0.01, 0.62, 0.63, 0.48],
        [0.62, 0.01, 0.62, 0.62, 0.33],
        [0.16, 0.01, 0.01, 0.16, 0.13],
        [0.16, 0.01, 0.01, 0.16, 0.13]
    ])
    economic = np.array([
        [0.99, 0.99, 0.99, 0.98, 0.99],
        [0.99, 0.99, 0.99, 0.98, 0.99],
        [0.98, 0.01, 0.98, 0.98, 0.88],
        [0.97, 0.01, 0.97, 0.97, 0.75],
        [0.64, 0.01, 0.01, 0.01, 0.64],
        [0.01, 0.01, 0.01, 0.01, 0.01],
        [0.01, 0.01, 0.01, 0.01, 0.01]
    ])
    ecowet = np.array([
        [0.99, 0.99, 0.99, 0.88, 0.98],
        [0.97, 0.01, 0.97, 0.72, 0.90],
        [0.72, 0.01, 0.01, 0.53, 0.64],
        [0.52, 0.01, 0.01, 0.52, 0.48],
        [0.52, 0.01, 0.01, 0.52, 0.48],
        [0.37, 0.01, 0.01, 0.37, 0.26],
        [0.01, 0.01, 0.01, 0.01, 0.01]
    ])
    ecodry = np.array([
        [0.98, 0.98, 0.98, 0.95, 0.98],
        [0.75, 0.01, 0.01, 0.75, 0.76],
        [0.75, 0.01, 0.01, 0.75, 0.74],
        [0.69, 0.01, 0.01, 0.49, 0.62],
        [0.49, 0.01, 0.01, 0.49, 0.48],
        [0.38, 0.01, 0.01, 0.38, 0.31],
        [0.01, 0.01, 0.01, 0.01, 0.01]
    ])
    plt.rcParams['font.sans-serif'] = 'Arial'
    plt.figure(figsize=(3.4, 5))
    if network_type == 'social':
        sns.heatmap(social, annot=False, cmap='Blues', xticklabels=['O', 'C', 'F', 'D', 'Rd'], yticklabels=['2.45', '2.20', '1.95', '1.70', '1.45', '1.20', '0.95'], linewidths=1.5, vmin=-0.01, vmax=1.01, cbar=True)
    elif network_type == 'vote':
        sns.heatmap(vote, annot=False, cmap='Blues', xticklabels=['O', 'C', 'F', 'D', 'Rd'], yticklabels=['2.28', '2.03', '1.78', '1.53', '1.28', '1.03', '0.78'], linewidths=1.5, vmin=-0.01, vmax=1.01, cbar=True)
    elif network_type == 'urt':
        sns.heatmap(urt, annot=False, cmap='Blues', xticklabels=['O', 'C', 'F', 'D', 'Rd'], yticklabels=['4.50', '4.25', '4.00', '3.75', '3.50', '3.25', '3.00'], linewidths=1.5, vmin=-0.01, vmax=1.01, cbar=True)
    elif network_type == 'economic':
        sns.heatmap(economic, annot=False, cmap='Blues', xticklabels=['O', 'C', 'F', 'D', 'Rd'], yticklabels=['2.74', '2.49', '2.24', '1.99', '1.74', '1.49', '1.24'], linewidths=1.5, vmin=-0.01, vmax=1.01, cbar=True)
    elif network_type == 'ecowet':
        sns.heatmap(ecowet, annot=False, cmap='Blues', xticklabels=['O', 'C', 'F', 'D', 'Rd'], yticklabels=['2.50', '2.25', '2.00', '1.75', '1.50', '1.25', '1.00'], linewidths=1.5, vmin=-0.01, vmax=1.01, cbar=True)
    elif network_type == 'ecodry':
        sns.heatmap(ecodry, annot=False, cmap='Blues', xticklabels=['O', 'C', 'F', 'D', 'Rd'], yticklabels=['2.50', '2.25', '2.00', '1.75', '1.50', '1.25', '1.00'], linewidths=1.5, vmin=-0.01, vmax=1.01, cbar=True)
    plt.savefig('D:/桌面/' + network_type + '_heatmap.jpg', dpi = 2400, bbox_inches = 'tight', pad_inches = 0)
    plt.clf()

def fig_para_analysis(network_type: str):
    social_origin = np.array([
        [0.99, 0.99, 0.99, 0.99],
        [0.98, 0.99, 0.99, 0.99],
        [0.95, 0.95, 0.95, 0.95],
        [0.76, 0.76, 0.76, 0.76],
        [0.49, 0.49, 0.49, 0.35],
        [0.01, 0.01, 0.01, 0.01],
        [0.01, 0.01, 0.01, 0.01]
    ])
    social_cml = np.array([
        [0.85, 0.85, 0.85, 0.85],
        [0.01, 0.01, 0.01, 0.01],
        [0.01, 0.01, 0.01, 0.01],
        [0.01, 0.01, 0.01, 0.01],
        [0.01, 0.01, 0.01, 0.01],
        [0.01, 0.01, 0.01, 0.01],
        [0.01, 0.01, 0.01, 0.01]
    ])
    social_flow = np.array([
        [0.99, 0.99, 0.99, 0.99],
        [0.98, 0.99, 0.99, 0.99],
        [0.95, 0.95, 0.95, 0.95],
        [0.01, 0.01, 0.01, 0.01],
        [0.01, 0.01, 0.01, 0.01],
        [0.01, 0.01, 0.01, 0.01],
        [0.01, 0.01, 0.01, 0.01]
    ])
    social_degree = np.array([
        [0.99, 0.99, 0.99, 0.99],
        [0.98, 0.99, 0.99, 0.99],
        [0.95, 0.95, 0.95, 0.95],
        [0.01, 0.01, 0.01, 0.01],
        [0.01, 0.01, 0.01, 0.01],
        [0.01, 0.01, 0.01, 0.01],
        [0.01, 0.01, 0.01, 0.01]
    ])
    vote_origin = np.array([
        [0.98, 0.98, 0.98, 0.98],
        [0.98, 0.98, 0.98, 0.98],
        [0.86, 0.86, 0.86, 0.86],
        [0.80, 0.80, 0.80, 0.86],
        [0.25, 0.25, 0.25, 0.25],
        [0.25, 0.25, 0.25, 0.25],
        [0.01, 0.01, 0.01, 0.01]
    ])
    vote_cml = np.array([
        [0.01, 0.01, 0.01, 0.01],
        [0.01, 0.01, 0.01, 0.01],
        [0.01, 0.01, 0.01, 0.01],
        [0.01, 0.01, 0.01, 0.01],
        [0.01, 0.01, 0.01, 0.01],
        [0.01, 0.01, 0.01, 0.01],
        [0.01, 0.01, 0.01, 0.01]
    ])
    vote_flow = np.array([
        [0.98, 0.98, 0.98, 0.98],
        [0.98, 0.92, 0.92, 0.92],
        [0.80, 0.86, 0.86, 0.86],
        [0.80, 0.80, 0.80, 0.86],
        [0.01, 0.01, 0.01, 0.01],
        [0.01, 0.01, 0.01, 0.01],
        [0.01, 0.01, 0.01, 0.01]
    ])
    vote_degree = np.array([
        [0.98, 0.98, 0.98, 0.98],
        [0.98, 0.98, 0.98, 0.98],
        [0.80, 0.84, 0.84, 0.84],
        [0.80, 0.80, 0.80, 0.80],
        [0.21, 0.21, 0.21, 0.21],
        [0.09, 0.09, 0.09, 0.09],
        [0.01, 0.01, 0.01, 0.01]
    ])
    transportation_origin = np.array([
        [0.83, 0.83, 0.83, 0.83],
        [0.83, 0.83, 0.83, 0.83],
        [0.83, 0.83, 0.83, 0.83],
        [0.82, 0.83, 0.63, 0.64],
        [0.62, 0.62, 0.62, 0.62],
        [0.62, 0.62, 0.16, 0.62],
        [0.16, 0.16, 0.16, 0.62]
    ])
    transportation_cml = np.array([
        [0.01, 0.01, 0.01, 0.01],
        [0.01, 0.01, 0.01, 0.01],
        [0.01, 0.01, 0.01, 0.01],
        [0.01, 0.01, 0.01, 0.01],
        [0.01, 0.01, 0.01, 0.01],
        [0.01, 0.01, 0.01, 0.01],
        [0.01, 0.01, 0.01, 0.01]
    ])
    transportation_flow = np.array([
        [0.82, 0.82, 0.82, 0.82],
        [0.82, 0.82, 0.82, 0.82],
        [0.82, 0.82, 0.63, 0.63],
        [0.82, 0.82, 0.62, 0.63],
        [0.62, 0.62, 0.62, 0.62],
        [0.01, 0.62, 0.01, 0.62],
        [0.01, 0.01, 0.01, 0.62]
    ])
    transportation_degree = np.array([
        [0.82, 0.82, 0.82, 0.82],
        [0.82, 0.82, 0.82, 0.82],
        [0.82, 0.82, 0.82, 0.82],
        [0.82, 0.82, 0.63, 0.63],
        [0.62, 0.62, 0.62, 0.62],
        [0.62, 0.62, 0.16, 0.62],
        [0.16, 0.16, 0.16, 0.62]
    ])
    economic_origin = np.array([
        [0.99, 0.99, 0.99, 0.99],
        [0.99, 0.99, 0.99, 0.99],
        [0.98, 0.98, 0.98, 0.98],
        [0.97, 0.97, 0.97, 0.97],
        [0.88, 0.64, 0.64, 0.64],
        [0.01, 0.01, 0.01, 0.01],
        [0.01, 0.01, 0.01, 0.01]
    ])
    economic_cml = np.array([
        [0.99, 0.99, 0.99, 0.99],
        [0.99, 0.99, 0.99, 0.99],
        [0.01, 0.97, 0.01, 0.01],
        [0.01, 0.01, 0.01, 0.01],
        [0.01, 0.01, 0.01, 0.01],
        [0.01, 0.01, 0.01, 0.01],
        [0.01, 0.01, 0.01, 0.01]
    ])
    economic_flow = np.array([
        [0.99, 0.99, 0.99, 0.99],
        [0.99, 0.99, 0.99, 0.99],
        [0.98, 0.98, 0.98, 0.98],
        [0.97, 0.97, 0.97, 0.97],
        [0.01, 0.01, 0.01, 0.01],
        [0.01, 0.01, 0.01, 0.01],
        [0.01, 0.01, 0.01, 0.01]
    ])
    economic_degree = np.array([
        [0.98, 0.98, 0.98, 0.98],
        [0.98, 0.98, 0.98, 0.98],
        [0.98, 0.98, 0.98, 0.98],
        [0.97, 0.97, 0.97, 0.97],
        [0.88, 0.01, 0.01, 0.01],
        [0.01, 0.01, 0.01, 0.01],
        [0.01, 0.01, 0.01, 0.01]
    ])
    wet_origin = np.array([
        [0.99, 0.99, 0.99, 0.99],
        [0.97, 0.97, 0.97, 0.97],
        [0.72, 0.72, 0.72, 0.72],
        [0.52, 0.52, 0.52, 0.52],
        [0.52, 0.52, 0.52, 0.52],
        [0.37, 0.37, 0.37, 0.37],
        [0.01, 0.01, 0.01, 0.01]
    ])
    wet_cml = np.array([
        [0.99, 0.99, 0.99, 0.99],
        [0.01, 0.01, 0.01, 0.01],
        [0.01, 0.01, 0.01, 0.01],
        [0.01, 0.01, 0.01, 0.01],
        [0.01, 0.01, 0.01, 0.01],
        [0.01, 0.01, 0.01, 0.01],
        [0.01, 0.01, 0.01, 0.01]
    ])
    wet_flow = np.array([
        [0.99, 0.99, 0.99, 0.99],
        [0.97, 0.97, 0.97, 0.97],
        [0.01, 0.01, 0.01, 0.01],
        [0.01, 0.01, 0.01, 0.01],
        [0.01, 0.01, 0.01, 0.01],
        [0.01, 0.01, 0.01, 0.01],
        [0.01, 0.01, 0.01, 0.01]
    ])
    wet_degree = np.array([
        [0.88, 0.88, 0.88, 0.88],
        [0.72, 0.72, 0.72, 0.72],
        [0.53, 0.53, 0.53, 0.53],
        [0.52, 0.52, 0.52, 0.52],
        [0.52, 0.52, 0.52, 0.52],
        [0.01, 0.01, 0.01, 0.01],
        [0.01, 0.01, 0.01, 0.01]
    ])
    dry_origin = np.array([
        [0.98, 0.98, 0.98, 0.98],
        [0.75, 0.75, 0.75, 0.75],
        [0.75, 0.75, 0.75, 0.75],
        [0.69, 0.69, 0.69, 0.69],
        [0.49, 0.49, 0.49, 0.49],
        [0.38, 0.38, 0.38, 0.38],
        [0.01, 0.01, 0.01, 0.01]
    ])
    dry_cml = np.array([
        [0.98, 0.98, 0.98, 0.98],
        [0.01, 0.01, 0.01, 0.01],
        [0.01, 0.01, 0.01, 0.01],
        [0.01, 0.01, 0.01, 0.01],
        [0.01, 0.01, 0.01, 0.01],
        [0.01, 0.01, 0.01, 0.01],
        [0.01, 0.01, 0.01, 0.01]
    ])
    dry_flow = np.array([
        [0.98, 0.98, 0.98, 0.98],
        [0.01, 0.01, 0.01, 0.01],
        [0.01, 0.01, 0.01, 0.01],
        [0.01, 0.01, 0.01, 0.01],
        [0.01, 0.01, 0.01, 0.01],
        [0.01, 0.01, 0.01, 0.01],
        [0.01, 0.01, 0.01, 0.01]
    ])
    dry_degree = np.array([
        [0.95, 0.95, 0.95, 0.95],
        [0.75, 0.75, 0.75, 0.75],
        [0.75, 0.75, 0.75, 0.75],
        [0.49, 0.49, 0.49, 0.49],
        [0.49, 0.49, 0.49, 0.49],
        [0.38, 0.38, 0.38, 0.38],
        [0.01, 0.01, 0.01, 0.01]
    ])

    plt.rcParams['font.sans-serif'] = 'Arial'
    plt.figure(figsize=(3.4, 5))
    if network_type == 'transportation_origin':
        sns.heatmap(transportation_origin, annot=True, cmap='Blues', xticklabels=['3', '5', '7', '9'], yticklabels=['4.50', '4.25', '4.00', '3.75', '3.50', '3.25', '3.00'], linewidths=1.5, vmin=-0.01, vmax=1.01, cbar=True)
    elif network_type == 'transportation_cml':
        sns.heatmap(transportation_cml, annot=True, cmap='Blues', xticklabels=['3', '5', '7', '9'], yticklabels=['4.50', '4.25', '4.00', '3.75', '3.50', '3.25', '3.00'], linewidths=1.5, vmin=-0.01, vmax=1.01, cbar=True)
    elif network_type == 'transportation_flow':
        sns.heatmap(transportation_flow, annot=True, cmap='Blues', xticklabels=['3', '5', '7', '9'], yticklabels=['4.50', '4.25', '4.00', '3.75', '3.50', '3.25', '3.00'], linewidths=1.5, vmin=-0.01, vmax=1.01, cbar=True)
    elif network_type == 'transportation_degree':
        sns.heatmap(transportation_degree, annot=True, cmap='Blues', xticklabels=['3', '5', '7', '9'], yticklabels=['4.50', '4.25', '4.00', '3.75', '3.50', '3.25', '3.00'], linewidths=1.5, vmin=-0.01, vmax=1.01, cbar=True)
    elif network_type == 'social_origin':
        sns.heatmap(social_origin, annot=True, cmap='Blues', xticklabels=['3', '5', '7', '9'], yticklabels=['2.45', '2.20', '1.95', '1.70', '1.45', '1.20', '0.95'], linewidths=1.5, vmin=-0.01, vmax=1.01, cbar=True)
    elif network_type == 'social_cml':
        sns.heatmap(social_cml, annot=True, cmap='Blues', xticklabels=['3', '5', '7', '9'], yticklabels=['2.45', '2.20', '1.95', '1.70', '1.45', '1.20', '0.95'], linewidths=1.5, vmin=-0.01, vmax=1.01, cbar=True)
    elif network_type == 'social_flow':
        sns.heatmap(social_flow, annot=True, cmap='Blues', xticklabels=['3', '5', '7', '9'], yticklabels=['2.45', '2.20', '1.95', '1.70', '1.45', '1.20', '0.95'], linewidths=1.5, vmin=-0.01, vmax=1.01, cbar=True)
    elif network_type == 'social_degree':
        sns.heatmap(social_degree, annot=True, cmap='Blues', xticklabels=['3', '5', '7', '9'], yticklabels=['2.45', '2.20', '1.95', '1.70', '1.45', '1.20', '0.95'], linewidths=1.5, vmin=-0.01, vmax=1.01, cbar=True)
    elif network_type == 'vote_origin':
        sns.heatmap(vote_origin, annot=True, cmap='Blues', xticklabels=['3', '5', '7', '9'], yticklabels=['2.28', '2.03', '1.78', '1.53', '1.28', '1.03', '0.78'], linewidths=1.5, vmin=-0.01, vmax=1.01, cbar=True)
    elif network_type == 'vote_cml':
        sns.heatmap(vote_cml, annot=True, cmap='Blues', xticklabels=['3', '5', '7', '9'], yticklabels=['2.28', '2.03', '1.78', '1.53', '1.28', '1.03', '0.78'], linewidths=1.5, vmin=-0.01, vmax=1.01, cbar=True)
    elif network_type == 'vote_flow':
        sns.heatmap(vote_flow, annot=True, cmap='Blues', xticklabels=['3', '5', '7', '9'], yticklabels=['2.28', '2.03', '1.78', '1.53', '1.28', '1.03', '0.78'], linewidths=1.5, vmin=-0.01, vmax=1.01, cbar=True)
    elif network_type == 'vote_degree':
        sns.heatmap(vote_degree, annot=True, cmap='Blues', xticklabels=['3', '5', '7', '9'], yticklabels=['2.28', '2.03', '1.78', '1.53', '1.28', '1.03', '0.78'], linewidths=1.5, vmin=-0.01, vmax=1.01, cbar=True)
    elif network_type == 'economic_origin':
        sns.heatmap(economic_origin, annot=True, cmap='Blues', xticklabels=['3', '5', '7', '9'], yticklabels=['2.74', '2.49', '2.24', '1.99', '1.74', '1.49', '1.24'], linewidths=1.5, vmin=-0.01, vmax=1.01, cbar=True)
    elif network_type == 'economic_cml':
        sns.heatmap(economic_cml, annot=True, cmap='Blues', xticklabels=['3', '5', '7', '9'], yticklabels=['2.74', '2.49', '2.24', '1.99', '1.74', '1.49', '1.24'], linewidths=1.5, vmin=-0.01, vmax=1.01, cbar=True)
    elif network_type == 'economic_flow':
        sns.heatmap(economic_flow, annot=True, cmap='Blues', xticklabels=['3', '5', '7', '9'], yticklabels=['2.74', '2.49', '2.24', '1.99', '1.74', '1.49', '1.24'], linewidths=1.5, vmin=-0.01, vmax=1.01, cbar=True)
    elif network_type == 'economic_degree':
        sns.heatmap(economic_degree, annot=True, cmap='Blues', xticklabels=['3', '5', '7', '9'], yticklabels=['2.74', '2.49', '2.24', '1.99', '1.74', '1.49', '1.24'], linewidths=1.5, vmin=-0.01, vmax=1.01, cbar=True)
    elif network_type == 'wet_origin':
        sns.heatmap(wet_origin, annot=True, cmap='Blues', xticklabels=['3', '5', '7', '9'], yticklabels=['2.50', '2.25', '2.00', '1.75', '1.50', '1.25', '1.00'], linewidths=1.5, vmin=-0.01, vmax=1.01, cbar=True)
    elif network_type == 'wet_cml':
        sns.heatmap(wet_cml, annot=True, cmap='Blues', xticklabels=['3', '5', '7', '9'], yticklabels=['2.50', '2.25', '2.00', '1.75', '1.50', '1.25', '1.00'], linewidths=1.5, vmin=-0.01, vmax=1.01, cbar=True)
    elif network_type == 'wet_flow':
        sns.heatmap(wet_flow, annot=True, cmap='Blues', xticklabels=['3', '5', '7', '9'], yticklabels=['2.50', '2.25', '2.00', '1.75', '1.50', '1.25', '1.00'], linewidths=1.5, vmin=-0.01, vmax=1.01, cbar=True)
    elif network_type == 'wet_degree':
        sns.heatmap(wet_degree, annot=True, cmap='Blues', xticklabels=['3', '5', '7', '9'], yticklabels=['2.50', '2.25', '2.00', '1.75', '1.50', '1.25', '1.00'], linewidths=1.5, vmin=-0.01, vmax=1.01, cbar=True)
    elif network_type == 'dry_origin':
        sns.heatmap(dry_origin, annot=True, cmap='Blues', xticklabels=['3', '5', '7', '9'], yticklabels=['2.50', '2.25', '2.00', '1.75', '1.50', '1.25', '1.00'], linewidths=1.5, vmin=-0.01, vmax=1.01, cbar=True)
    elif network_type == 'dry_cml':
        sns.heatmap(dry_cml, annot=True, cmap='Blues', xticklabels=['3', '5', '7', '9'], yticklabels=['2.50', '2.25', '2.00', '1.75', '1.50', '1.25', '1.00'], linewidths=1.5, vmin=-0.01, vmax=1.01, cbar=True)
    elif network_type == 'dry_flow':
        sns.heatmap(dry_flow, annot=True, cmap='Blues', xticklabels=['3', '5', '7', '9'], yticklabels=['2.50', '2.25', '2.00', '1.75', '1.50', '1.25', '1.00'], linewidths=1.5, vmin=-0.01, vmax=1.01, cbar=True)
    elif network_type == 'dry_degree':
        sns.heatmap(dry_degree, annot=True, cmap='Blues', xticklabels=['3', '5', '7', '9'], yticklabels=['2.50', '2.25', '2.00', '1.75', '1.50', '1.25', '1.00'], linewidths=1.5, vmin=-0.01, vmax=1.01, cbar=True)
    
    plt.savefig('D:/桌面/' + network_type + '_heatmap.jpg', dpi = 1200, bbox_inches = 'tight', pad_inches = 0)

def fig_cluster_power_law(qc_list: list, result_list: list, save_path: str, save_name: str):
    for item in result_list:
        file_name = str(round(item[0], 2))
        if len(item[1]) >= 2 and file_name in qc_list:
            size_list = np.unique(np.array(item[1]))
            p_list, l = [], len(item[1])
            for size in size_list:
                c = 0
                for i in item[1]:
                    if size == i:
                        c += 1
                p_list.append(c/l)
            list_zip = list(zip(p_list, size_list))
            sorted(list_zip, reverse=True)
            x, y = [], []
            for i in list_zip:
                y.append(i[0])
                x.append(i[1])
            print(file_name)
            line_x, line_y = func_line_fit(size_list, p_list)
            plt.rcParams['font.sans-serif'] = 'Arial'
            plt.xticks(fontsize = 20)
            plt.yticks(fontsize = 20)
            plt.xscale('log')
            plt.yscale('log')
            if file_name == qc_list[0]:
                plt.scatter(x, y, edgecolors='#C365A3', marker='s', color = 'white', s = 90, linewidths = 2.5, alpha=0.8)
                plt.plot(line_x, line_y, color = '#2A97D5', linewidth = 4, alpha = 0.8, linestyle = '-')
            if file_name == qc_list[1]:
                plt.scatter(x, y, edgecolors='#C7D885', marker='o', color = 'white', s = 90, linewidths = 2.5, alpha=0.8)
            if file_name == qc_list[2]:
                plt.scatter(x, y, edgecolors='#4E2A82', marker='^', color = 'white', s = 90, linewidths = 2.5, alpha=0.8)
                plt.plot(line_x, line_y, color = '#2A97D5', linewidth = 4, alpha = 0.8, linestyle = '--')
    plt.savefig(save_path + save_name + '.jpg', dpi = 1200, bbox_inches = 'tight', pad_inches = 0)
    # plt.clf()

def fig_hypermotifs_sta():
    data = [[11/504510, 4/504510, 13/504510, 0, 4/504510, 3/504510, 1/504510, 1/504510, 0, 2/504510, 0, 0, 0, 0, 0, 0],
            [0, 1/23871, 0, 0, 1/23871, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [2/118828, 3/118828, 4/118828, 0, 4/118828, 3/118828, 0, 0, 0, 0, 0, 1/118828, 1/118828, 0, 0, 0],
            [11/50086, 0, 9/50086, 2/50086, 2/50086, 2/50086, 0, 2/50086, 0, 1/50086, 1/50086, 0, 1/50086, 0, 0, 0],
            [0, 0, 1/8128, 0, 2/8128, 0, 0, 0, 0, 1/8128, 0, 0, 0, 0, 0, 0],
            [1/8128, 0, 0, 0, 2/8128, 1/8128, 0, 0, 0, 1/8128, 1/8128, 0, 0, 1/8128, 0, 0]]
    # data = [[2.480, 1.605, 2.634, 0, 1.605, 1.383, 0.691, 0.691, 0, 1.095, 0, 0, 0, 0, 0, 0],
    #         [0, 1.717, 0, 0, 1.717, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    #         [3.575, 0, 3.381, 1.989, 1.989, 1.989, 0, 1.989, 0, 1.424, 1.424, 0, 1.424, 0, 0, 0],
    #         [1.629, 1.967, 2.219, 0, 2.219, 1.967, 0, 0, 0, 0, 0, 1.115, 1.115, 0, 0, 0],
    #         [0, 0, 2.176, 0, 2.811, 0, 0, 0, 0, 2.176, 0, 0, 0, 0, 0, 0],
    #         [2.176, 0, 0, 0, 2.811, 2.176, 0, 0, 0, 2.176, 2.176, 0, 0, 2.176, 0, 0]]
    # data = [[11, 4, 13, 0, 4, 3, 1, 1, 0, 2, 0, 0, 0, 0, 0, 0],
    #         [0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    #         [2, 3, 4, 0, 4, 3, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0],
    #         [11, 0, 9, 2, 2, 2, 0, 2, 0, 1, 1, 0, 1, 0, 0, 0],
    #         [0, 0, 1, 0, 2, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
    #         [1, 0, 0, 0, 2, 1, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0]]
    mask = np.array([[False, False, False, True, False, False, False, False, True, False, True, True, True, True, True, True],
            [True, False, True, True, False, True, True, True, True, True, True, True, True, True, True, True],
            [False, False, False, True, False, False, True, True, True, True, True, False, False, True, True, True],
            [False, True, False, False, False, False, True, False, True, False, False, True, False, True, True, True],
            [True, True, False, True, False, True, True, True, True, False, True, True, True, True, True, True],
            [False, True, True, True, False, False, True, True, True, False, False, True, True, False, True, True]])
    data = np.array(data)
    xtic = []
    for i in range(16): xtic.append(' ')
    plt.rcParams['font.sans-serif'] = 'Arial'
    plt.rcParams['font.size'] = 20
    plt.figure(figsize=(16, 5))
    sns.heatmap(data, annot=False, cmap='GnBu', xticklabels = xtic, yticklabels=False, linewidths=1.5, cbar=True, center = np.mean(data), mask=mask) #cmap='GnBu'  cmap='YlOrBr'
    plt.savefig('D:/桌面/hypermotifs_sta.jpg', dpi = 1200, bbox_inches = 'tight', pad_inches = 0)

def fig_ci_distribution(ci_list: list):
    y_list = []
    for item in ci_list:
        y_list.append(item[0])
    x_list = list(range(len(y_list)))
    plt.rcParams['font.sans-serif'] = 'Arial'
    plt.xticks(fontsize = 20)
    plt.yticks(fontsize = 20)
    plt.scatter(x_list, y_list, marker = 'o', color = '#008671', s = 40)
    plt.savefig('D:/桌面/ci.jpg', dpi = 2400, bbox_inches = 'tight', pad_inches = 0)
    plt.clf()
    print('Done!')

def fig_average_size_enhance():
    mode_name_list = ['', '_enhance/cml', '_enhance/flow', '_enhance/degree']
    mm_list = ['', '_enhance', '_enhance', '_enhance']
    data_list = []
    for i in range(4):
        with open('D:/桌面/F/2023.05.25-流量加权网络崩溃过程中超模体的涌现/result_fig/fig_1_result_SOCIAL' + str(mode_name_list[i]) + '/k=7_r=1.75' + str(mm_list[i]) + '.txt', mode = 'r+', encoding = 'UTF-8') as file_1:
            meta_data_social = eval(file_1.read())
            data_list.append((1005, mode_name_list[i], 'social', sum([len(item) for item in list(meta_data_social.values())])/1005))
        with open('D:/桌面/F/2023.05.25-流量加权网络崩溃过程中超模体的涌现/result_fig/fig_1_result_VOTE' + str(mode_name_list[i]) + '/k=7_r=1.75' + str(mm_list[i]) + '.txt', mode = 'r+', encoding = 'UTF-8') as file_2:
            meta_data_vote = eval(file_2.read())
            data_list.append((219, mode_name_list[i], 'vote', sum([len(item) for item in list(meta_data_vote.values())])/219))
        with open('D:/桌面/F/2023.05.25-流量加权网络崩溃过程中超模体的涌现/result_fig/fig_1_result_ECONOMIC' + str(mode_name_list[i]) + '/k=7_r=1.75' + str(mm_list[i]) + '.txt', mode = 'r+', encoding = 'UTF-8') as file_4:
            meta_data_economic = eval(file_4.read())
            data_list.append((488, mode_name_list[i], 'economic', sum([len(item) for item in list(meta_data_economic.values())])/488))
        with open('D:/桌面/F/2023.05.25-流量加权网络崩溃过程中超模体的涌现/result_fig/fig_1_result_URT' + str(mode_name_list[i]) + '/k=7_r=3.75' + str(mm_list[i]) + '.txt', mode = 'r+', encoding = 'UTF-8') as file_3:
            meta_data_urt = eval(file_3.read())
            data_list.append((317, mode_name_list[i], 'urt', sum([len(item) for item in list(meta_data_urt.values())])/317))
        with open('D:/桌面/F/2023.05.25-流量加权网络崩溃过程中超模体的涌现/result_fig/fig_1_result_ECOWET' + str(mode_name_list[i]) + '/k=7_r=1.75' + str(mm_list[i]) + '.txt', mode = 'r+', encoding = 'UTF-8') as file_5:
            meta_data_ecowet = eval(file_5.read())
            data_list.append((128, mode_name_list[i], 'ecowet', sum([len(item) for item in list(meta_data_ecowet.values())])/128))
        with open('D:/桌面/F/2023.05.25-流量加权网络崩溃过程中超模体的涌现/result_fig/fig_1_result_ECOWET' + str(mode_name_list[i]) + '/k=7_r=1.75' + str(mm_list[i]) + '.txt', mode = 'r+', encoding = 'UTF-8') as file_6:
            meta_data_ecodry = eval(file_6.read())
            data_list.append((128, mode_name_list[i], 'ecodry', sum([len(item) for item in list(meta_data_ecodry.values())])/128))
    plt.rcParams['font.sans-serif'] = 'Arial'
    plt.rcParams['font.size'] = 20
    plt.figure(figsize = (12*0.8, 9*0.6))
    ax = plt.gca()
    ax.spines['bottom'].set_linewidth(2)
    ax.spines['left'].set_linewidth(2)
    ax.spines['right'].set_linewidth(2)
    ax.spines['top'].set_linewidth(2)
    plt.xlim(-0.5, 5.5)
    plt.xticks(ticks = [0, 1, 2, 3, 4, 5], labels = ['', '', '', '', '', ''], rotation = 45)
    plt.yticks(ticks = [1, 2, 3], labels = ['', '', ''], rotation = 45)
    x_list, y_list = [], []
    for i in range(4):
        for j in range(6):
            y_list.append(i)
            x_list.append(j)
    size_list = np.array([item[-1] for item in data_list])*400
    color_list = ['#00BAE1', '#00CEDA', '#12DFC5', '#70ECA6', '#B5F587', '#F9F871']*4
    plt.scatter(np.array(x_list), np.array(y_list), s = size_list, edgecolors = 'black', c = color_list, linewidths = 1, alpha = 0.8)
    plt.savefig('D:/桌面/enhance_size.jpg', dpi = 2400, bbox_inches = 'tight', pad_inches = 0)

def fig_big_small_enhance():
    mode_name_list = ['_enhance/cml', '_enhance/flow', '_enhance/degree']
    mm_list = ['_enhance', '_enhance', '_enhance']
    data_social, data_vote, data_urt, data_economic, data_ecowet, data_ecodry = [], [], [], [], [], []
    for i in range(3):
        with open('D:/桌面/F/2023.05.25-流量加权网络崩溃过程中超模体的涌现/result_fig/fig_1_result_SOCIAL' + str(mode_name_list[i]) + '/k=7_r=1.75' + str(mm_list[i]) + '.txt', mode = 'r+', encoding = 'UTF-8') as file_1:
            meta_data_social = eval(file_1.read())
            for item in meta_data_social.keys():
                meta_data_social[item] = len(meta_data_social[item])
            data_social.append(meta_data_social)
        with open('D:/桌面/F/2023.05.25-流量加权网络崩溃过程中超模体的涌现/result_fig/fig_1_result_VOTE' + str(mode_name_list[i]) + '/k=7_r=1.75' + str(mm_list[i]) + '.txt', mode = 'r+', encoding = 'UTF-8') as file_2:
            meta_data_vote = eval(file_2.read())
            for item in meta_data_vote.keys():
                meta_data_vote[item] = len(meta_data_vote[item])
            data_vote.append(meta_data_vote)
        with open('D:/桌面/F/2023.05.25-流量加权网络崩溃过程中超模体的涌现/result_fig/fig_1_result_URT' + str(mode_name_list[i]) + '/k=7_r=3.75' + str(mm_list[i]) + '.txt', mode = 'r+', encoding = 'UTF-8') as file_3:
            meta_data_urt = eval(file_3.read())
            for item in meta_data_urt.keys():
                meta_data_urt[item] = len(meta_data_urt[item])
            data_urt.append(meta_data_urt)
        with open('D:/桌面/F/2023.05.25-流量加权网络崩溃过程中超模体的涌现/result_fig/fig_1_result_ECONOMIC' + str(mode_name_list[i]) + '/k=7_r=1.75' + str(mm_list[i]) + '.txt', mode = 'r+', encoding = 'UTF-8') as file_4:
            meta_data_economic = eval(file_4.read())
            for item in meta_data_economic.keys():
                meta_data_economic[item] = len(meta_data_economic[item])
            data_economic.append(meta_data_economic)
        with open('D:/桌面/F/2023.05.25-流量加权网络崩溃过程中超模体的涌现/result_fig/fig_1_result_ECOWET' + str(mode_name_list[i]) + '/k=7_r=1.75' + str(mm_list[i]) + '.txt', mode = 'r+', encoding = 'UTF-8') as file_5:
            meta_data_ecowet = eval(file_5.read())
            for item in meta_data_ecowet.keys():
                meta_data_ecowet[item] = len(meta_data_ecowet[item])
            data_ecowet.append(meta_data_ecowet)
        with open('D:/桌面/F/2023.05.25-流量加权网络崩溃过程中超模体的涌现/result_fig/fig_1_result_ECOWET' + str(mode_name_list[i]) + '/k=7_r=1.75' + str(mm_list[i]) + '.txt', mode = 'r+', encoding = 'UTF-8') as file_6:
            meta_data_ecodry = eval(file_6.read())
            for item in meta_data_ecodry.keys():
                meta_data_ecodry[item] = len(meta_data_ecodry[item])
            data_ecodry.append(meta_data_ecodry)
    y_flow_big, y_flow_small, y_degree_big, y_degree_small = [], [], [], []
    re_big, re_small = func_eq_dict(data_social[0], data_social[1])
    y_flow_big.append(re_big)
    y_flow_small.append(re_small)
    re_big, re_small = func_eq_dict(data_social[0], data_social[2])
    y_degree_big.append(re_big)
    y_degree_small.append(re_small)
    re_big, re_small = func_eq_dict(data_vote[0], data_vote[1])
    y_flow_big.append(re_big)
    y_flow_small.append(re_small)
    re_big, re_small = func_eq_dict(data_vote[0], data_vote[2])
    y_degree_big.append(re_big)
    y_degree_small.append(re_small)
    re_big, re_small = func_eq_dict(data_economic[0], data_economic[1])
    y_flow_big.append(re_big)
    y_flow_small.append(re_small)
    re_big, re_small = func_eq_dict(data_economic[0], data_economic[2])
    y_degree_big.append(re_big)
    y_degree_small.append(re_small)
    re_big, re_small = func_eq_dict(data_urt[0], data_urt[1])
    y_flow_big.append(re_big)
    y_flow_small.append(re_small)
    re_big, re_small = func_eq_dict(data_urt[0], data_urt[2])
    y_degree_big.append(re_big)
    y_degree_small.append(re_small)
    re_big, re_small = func_eq_dict(data_ecowet[0], data_ecowet[1])
    y_flow_big.append(re_big)
    y_flow_small.append(re_small)
    re_big, re_small = func_eq_dict(data_ecowet[0], data_ecowet[2])
    y_degree_big.append(re_big)
    y_degree_small.append(re_small)
    re_big, re_small = func_eq_dict(data_ecodry[0], data_ecodry[1])
    y_flow_big.append(re_big)
    y_flow_small.append(re_small)
    re_big, re_small = func_eq_dict(data_ecodry[0], data_ecodry[2])
    y_degree_big.append(re_big)
    y_degree_small.append(re_small)
    x_list = np.arange(1, 7)
    y_cml = np.zeros(6)
    plt.rcParams['font.sans-serif'] = 'Arial'
    plt.rcParams['font.size'] = 20
    plt.figure(figsize = (12*0.8, 9*0.4))
    plt.xticks(ticks = [1, 2, 3, 4, 5, 6], labels = ['', '', '', '', '', ''], rotation = 45)
    ax = plt.gca()
    ax.spines['bottom'].set_linewidth(2)
    ax.spines['left'].set_linewidth(2)
    ax.spines['right'].set_linewidth(2)
    ax.spines['top'].set_linewidth(2)
    plt.fill_between(x_list, y_cml, y_flow_big, facecolor = '#00D8CD', alpha = 0.3)
    plt.fill_between(x_list, y_cml, y_degree_big, facecolor = '#50E3C0', alpha = 0.3)
    # plt.fill_between(x_list, y_cml, y_flow_small, facecolor = '#7DEDB2', alpha = 0.3)
    # plt.fill_between(x_list, y_cml, y_degree_small, facecolor = '#A6F5A6', alpha = 0.3)
    plt.plot(x_list, y_cml, label = 'CML', marker = 'x', color = '#56E8AC', linewidth = 2.5, markersize = 12)
    plt.plot(x_list, y_flow_big, label = 'Flow-big', marker = '>', color = '#ABF488', linewidth = 2.5, markersize = 12)
    # plt.plot(x_list, y_flow_small, label = 'Flow-small', marker = '<', color = '#00C3E1', linewidth = 2.5, markersize = 12)
    plt.plot(x_list, y_degree_big, label = 'Degree-big', marker = 'o', color = '#F9F871', linewidth = 2.5, markersize = 12)
    # plt.plot(x_list, y_degree_small, label = 'Degree-small', marker = 's', color = '#00ABE2', linewidth = 2.5, markersize = 12)
    plt.savefig('D:/桌面/big_small.jpg', dpi = 2400, bbox_inches = 'tight', pad_inches = 0)

def hypermotifs_local_resilience():
    x = [1, 2, 3, 4, 5, 6]
    # y = [0.000289389704862143, 0.000293242846969126, 0.00237591342890229, 0.000597502272191739, 0.00246062992125984, 0.00418307086614173]
    y = [0.00418307086614173, 0.00246062992125984, 0.00237591342890229, 0.000597502272191739, 0.000293242846969126, 0.000289389704862143]
    plt.rcParams['font.sans-serif'] = 'Arial'
    plt.rcParams['font.size'] = 20
    # plt.figure(figsize = (12*0.8, 9*0.5))
    plt.figure(figsize = (9*0.3, 12*0.63))
    # plt.xticks(ticks = [1, 2, 3, 4, 5, 6], labels = ['', '', '', '', '', ''], rotation = 45)
    plt.yticks(ticks = [1, 2, 3, 4, 5, 6], labels = ['', '', '', '', '', ''], rotation = 45)
    ax = plt.gca()
    ax.spines['bottom'].set_linewidth(2)
    ax.spines['left'].set_linewidth(2)
    ax.spines['right'].set_linewidth(0)
    ax.spines['top'].set_linewidth(0)
    # plt.plot(y, x, marker = 's', color = '#597b98', linewidth = 2.5, markersize = 12)
    plt.barh(x, y, edgecolor = ['#34E076', '#34E076', '#7F7F7F', '#BF9000', '#05BEFF', '#F05A56'], color = 'white', linewidth = 5, hatch = '/')
    plt.savefig('D:/桌面/hypermotifs_local_resilience.jpg', dpi = 2400, bbox_inches = 'tight', pad_inches = 0)

def fig_different_miu(file_path: str, flow_matrix: np.ndarray, node_list: list):
    file_name_list, name_pos_dict, temp_pos_dict, fig_mat, cover_mat = listdir(file_path), {}, {}, np.zeros((21, 21), dtype = np.float32), np.zeros((21, 21), dtype = np.bool_)
    for i, para in enumerate(np.linspace(0, 1, 21)): temp_pos_dict[round(float(para), 2)] = i
    for i, file_name in enumerate(file_name_list):
        tp_list = file_name_list[i].split('(')[1].split(')')[0].split(',')
        name_pos_dict[file_name] = (temp_pos_dict[round(float(tp_list[0]), 2)], temp_pos_dict[round(float(tp_list[1]), 2)])
    for i in range(len(cover_mat)):
        for j in range(len(cover_mat)):
            if i + j > 20: cover_mat[i, j] = True
    for i, file_name in enumerate(file_name_list):
        print(round((i + 1) / 231, 2))
        percolation_re = fw_percolation_flow(file_path + file_name, flow_matrix, node_list)
        fig_mat[name_pos_dict[file_name]] = [item[1] for item in percolation_re].index(max([item[1] for item in percolation_re]))
    plt.rcParams['font.sans-serif'] = 'Arial'
    plt.rcParams['font.size'] = 12
    plt.figure(figsize=(5, 5))
    sns.heatmap(fig_mat, cmap = 'vlag', alpha = 0.6, vmin = -0.01, vmax = 1.01, mask = cover_mat, cbar = True, annot = False, linewidths = 0.5, xticklabels = [round(float(item), 2) for item in np.linspace(0, 1, 21)], yticklabels = [round(float(item), 2) for item in np.linspace(0, 1, 21)])
    plt.savefig('D:/桌面/different_miu.jpg', dpi = 2400, bbox_inches = 'tight', pad_inches = 0)
    plt.clf()

def fig_artifical_hypermotifs_sta(mode: str):
    data = [[11/504510, 4/504510, 13/504510, 0, 4/504510, 3/504510, 1/504510, 1/504510, 0, 2/504510, 0, 0, 0, 0, 0, 0],
            [0, 1/23871, 0, 0, 1/23871, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [2/118828, 3/118828, 4/118828, 0, 4/118828, 3/118828, 0, 0, 0, 0, 0, 1/118828, 1/118828, 0, 0, 0],
            [11/50086, 0, 9/50086, 2/50086, 2/50086, 2/50086, 0, 2/50086, 0, 1/50086, 1/50086, 0, 1/50086, 0, 0, 0],
            [0, 0, 1/8128, 0, 2/8128, 0, 0, 0, 0, 1/8128, 0, 0, 0, 0, 0, 0],
            [1/8128, 0, 0, 0, 2/8128, 1/8128, 0, 0, 0, 1/8128, 1/8128, 0, 0, 1/8128, 0, 0]]
    # mask = np.array([[False, False, False, True, False, False, False, False, True, False, True, True, True, True, True, True],
    #         [True, False, True, True, False, True, True, True, True, True, True, True, True, True, True, True],
    #         [False, False, False, True, False, False, True, True, True, True, True, False, False, True, True, True],
    #         [False, True, False, False, False, False, True, False, True, False, False, True, False, True, True, True],
    #         [True, True, False, True, False, True, True, True, True, False, True, True, True, True, True, True],
    #         [False, True, True, True, False, False, True, True, True, False, False, True, True, False, True, True]])
    if mode == 'r':
        data = [[2, 19, 0, 8, 0, 4, 12, 1, 4, 9, 0, 3, 1, 1, 1, 1],
                [0, 20, 0, 14, 2, 3, 1, 4, 2, 4, 0, 1, 2, 0, 0, 4],
                [0, 18, 0, 8, 0, 4, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0],
                [1, 20, 4, 19, 2, 6, 1, 4, 0, 0, 3, 0, 0, 1, 1, 1]]
    elif mode == 'ba':
        data = [[0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
                [0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
    elif mode == 'ws':
        data = [[0, 27, 3, 7, 0, 10, 0, 2, 4, 0, 1, 0, 2, 0, 0, 0],
                [1, 26, 1, 17, 0, 18, 16, 8, 2, 43, 3, 4, 32, 9, 0, 4],
                [2, 22, 1, 18, 3, 6, 2, 4, 0, 15, 1, 8, 13, 0, 0, 1],
                [0, 21, 1, 19, 0, 6, 7, 1, 3, 19, 0, 5, 5, 0, 0, 5]]
    mask = []
    for i in range(len(data)):
        temp_list = []
        for item in data[i]:
            if item != 0: temp_list.append(False)
            elif item == 0: temp_list.append(True)
        mask.append(temp_list)
    mask = np.array(mask)
    data = np.array(data)/1247500
    xtic = []
    for i in range(16): xtic.append(' ')
    plt.rcParams['font.sans-serif'] = 'Arial'
    plt.rcParams['font.size'] = 20
    plt.figure(figsize=(16, 3))
    sns.heatmap(data, annot=False, cmap='GnBu', xticklabels = xtic, yticklabels=False, linewidths=1.5, cbar=True, center = np.mean(data), mask=mask, vmin = 0, vmax = 0.00004) #cmap='GnBu'  cmap='YlOrBr'
    plt.savefig('D:/桌面/' + mode + '_hypermotifs_sta.jpg', dpi = 1200, bbox_inches = 'tight', pad_inches = 0)

def fig_artifical_bar(mode: str):
    plt.rcParams['font.sans-serif'] = 'Arial'
    plt.rcParams['font.size'] = 20
    axes = plt.axes([0, 0, 0.2, 0.55])
    axes.set_ylabel('$R_l$')
    axes.set_ylim(0, 0.00073)
    if mode == 'r':
        data = [0.000198797595190381, 0.000151503006012024, 0.0000697394789579158, 0.000161122244488978]
        plt.xticks([1, 2, 3, 4], ['0.05', '0.10', '0.15', '0.20'], rotation = 90)
        axes.bar(list(range(1, len(data) + 1)), data, color = '#75fffc')
    elif mode == 'ba':
        data = [0.0000120240480961924, 6.41282565130261E-06, 7.21442885771543E-06, 0]
        plt.xticks([1, 2, 3, 4], ['1', '2', '3', '4'], rotation = 0)
        axes.bar(list(range(1, len(data) + 1)), data, color = '#81c2ff')
    elif mode == 'ws':
        data = [0.000133066132264529, 0.000707815631262525, 0.000316633266533066, 0.000291783567134269]
        plt.xticks([1, 2, 3, 4], ['0.05', '0.10', '0.15', '0.20'], rotation = 90)
        axes.bar(list(range(1, len(data) + 1)), data, color = '#6f71ff')
    plt.savefig('D:/桌面/' + mode + '_hypermotifs_sta.svg', bbox_inches = 'tight', pad_inches = 0)
    plt.clf()
    
def fig_different_k_fitline(mode: str, matrix_flow: np.ndarray):
    degree_matrix = np.zeros(matrix_flow.shape, dtype = np.int8)
    for i in range(matrix_flow.shape[0]):
        for j in range(matrix_flow.shape[1]):
            if matrix_flow[i, j] != 0: degree_matrix[i, j] = 1
    out_deg, in_deg = np.sum(degree_matrix, axis = 1), np.sum(degree_matrix, axis = 0)
    deg_list = np.sort(out_deg + in_deg)[::-1]
    y = get_different_k_fit(mode)
    x = list(range(1, len(y) + 1))
    plt.rcParams['font.sans-serif'] = 'Arial'
    plt.rcParams['font.size'] = 20
    axes = plt.axes([0, 0, 1.6*0.35*1.6, 0.9*0.35])
    axes.axvline(np.mean(deg_list), lw = 4, label = r'$\hat{k}$', color = '#7bff57', alpha = 0.7, zorder = 2)
    axes.axvline(np.max(deg_list), lw = 4, ls = '--', label = r'$\max{k}$', color = '#d886ff', alpha = 0.7, zorder = 2)
    axes.set_ylabel('Slope')
    axes.set_xlabel('$K$')
    axes.plot(x, y, color = '#ff7377', linewidth = 4, alpha = 0.7)
    plt.savefig('D:/桌面/' + mode + '_fitline.svg', bbox_inches = 'tight', pad_inches = 0.1)
    plt.clf()
    y = get_different_k_qc(mode)
    axes = plt.axes([0, 0, 1.6*0.35*1.6, 0.9*0.35])
    axes.axvline(np.mean(deg_list), lw = 4, label = r'$\hat{k}$', color = '#7bff57', alpha = 0.7, zorder = 2)
    axes.axvline(np.max(deg_list), lw = 4, ls = '--', label = r'$\max{k}$', color = '#d886ff', alpha = 0.7, zorder = 2)
    axes.set_ylabel('$q_c$')
    axes.set_xlabel('$K$')
    axes.plot(x, y, color = '#ff9f51', linewidth = 4, alpha = 0.7)
    plt.savefig('D:/桌面/' + mode + '_qc.svg', bbox_inches = 'tight', pad_inches = 0.1)
    plt.clf()
    axes = plt.axes([0, 0, 1.6*0.35*1.6, 0.9*0.35])
    axes.set_xlabel('Nodes')
    axes.set_ylabel('Degree')
    axes.axhline(np.mean(deg_list), lw = 4, label = 'Mean degree', color = '#7bff57', alpha = 0.7, zorder = 2)
    axes.axhline(np.max(deg_list), lw = 4, ls = '--', label = 'Max degree', color = '#d886ff', alpha = 0.7, zorder = 2)
    axes.scatter(x, deg_list, c = '#00ffb5', alpha = 0.7)
    plt.legend(frameon = False, ncol = 2, bbox_to_anchor = (0.98, -0.35))
    plt.savefig('D:/桌面/' + mode + '_deg.svg', bbox_inches = 'tight', pad_inches = 0.1)
    plt.clf()
