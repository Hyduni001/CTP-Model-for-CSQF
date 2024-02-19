### If you use our CTP model in your work, we would appreciate a reference to the following paper:
### Yudong Huang, Tao Huang, Xinyuan Zhang, Shuo Wang,Hongyang Du, Dusit Niyato, Fei Richard Yu, and Yunjie Liu.
### CSQF-based Time-Sensitive Flow Scheduling in Long-distance Industrial IoT Networks

import matplotlib.pyplot as plt
import networkx as nx
import random
import time
import numpy as np


#hnodes=['h0','h1','h2','h3','h4','h5','h6','h7','h8','h9','h10','h11','h12','h13','h14']
#nodes=['0','1','2','3','4','5','6','7','8','9','10','11','12','13','14','h0','h1','h2','h3','h4','h5','h6','h7','h8','h9','h10','h11','h12','h13','h14']
#edges=[('h0','0', 0),('0','h0', 0),('h1','1', 0),('1','h1', 0),('h2','2', 0),('2','h2', 0),('h3','3', 0),('3','h3', 0),('h4','4', 0),('4','h4', 0),('h5','5', 0),('5','h5', 0),('h6','6', 0),('6','h6', 0),('h7','7', 0),('7','h7', 0),('h8','8', 0),('8','h8', 0),('h9','9', 0),('9','h9', 0),('h10','10', 0),('10','h10', 0),('h11','11', 0),('11','h11', 0),('h12','12', 0),('12','h12', 0),('h13','13', 0),('13','h13', 0),('h14','14', 0),('14','h14', 0),('0','1', 6.75),('1','0', 6.75),('1','2', 6.18),('2','1', 6.18),('0','2', 6.77),('2','0', 6.77),('0','8', 18.11),('8','0', 18.11),('1','3', 2.82),('3','1', 2.82),('2','4', 8.64),('4','2', 8.64),('2','3', 5.55),('3','2', 5.55),('3','6', 12.46),('6','3', 12.46),('4','5', 3.73),('5','4', 3.73),('4','7', 4.11),('7','4', 4.11),('5','6', 1.92),('6','5', 1.92),('6','11', 6.38),('11','6', 6.38),('7','8', 1.5),('8','7', 1.5),('7','11', 5.79),('11','7', 5.79),('8','9', 2.55),('9','8', 2.55),('9','10', 2.87),('10','9', 2.87),('9','14', 3.73),('14','9', 3.73),('10','12', 0.27),('12','10', 0.27),('11','12', 5.14),('12','11', 5.14),('12','13', 1.84),('13','12', 1.84),('13','14', 0.15),('14','13', 0.15)]# (u,v,w) where (u,v) is the egde, w is the weight

#part of internet2
hnodes=['h0','h1','h2','h3','h4','h5','h6','h7']
nodes=['0','1','2','3','4','5','6','7','h0','h1','h2','h3','h4','h5','h6','h7']
edges=[('h0','0', 0),('0','h0', 0),('h1','1', 0),('1','h1', 0),('h2','2', 0),('2','h2', 0),('h3','3', 0),('3','h3', 0),('h4','4', 0),('4','h4', 0),('h5','5', 0),('5','h5', 0),('h6','6', 0),('6','h6', 0),('h7','7', 0),('7','h7', 0),('0','1', 1.5),('1','0', 1.5),('1','2', 2.55),('2','1', 2.55),('2','3', 6.77),('3','2', 3.75),('3','4', 0.15),('4','3', 0.15),('4','6', 1.84),('6','4', 1.84),('2','5', 2.87),('5','2', 2.87),('5','6', 0.27),('6','5', 0.27),('6','7', 5.14),('7','6', 5.14),('0','7', 5.79),('7','0', 5.79)]# (u,v,w) where (u,v) is the egde, w is the weight

# 生成有向加权图
G = nx.DiGraph()
G.add_nodes_from(nodes)
G.add_weighted_edges_from(edges[i] for i in range(len(edges)))

pos = nx.spring_layout(G,k=1,iterations=100)

nx.draw_networkx_nodes(G, pos,node_size=400,font_size=8,node_color='#b3e2cd')
nx.draw_networkx_edges(G, pos, width=1,)
nx.draw_networkx_labels(G, pos)
nx.draw_networkx_edge_labels(G, pos, {(edges[i][0],edges[i][1]):edges[i][2] for i in range(len(edges))})
plt.tight_layout()
#plt.show()
print("*" * 10, "拓扑及时间敏感流的初始化", "*" * 10, "\n")
print("*" * 10, "有向无环加权双边图，拓扑初始化：图中共%d个节点，%d条边"%(len(nodes),len(edges)), "*" * 10)
print ("图的所有节点为:", G.nodes)
print ("图的所有边为:", G.edges)
print ("图的所有边的权重为:", G.edges.data())


