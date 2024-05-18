from dataread import *
from CML import *
from result import *
from percolation import *
from enhance import *

# 三个网络的flow与distance矩阵统一返回数据类型为ndarray，但node_list_XXX则为list
# 社交网络部分
# data_SOCIAL_flow, data_SOCIAL_distance, node_list_SOCIAL = data_reader_SOCIAL('D:/桌面/F/2023.05.25-流量加权网络崩溃过程中超模体的涌现/code_data/email-Eu-core.txt')
# 投票网络部分
# data_VOTE_flow, data_VOTE_distance, node_list_VOTE = data_reader_VOTE('D:/桌面/F/2023.05.25-流量加权网络崩溃过程中超模体的涌现/code_data/out.convote.txt')
# URT部分
# data_URT_flow, data_URT_distance, node_list_URT = data_reader_URT('D:/桌面/F/2023.05.25-流量加权网络崩溃过程中超模体的涌现/code_data/URT.xlsx')
# 经济网络部分
# data_ECONOMIC_flow, data_ECONOMIC_distance, node_list_ECONOMIC = data_reader_economic('D:/桌面/F/2023.05.25-流量加权网络崩溃过程中超模体的涌现/code_data/econ-mbeacxc.txt')
# 生态网络部分-wet
# data_ECOWET_flow, data_ECOWET_distance, node_list_ECOWET = data_reader_ecosystem('D:/桌面/F/2023.05.25-流量加权网络崩溃过程中超模体的涌现/code_data/out.foodweb-baywet.txt')
# 生态网络部分-dry
# data_ECODRY_flow, data_ECODRY_distance, node_list_ECODRY = data_reader_ecosystem('D:/桌面/F/2023.05.25-流量加权网络崩溃过程中超模体的涌现/code_data/out.foodweb-baydry.txt')

miu, k, r, alpha = (0.4, 0.4), 3, 3, 1.1

# c, cl = 1, 7
# for i in range(4):
#     r = 0.75
#     for j in range(7):
#         ccc = round(c/cl * 100, 5)
#         r = round(r, 2)
#         # hyperedge_SOCIAL = cml_simulation(data_URT_flow, data_URT_distance, node_list_URT, miu, k, r, alpha, ccc)
#         file_1 = open('D:/桌面/F/2023.05.25-流量加权网络崩溃过程中超模体的涌现/result_fig/fig_1_result_VOTE/k=' + str(k) + '_r=' + str(r) + '.txt', mode='w+', encoding='UTF-8')
#         # print(hyperedge_SOCIAL, file=file_1)
#         file_1.close()
#         fig_hyperedge_cardinality_p_distribution(hyperedge_SOCIAL, 'k=' + str(k) + '_r=' + str(r))
#         # file_name = 'k=' + str(k) + '_r=' + str(r) + '.txt'
#         # percolation_result = fw_percolation_flow('D:/桌面/F/2023.05.25-流量加权网络崩溃过程中超模体的涌现/result_fig/fig_1_result_NEURAL/' + file_name, data_URT_flow, node_list_URT)
#         # fig_percolation_transition(percolation_result, file_name)
#         r += 0.25
#         c += 1
#     k += 2

# hyperedge_NOW = cml_simulation(data_ECODRY_flow, data_ECODRY_distance, node_list_ECODRY, (0.1, 0.1), 3, 6.75, 1.1, 100)
# file_1 = open('D:/桌面/k=' + str(k) + '_r=' + str(r) + '.txt', mode='w+', encoding='UTF-8')
# print(hyperedge_NOW, file=file_1)
# file_1.close()
# fig_hyperedge_cardinality_p_distribution(hyperedge_NOW, 'k=' + str(k) + '_r=' + str(r))
# file_name = 'k=' + str(k) + '_r=' + str(r) + '.txt'
# percolation_result = fw_percolation_flow('D:/桌面/' + file_name, data_ECODRY_flow, node_list_ECODRY)
# fig_percolation_transition(percolation_result, file_name)

#------------------------------------------------------------
#--------------------------Result----------------------------
#------------------------------------------------------------

# for i in range(4):
#     r = 1
#     for j in range(7):
#         r = round(r, 2)
#         file_name = 'k=' + str(k) + '_r=' + str(r)
#         percolation_result = fw_percolation_flow('D:/桌面/F/2023.05.25-流量加权网络崩溃过程中超模体的涌现/result_fig/fig_1_result_SOCIAL_enhance/degree/' + file_name + '_enhance.txt', data_SOCIAL_flow, node_list_SOCIAL)
#         fig_percolation_transition(percolation_result, file_name)
        # r += 0.25
#         input(file_name)
    # k += 2

