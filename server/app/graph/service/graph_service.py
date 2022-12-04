from py2neo import Graph
from config import NEO4J_HOST, NEO4J_PORT, NEO4J_USER, NEO4J_PASSWORD
import pandas as pd
import pickle
import _thread
import os
import numpy as np
import json

import time
import datetime

def mkdir(path):
    folder = os.path.exists(path)

    if not folder:
        os.makedirs(path)

class GraphNeo():
    def __init__(self,neo4j_host,neo4j_port,neo4j_user,neo4j_password):
        self.graph = Graph("neo4j://" + neo4j_host + ":" + neo4j_port, auth=(neo4j_user, neo4j_password))
        self.session = {}
        self.cache_path = "cache"
        self.cache_graph = "graph"
        self.cache_table = "table"
        self.en2ch = {"Title":"文献","Drugs":"药物/成分","Pathway_Target":"通路/靶标","Result":"结论","Group":"分组","Indicator":"指标","Molecular":"机制"}

        self.total_graph = self.load_cache(self.cache_graph)
        self.total_table = self.load_cache(self.cache_table)
        try:
            _thread.start_new_thread(self.get_graphs,("图谱异步加载",))
            _thread.start_new_thread(self.get_table,("表格异步加载",))
        except:
            print("异步错误")

    def build_nodes(self, nodes_record):
        data = {"id": str(nodes_record.get('n').identity),
                "label": next(iter(nodes_record.get('n').labels))}
        data.update(nodes_record.get('n'))

        return {"data": data}

    def build_edges(self, relation_record):
        data = {"source": relation_record.get('r').start_node.identity,
                "target": relation_record.get('r').end_node.identity,
                "relationship": type(relation_record.get('r')).__name__}

        return {"data": data}

    def build_graph(self,nodes_result,relation_result):
        nodes = list(map(self.build_nodes, nodes_result))
        edges = list(map(self.build_edges, relation_result))
        return edges, nodes

    def get_graphs(self, name):
        while True:
            search_rel_sql = "MATCH ()-[r]->() RETURN r"
            search_nodes_sql = "MATCH (n) RETURN n"

            relation_result = self.graph.run(search_rel_sql).data()
            nodes_result = self.graph.run(search_nodes_sql).data()

            edges, nodes = self.build_graph(nodes_result,relation_result)
            self.save_cache({"nodes": nodes, "links": edges},self.cache_graph)
            self.total_graph = self.load_cache(self.cache_graph)

    def get_table(self,name):
        while True:
            search_nodes_sql = "MATCH (n:Title) RETURN n"
            nodes_result = self.graph.run(search_nodes_sql).data()

            nodes_result = list(map(self.build_nodes, nodes_result))
            temp_dict = {"id":[],"Drugs":[],"Group":[],"Abstract":[],"Title":[],"Molecular":[],"Indicator":[],"Result":[],"Side Effect":[],"Pathway/Target":[],"Year":[],"Sample count":[],"Author":[]}
            for line in nodes_result:
                for sub_line in temp_dict.keys():
                    temp_dict[sub_line].append(line["data"][sub_line])
            self.save_cache(pd.DataFrame(temp_dict),self.cache_table)
            self.total_table = self.load_cache(self.cache_table)

    def table2dict(self,table):
        temp_dict = {}
        table = table.replace(np.nan, "")
        for line in table.keys():
            temp_dict[line] = list(table[line].values)
        return temp_dict

    def save_cache(self,data,name):
        mkdir(self.cache_path)
        pic_file = open(self.cache_path + "/" + name + ".pickle", "wb")
        pickle.dump(data, pic_file)
        pic_file.close()

    def load_cache(self,name):
        try:
            with open(self.cache_path + "/" + name + ".pickle", 'rb') as f:
                data = pickle.load(f)
            print(name + "服务器成功加载")
            return data
        except:
            print(name + "服务器正在初始化")
            return None

    def search_graph(self, text):
        ids = []
        nodes = []
        links = []
        text = text.lower()
        num_article = 0
        for line in self.total_graph["nodes"]:
            try:
                if text in line["data"]['Abstract'].lower():
                    ids.append(line["data"]['id'])
                    nodes.append(line)
                    pass
            except:
                None
            try:
                if text in line["data"]['name'].lower() or text in line["data"]['title'].lower():
                    ids.append(line["data"]['id'])
                    nodes.append(line)
            except:
                if text in line["data"]['name'].lower() or text in line["data"]['Title'].lower():
                    ids.append(line["data"]['id'])
                    nodes.append(line)
        for line in self.total_graph["links"]:
            if str(line["data"]['source']) in ids and str(line["data"]["target"]) in ids:
                links.append(line)

        for line in nodes:
            if "Abstract" in line["data"].keys():
                num_article += 1 
        today = str(datetime.date.today().strftime('%y-%m'))
        year = str(today.split("-")[0])
        month = int(today.split("-")[1])
        
        up_date = {}
        for i in range(6):
            if month - i < 0:
                year = str(int(year) - 1)
                month += i
            up_date[year + "-" + str(month)] = 0
        classin = {}
        for line in nodes:
            if self.en2ch[line["label"]] not in classin.keys():
                classin[self.en2ch[line["label"]]] = 0.0
            classin[self.en2ch[line["label"]]] += 1.0
            try:
                up_date[line["up_date"]] += 1
            except:
                None
        classin = {"name":list(classin.keys()),"count":list(classin.values())}
        return {"nodes": nodes, "links": links,"number_nodes":float(len(nodes)),"number_links":float(len(links)),"number_article":float(num_article),"nodes_count":classin,"up_date":up_date}


    def search_table(self,text):
        indexs_n = []
        text = text.lower()
        self.total_table = self.total_table.replace(np.nan,"")
        for i, line in enumerate(self.total_table.values):
            line = " ".join(line)
            if text in line.lower():
                indexs_n.append(True)
            else:
                indexs_n.append(False)
                
        file_name = self.cache_path + "/SearchResult" + str(int(time.time()*100000000000)) + ".xlsx"
        self.total_table[indexs_n].to_excel(file_name,index=None)
        return {"table":[list(a) for a in self.total_table[indexs_n].values],"number_article":float(np.sum(indexs_n)),"file_name":file_name}

if __name__ == '__main__':
    '''
    Sample
    '''
    graph = GraphNeo(NEO4J_HOST, NEO4J_PORT, NEO4J_USER, NEO4J_PASSWORD)
    # 所有图谱（图结构）
    graph.total_graph
    # 所有文章数据（表格）
    graph.total_table
    # 所有文章名
    graph.total_table["table"]["Title"].values
    # 检索图谱（图结构）
    result = graph.search_graph("检索内容")
    print(json.dumps(result["nodes"]))
    print(json.dumps(result["links"]))
    # 检索文章数据（表格）
    result = graph.search_table("检索内容")
    print(json.dumps(result["table"]))

    # 2022/12/04 更新
    '''
    1、文章搜索返回的数据按一条一条的list返回 已完成
    2、Excel下载：  已完成
        先调用 graph.search_table 函数获取所有文章数据，返回值当中包含 file_name 字段，该字段指向保存好的excel文件位置以及文件名“cache文件夹下”
        前端调用该excel即可
    3、获取文章题目列表  已完成
        所有文章题目列表方法：list(graph.total_table["table"]["Title"].values)
    4、更新统计  已完成
        集成在 graph.search_graph 函数当中，返回字段为 up_date
    5、节点类型统计  已完成
        集成在 graph.search_graph 函数当中，返回字段为 nodes_count
    '''