# 生成流及其相关参数
class FLOW (object) :
    def __init__(self):
        self.id = 0
        self.offset = 0
        self.of_df = None
        self.pf = 0
        self.pkt_num = 0
        self.path = None
        self.cycle_shift = []
        self.t_map = []

def generate_of_df(hnodes):  #生成流的源节点和目的节点（且源！=目的）
    while True:
        of = random.choice(hnodes)
        df = random.choice(hnodes)
        if of == df:
            continue
        if of != df:
            break
    return (of,df)

def generate_flow(num, hnodes):  #生成num个流的列表，每条流为四元组（of, df, pf, ptk_num）,分别表示源，目的，发包周期，包数量
    flow_list_show = []
    flow_list_obj = []
    for i in range(num):
        new_flow = FLOW()
        new_flow.id = i
        new_flow.of_df = generate_of_df(hnodes)
        new_flow.pf = random.choice([4,8,16,32]) #ms
        new_flow.pkt_num = random.choice([1,2,3])
        tup_flow = (new_flow.id, new_flow.of_df[0], new_flow.of_df[1], new_flow.pf, new_flow.pkt_num)
        flow_list_obj.append(new_flow)
        flow_list_show.append(tup_flow)
        print ("第%d条流的参数为"%i, flow_list_show[i])
    return flow_list_obj,flow_list_show

print("\n")
print("*" * 10, "流及其相关参数【流id、源节点、目的节点、周期（ms），包数量（个）】", "*" * 10)


flow_list_obj, flow_list_show = generate_flow(1000, hnodes)


def generate_path(snodes, dnodes):
    shortest_weighted_path = nx.dijkstra_path(G, snodes, dnodes)
    #print("节点%s到节点%s最短加权路径为：" % (snodes, dnodes), shortest_weighted_path)
    return shortest_weighted_path

def paths_to_edges(paths):  # 将流的路径转化成边的组合
    flow_edge_list = []
    for j in range(len(paths) - 1):
        edge_tmp = (paths[j], paths[j + 1])
        flow_edge_list.append(edge_tmp)
    #print("节点%s到节点%s最短加权路径流经的边为：" % (paths[0], paths[-1]), flow_edge_list[1:])
    return flow_edge_list

#开始CSQF调度算法
T_cycle = 0.125 #ms
Hyper_cycle = 32 #ms
total_cycle_num = int(Hyper_cycle/T_cycle)
queue_num = 3 #每个交换机出端口的队列数量
queue_length = 10

Q_Ek_Tt = np.zeros((len(edges), total_cycle_num), dtype=np.int)

def print_flow_edge_matrix():
    print ("flow_cycle映射矩阵为：")
    print ("                T0,T1,T2,T3,T4,T5,T6,T7")
    for i in range (len(edges)):
        print(edges[i],Q_Ek_Tt[i])
    return 0

