import numpy as np
import xlwings as xw
import math
import copy

# 建立读取三个网络的方法，在main中直接调用
def data_reader_URT(file_path: str):
    # 读取数据与处理
    new_app = xw.App(visible = True, add_book = False)
    work_excel = new_app.books.open(file_path)
    origin_OD_data = work_excel.sheets['OD'].range('A1').expand('table').value
    origin_distance_data = work_excel.sheets['position'].range('A1').expand('table').value
    work_excel.close()
    new_app.quit()
    node_arr = np.array(origin_OD_data)
    node_arr = np.delete(node_arr, -1, axis = 1).reshape((1, -1))
    node_arr = np.unique(node_arr)
    matrix_size = len(node_arr)
    pos_dict = {}
    for i in origin_distance_data:
        pos_l = i[1].split(',')
        pos_t = (float(pos_l[0]), float(pos_l[1]))
        pos_dict[i[0]] = pos_t
    matrix_flow, matrix_distance = np.zeros((matrix_size, matrix_size), dtype=np.float32), np.zeros((matrix_size, matrix_size), np.float32)
    # 生成流量矩阵
    node_arr = list(node_arr)
    for t in origin_OD_data:
        i, j = node_arr.index(t[0]), node_arr.index(t[1])
        matrix_flow[i, j] += t[2]
    for i in range(matrix_size): # 去除噪点数据（OD相同的）
        matrix_flow[i, i] = 0
    # 生成距离矩阵
    for o in node_arr:
        for d in node_arr:
            i, j = node_arr.index(o), node_arr.index(d)
            matrix_distance[i, j] = distance_URT(pos_dict[o], pos_dict[d])
    for i in range(len(matrix_distance)):
        matrix_distance[i, i] = np.max(matrix_distance)
    return matrix_flow, matrix_distance, node_arr

def data_reader_SOCIAL(file_path: str):
    file = open(file_path, mode='r+', encoding='UTF-8')
    lines = file.readlines()
    for i in range(len(lines)):
        lines[i] = lines[i][:-1].split(' ')
        for j in range(len(lines[i])):
            lines[i][j] = int(lines[i][j])
    node_arr = np.array(lines).reshape((1, -1))
    node_arr = list(np.unique(node_arr))
    node_arr.sort()
    # 生成流量矩阵
    matrix_flow = np.zeros((len(node_arr), len(node_arr)), dtype=np.float32)
    for line in lines:
        matrix_flow[line[0], line[1]] += 1
    for i in range(len(node_arr)):
        matrix_flow[i, i] = 0
    # 生成距离矩阵
    matrix_distance = copy.deepcopy(matrix_flow)
    m_max = np.max(matrix_distance)
    matrix_distance = (m_max - matrix_distance)/m_max
    m_max = np.max(matrix_distance)
    for i in range(len(node_arr)):
        matrix_distance[i, i] = m_max
    return matrix_flow, matrix_distance, node_arr

def data_reader_NEURAL(file_path: str):
    file_1 = open(file_path, mode='r+', encoding='UTF-8')
    origin_data = file_1.readlines()
    for i in range(len(origin_data)):
        origin_data[i] = origin_data[i][:-1].split('\t')
        for j in range(len(origin_data[i])):
            origin_data[i][j] = int(origin_data[i][j])
    node_arr = []
    for i in range(len(origin_data)):
        node_arr.append(origin_data[i][0])
        node_arr.append(origin_data[i][1])
    node_arr = np.array(node_arr)
    node_arr = list(np.unique(node_arr))
    # 生成流量矩阵
    matrix_flow = np.zeros((len(node_arr), len(node_arr)), dtype=np.float32)
    for item in origin_data:
        matrix_flow[item[0]-1, item[1]-1] += item[2]
    for i in range(len(node_arr)):
        matrix_flow[i, i] = 0
    # 生成距离矩阵
    matrix_distance = copy.deepcopy(matrix_flow)
    m_max = np.max(matrix_distance)
    matrix_distance = (m_max - matrix_distance)/m_max
    m_max = np.max(matrix_distance)
    for i in range(len(node_arr)):
        matrix_distance[i, i] = m_max
    return matrix_flow, matrix_distance, node_arr