# cut_num = 3
# file_name = 'k=7_r=1.75'
# with open('D:/桌面/F/2023.05.25-流量加权网络崩溃过程中超模体的涌现/result_fig/fig_1_result_ECONOMIC/' + file_name + '.txt', mode='r+', encoding='UTF-8') as file_1:
#     hyperedge = eval(file_1.read())
# fig_hyperedge_cardinality_p_distribution(hyperedge, file_name, cut_num)
# percolation_result = fw_percolation_flow('D:/桌面/F/2023.05.25-流量加权网络崩溃过程中超模体的涌现/result_fig/fig_1_result_ECODRY/' + file_name + '.txt', data_ECODRY_flow, node_list_ECODRY)
# percolation_result = fw_percolation_degree('D:/桌面/F/2023.05.25-流量加权网络崩溃过程中超模体的涌现/result_fig/fig_1_result_ECOWET/' + file_name + '.txt', node_list_ECOWET)
# fig_percolation_transition(percolation_result, file_name)

# fig_para_analysis('economic_origin')

# file_name = 'k=7_r=1.75'
# cluster_re = fw_percolation_cluster_list('D:/桌面/F/2023.05.25-流量加权网络崩溃过程中超模体的涌现/result_fig/fig_1_result_ECOWET/' + file_name + '.txt', data_ECOWET_flow, node_list_ECOWET)
# fig_cluster_power_law(['0.52', '0.6', '0.68'], cluster_re, 'D:/桌面/', file_name)

# 数hm的数量
# file_name = 'k=7_r=2.25_enhance'
# a = fw_hm_emergence('D:/桌面/F/2023.05.25-流量加权网络崩溃过程中超模体的涌现/result_fig/fig_1_result_ECODRY_enhance/flow/' + file_name + '.txt', data_SOCIAL_flow, node_list_SOCIAL)

# 计算hm出现水平，筛选适合的超边
# file_name = 'k=7_r=3.75'
# fw_t_hyperedge_num('D:/桌面/F/2023.05.25-流量加权网络崩溃过程中超模体的涌现/result_fig/fig_1_result_URT/' + file_name + '.txt', data_URT_flow, node_list_URT, 0.63)

fig_hypermotifs_sta()
# fig_average_size_enhance()
# fig_big_small_enhance()
# hypermotifs_local_resilience()

#------------------------------------------------------------
#--------------------------Result----------------------------
#------------------------------------------------------------

#------------------------------------------------------------
#--------------------Gao's意见修改----------------------------
#------------------------------------------------------------

# file_name = 'k=7_r=1.66'

# percolation_result = fw_percolation_flow('D:/桌面/F/2023.05.25-流量加权网络崩溃过程中超模体的涌现/result_fig/fig_1_result_NEURAL/' + file_name + '.txt', data_NEURAL_flow, node_list_NEURAL)
# percolation_result = fw_percolation_degree('D:/桌面/F/2023.05.25-流量加权网络崩溃过程中超模体的涌现/result_fig/fig_1_result_NEURAL/' + file_name + '.txt', node_list_NEURAL)
# fig_percolation_transition(percolation_result, file_name)

# for i in range(100):
#     percolation_result = fw_percolation_random('D:/桌面/F/2023.05.25-流量加权网络崩溃过程中超模体的涌现/result_fig/fig_1_result_SOCIAL/' + file_name + '.txt', node_list_SOCIAL)
#     fig_percolation_transition(percolation_result, file_name + '_' +  str(i))

# fig_ci_distribution(func_node_degree(func_hyperedge_read('D:/桌面/F/2023.05.25-流量加权网络崩溃过程中超模体的涌现/result_fig/fig_1_result_URT/' + file_name + '.txt')))
# fig_ci_distribution(func_node_flow(data_ECONOMIC_flow, node_list_ECONOMIC))

# 图4
# func_degree_flow_correlation(data_ECODRY_flow, 'ecodry') # 度、流量相关性
# fig_para_analysis_main('social')

#------------------------------------------------------------
#--------------------Gao's意见修改----------------------------
#------------------------------------------------------------




#------------------------------------------------------------
#---------------------关键节点加强----------------------------
#------------------------------------------------------------

# c, cl = 1, 7
# k = 3
# enhance_nodes_num = int(len(node_list_SOCIAL)*0.1)
# a = sorted(enhance_nodes_list_flow(data_SOCIAL_flow, node_list_SOCIAL, enhance_nodes_num))
# b = sorted(enhance_nodes_list_degree(data_SOCIAL_flow, node_list_SOCIAL, enhance_nodes_num))
# print(len([item for item in a if item in b]))
# for i in range(4):
#     r = 1
#     for j in range(7):
#         r = round(r, 2)
#         file_0 = open('D:/桌面/F/2023.05.25-流量加权网络崩溃过程中超模体的涌现/result_fig/fig_1_result_ECONOMIC/k=' + str(k) + '_r=' + str(r) + '.txt', mode='r+', encoding='UTF-8')
#         hyperedge = eval(file_0.read())
#         file_0.close()
#         enhance_nodes_list = enhance_nodes_list_cml(hyperedge, enhance_nodes_num)
#         # enhance_nodes_list = enhance_nodes_list_flow(data_ECONOMIC_flow, node_list_ECONOMIC, enhance_nodes_num)
#         # enhance_nodes_list = enhance_nodes_list_degree(data_ECONOMIC_flow, node_list_ECONOMIC, enhance_nodes_num)