def sche_flows(flow_list_obj, Q_Ek_Tt):
    print("\n", "*" * 10, "调度开始", "*" * 10)
    sched_flow_num = 0
    global running_time
    for i in range(len(flow_list_obj)):
        starttime = time.time()
        #print( "*" * 10, "第%d条流的调度"%i, flow_list_show[i], "*" * 10)
        result_path = generate_path(flow_list_obj[i].of_df[0],flow_list_obj[i].of_df[1])
        result_edges = paths_to_edges(result_path)
        #tmp_cycle_shift = [0 for i in range(len(result_edges)-1)] + [1]
        flow_list_obj[i].offset = 0
        #print("流%d的偏置offset为：" % i, flow_list_obj[i].offset)
        #print("流%d的周期偏移为：" % i, tmp_cycle_shift)
        while flow_list_obj[i].offset < flow_list_obj[i].pf/T_cycle:

            suc_cycle_shift = [0] + [-1 for i in range(len(result_edges) - 1)]
            tmp_t_map = flow_list_obj[i].offset
            for k in range (1, len(result_edges)):
                tmp_cycle_shift = [0 for i in range(len(result_edges))]
                tmp_link_delay = G.edges[result_edges[k-1][0],result_edges[k-1][1]]["weight"]

                while tmp_cycle_shift[k] <= queue_num-2:
                    tmp_t_map += np.ceil(tmp_link_delay / T_cycle) + tmp_cycle_shift[k]
                    #print("流%d的offset,link_delay和tmp_cycle_shift信息为：" % i, flow_list_obj[i].offset, np.ceil(tmp_link_delay / T_cycle),tmp_cycle_shift[k])
                    #print("流%d经过的tmp_t_map信息：" % i, tmp_t_map)
                    M_Q_F = [0 for i in range(int(Hyper_cycle / flow_list_obj[i].pf))]
                    for j in range(int(Hyper_cycle/flow_list_obj[i].pf)):
                        tmp_t_map_period = (tmp_t_map + j*flow_list_obj[i].pf/T_cycle)%total_cycle_num
                        #print("流%d经过的tmp_t_map_period信息：" % i, tmp_t_map_period)
                        if (Q_Ek_Tt[edges.index((result_edges[k][0],result_edges[k][1],  G.edges[result_edges[k][0],result_edges[k][1]]["weight"]))][int(tmp_t_map_period)] + flow_list_obj[i].pkt_num <= queue_length):
                            #print("Q_Ek_Tt", Q_Ek_Tt[edges.index((result_edges[k][0],result_edges[k][1],  G.edges[result_edges[k][0],result_edges[k][1]]["weight"]))][int(tmp_t_map_period)])
                            #print("pkt_num", flow_list_obj[i].pkt_num)
                            #print("Q_Ek_Tt+pkt_num", Q_Ek_Tt[edges.index((result_edges[k][0],result_edges[k][1],  G.edges[result_edges[k][0],result_edges[k][1]]["weight"]))][int(tmp_t_map_period)] + flow_list_obj[i].pkt_num)
                            M_Q_F[j] = 1
                        else:
                            M_Q_F[j] = 0
                            #print(Q_Ek_Tt[edges.index((result_edges[k][0], result_edges[k][1],G.edges[result_edges[k][0], result_edges[k][1]]["weight"]))][int(tmp_t_map_period)])
                            #print(flow_list_obj[i].pkt_num)
                            #print(Q_Ek_Tt[edges.index((result_edges[k][0], result_edges[k][1],G.edges[result_edges[k][0], result_edges[k][1]]["weight"]))][int(tmp_t_map_period)] + flow_list_obj[i].pkt_num)
                    #print("第%d跳的M_Q_F信息:"%k, M_Q_F)
                    if 0 not in set(M_Q_F):
                        suc_cycle_shift[k]=tmp_cycle_shift[k]
                        break
                    elif (0 in set(M_Q_F) and tmp_cycle_shift[k]!=queue_num-2):
                        tmp_t_map = tmp_t_map - np.ceil(tmp_link_delay / T_cycle) - tmp_cycle_shift[k]
                        tmp_cycle_shift[k]=tmp_cycle_shift[k]+1
                        continue
                    else:
                        break

            #print("suc_cycle_shift信息：", suc_cycle_shift)
            if -1 not in set(suc_cycle_shift):

                tmp_t_map1 = flow_list_obj[i].offset
                for k in range(1, len(result_edges)):
                    flow_list_obj[i].cycle_shift.append(suc_cycle_shift[k])
                    tmp_link_delay = G.edges[result_edges[k - 1][0], result_edges[k - 1][1]]["weight"]
                    tmp_t_map1 += np.ceil(tmp_link_delay / T_cycle) + suc_cycle_shift[k]

                    for j in range(int(Hyper_cycle/flow_list_obj[i].pf)):
                        tmp_t_map_period = 0
                        tmp_t_map_period += (tmp_t_map1 + j*flow_list_obj[i].pf/T_cycle)%total_cycle_num
                        Q_Ek_Tt[edges.index((result_edges[k][0], result_edges[k][1],G.edges[result_edges[k][0], result_edges[k][1]]["weight"]))][int(tmp_t_map_period)] += flow_list_obj[i].pkt_num
                        flow_list_obj[i].t_map.append(int(tmp_t_map_period))
                #print("流%d被成功调度" % i)
                #print("流%d的offset信息为:"%i, flow_list_obj[i].offset)
                #print("流%d的cycle shift信息为:"%i, flow_list_obj[i].cycle_shift)
                #print("流%d经过的边信息为：" % i, result_edges)
                #print("流%d经过的cycle信息为：" % i, flow_list_obj[i].t_map)
                #print_flow_edge_matrix()
                sched_flow_num = sched_flow_num + 1
                endtime = time.time()
                running_time.append(round((endtime - starttime), 5))
                break
            else:
                flow_list_obj[i].offset = flow_list_obj[i].offset+1
                continue
        if  flow_list_obj[i].offset == flow_list_obj[i].pf/T_cycle:
            endtime = time.time()
            running_time.append(round((endtime - starttime), 5))
            #print("流%d不能调度" % i)
        else:
            continue
    print("%d条流中成功调度的流数量为："%(len(flow_list_obj)), sched_flow_num)
    return 0


running_time = []
sche_flows(flow_list_obj,Q_Ek_Tt)
print("所有流的算法运行时间为",running_time)
print("所有流的算法运行总时间为",sum(running_time))