def data_reader_VOTE(file_path: str):
    file_1 = open(file_path, mode='r+', encoding='UTF-8')
    origin_data = file_1.readlines()
    for i in range(len(origin_data)):
        origin_data[i] = origin_data[i][: -1].split(' ')[: -1]
        for j in range(len(origin_data[i])):
            origin_data[i][j] = int(origin_data[i][j])
    node_arr = np.reshape(np.array(origin_data), (1, -1))
    node_arr = list(np.unique(node_arr))
    node_arr.sort()
    # 生成流量矩阵
    matrix_flow = np.zeros((len(node_arr), len(node_arr)), dtype = np.float32)
    for item in origin_data:
        matrix_flow[item[0]-1, item[1]-1] += 1
    for i in range(len(node_arr)):
        matrix_flow[i, i] = 0
    # 生成距离矩阵
    matrix_distance = copy.deepcopy(matrix_flow)
    m_max = np.max(matrix_distance)
    matrix_distance = (m_max - matrix_distance)/m_max
    m_max = np.max(matrix_distance)
    for i in range(len(node_arr)):
        matrix_distance[i, i] = m_max
    return matrix_flow, matrix_distance, node_arr

def data_reader_ecosystem(file_path: str):
    file_1 = open(file_path, mode='r+', encoding='UTF-8')
    origin_data = file_1.readlines()
    for i in range(len(origin_data)):
        origin_data[i] = origin_data[i][: -1].split(' ')
        origin_data[i].pop(2)
        origin_data[i][0] = int(origin_data[i][0])
        origin_data[i][1] = int(origin_data[i][1])
        origin_data[i][2] = float(origin_data[i][2])
    node_arr = []
    for i in range(len(origin_data)):
        node_arr.append(origin_data[i][0])
        node_arr.append(origin_data[i][1])
    node_arr = list(np.unique(np.array(node_arr)))
    node_arr.sort()
    # 生成流量矩阵
    matrix_flow = np.zeros((len(node_arr), len(node_arr)), dtype = np.float32)
    for item in origin_data:
        matrix_flow[item[0]-1, item[1]-1] += item[2]
    for i in range(len(node_arr)):
        matrix_flow[i, i] = 0
    # 生成距离矩阵
    matrix_distance = copy.deepcopy(matrix_flow)
    m_max = np.max(matrix_distance)
    matrix_distance = (m_max - matrix_distance)/m_max
    m_max = np.max(matrix_distance)
    for i in range(len(node_arr)):
        matrix_distance[i, i] = m_max
    return matrix_flow, matrix_distance, node_arr

def data_reader_economic(file_path: str):
    file_1 = open(file_path, mode='r+', encoding='UTF-8')
    origin_data = file_1.readlines()
    for i in range(len(origin_data)):
        origin_data[i] = origin_data[i][: -1].split(' ')
        origin_data[i][0] = int(origin_data[i][0])
        origin_data[i][1] = int(origin_data[i][1])
        origin_data[i][2] = float(origin_data[i][2])
    node_arr = []
    for i in range(len(origin_data)):
        node_arr.append(origin_data[i][0])
        node_arr.append(origin_data[i][1])
    node_arr = list(np.unique(np.array(node_arr)))
    node_arr.sort()
    # 生成流量矩阵
    matrix_flow = np.zeros((len(node_arr), len(node_arr)), dtype = np.float32)
    for item in origin_data:
        matrix_flow[node_arr.index(item[0]), node_arr.index(item[1])] += item[2]
    for i in range(len(node_arr)):
        matrix_flow[i, i] = 0
    # 生成距离矩阵
    matrix_distance = copy.deepcopy(matrix_flow)
    m_max = np.max(matrix_distance)
    matrix_distance = (m_max - matrix_distance)/m_max
    m_max = np.max(matrix_distance)
    for i in range(len(node_arr)):
        matrix_distance[i, i] = m_max
    return matrix_flow, matrix_distance, node_arr

# 内部方法，请勿在其他地方调用
def distance_URT(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)