#         r += 0.25
#         c += 1
#     k += 2
# for i in range(4):
#     r = 1.25
#     for j in range(7):
#         ccc = round(c/cl * 100, 5)
#         r = round(r, 2)
#         file_0 = open('D:/桌面/F/2023.05.25-流量加权网络崩溃过程中超模体的涌现/result_fig/fig_1_result_ECONOMIC/k=' + str(k) + '_r=' + str(r) + '.txt', mode='r+', encoding='UTF-8')
#         hyperedge = eval(file_0.read())
#         file_0.close()
#         enhance_nodes_list = enhance_nodes_list_cml(hyperedge, enhance_nodes_num)
#         # enhance_nodes_list = enhance_nodes_list_flow(data_ECONOMIC_flow, node_list_ECONOMIC, enhance_nodes_num)
#         # enhance_nodes_list = enhance_nodes_list_degree(data_ECONOMIC_flow, node_list_ECONOMIC, enhance_nodes_num)
#         hyperedge_enhance = cml_simulation_enhance(data_ECONOMIC_flow, data_ECONOMIC_distance, node_list_ECONOMIC, miu, k, r, alpha, ccc, enhance_nodes_list)
#         file_1 = open('D:/桌面/F/2023.05.25-流量加权网络崩溃过程中超模体的涌现/result_fig/fig_1_result_ECONOMIC_enhance/cml/k=' + str(k) + '_r=' + str(r) + '_enhance.txt', mode='w+', encoding='UTF-8')
#         print(hyperedge_enhance, file=file_1)
#         file_1.close()
#         # fig_hyperedge_cardinality_p_distribution(hyperedge_enhance, 'k=' + str(k) + '_r=' + str(r) + '_enhance')
#         # file_name = 'k=' + str(k) + '_r=' + str(r) + '_enhance.txt'
#         # percolation_result = fw_percolation_flow('D:/桌面/F/2023.05.25-流量加权网络崩溃过程中超模体的涌现/result_fig/fig_1_result_NEURAL_enhance/degree/' + file_name, data_NEURAL_flow, node_list_NEURAL)
#         # fig_percolation_transition(percolation_result, file_name)
#         r += 0.25
#         c += 1
#     k += 2

# enhance_degree_list, enhance_flow_list, enhance_cml_list = [], [], []
# for i in range(4):
#     r = 1.5
#     for j in range(30):
#         r = round(r, 2)
#         file_0 = open('D:/桌面/F/2023.05.25-流量加权网络崩溃过程中超模体的涌现/result_fig/fig_1_result_NEURAL_enhance/degree/k=' + str(k) + '_r=' + str(r) + '_enhance.txt', mode='r+', encoding='UTF-8')
#         hyperedge = eval(file_0.read())
#         file_0.close()
#         # enhance_degree_list.append(len([x for item in list(hyperedge.values()) for x in item]) - 297)
#         enhance_degree_list.append([len(item) for item in list(hyperedge.values())])
#         r += 0.01
#     k += 2
# k = 3
# for i in range(4):
#     r = 1.5
#     for j in range(30):
#         r = round(r, 2)
#         file_0 = open('D:/桌面/F/2023.05.25-流量加权网络崩溃过程中超模体的涌现/result_fig/fig_1_result_NEURAL_enhance/flow/k=' + str(k) + '_r=' + str(r) + '_enhance.txt', mode='r+', encoding='UTF-8')
#         hyperedge = eval(file_0.read())
#         file_0.close()
#         enhance_flow_list.append([len(item) for item in list(hyperedge.values())])
#         r += 0.01
#     k += 2
# k = 3
# for i in range(4):
#     r = 1.5
#     for j in range(30):
#         r = round(r, 2)
#         file_0 = open('D:/桌面/F/2023.05.25-流量加权网络崩溃过程中超模体的涌现/result_fig/fig_1_result_NEURAL_enhance/cml/k=' + str(k) + '_r=' + str(r) + '_enhance.txt', mode='r+', encoding='UTF-8')
#         hyperedge = eval(file_0.read())
#         file_0.close()
#         enhance_cml_list.append([len(item) for item in list(hyperedge.values())])
#         r += 0.01
#     k += 2
# start, end = 90, 120
# fig_enhance_resilience(enhance_degree_list[start: end], enhance_flow_list[start: end], enhance_cml_list[start: end])

#------------------------------------------------------------
#---------------------关键节点加强----------------------------
#------------------------------------------------------------
