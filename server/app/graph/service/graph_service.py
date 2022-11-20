from py2neo import Graph
from config import NEO4J_HOST, NEO4J_PORT, NEO4J_USER, NEO4J_PASSWORD
import pandas as pd
import pickle
import _thread
import os


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

        self.total_graph = self.load_cache(self.cache_graph)
        self.total_table = self.load_cache(self.cache_table)
        try:
            _thread.start_new_thread(self.get_seach_graphs,("图谱异步加载",))
            _thread.start_new_thread(self.get_search_table,("表格异步加载",))
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


    def save_cache(self,data,name):
        mkdir(self.cache_path)
        pic_file = open(self.cache_path + "/" + name + ".pickle", "wb")
        pickle.dump(data, pic_file)
        pic_file.close()

    def load_cache(self,name):
        try:
            print(name + "服务器成功加载")
            with open(self.cache_path + "/" + name + ".pickle", 'rb') as f:
                data = pickle.load(f)
            return data
        except:
            print(name + "服务器正在初始化")
            return None

    def search_graph(self, text):
        ids = []
        nodes = []
        links = []
        text = text.lower()
        for line in self.total_graph["nodes"]:
            try:
                if text in line["data"]['name'].lower() or text in line["data"]['title'].lower():
                    ids.append(line["data"]['id'])
                    nodes.append(line)
            except:
                if text in line["data"]['name'].lower() or text in line["data"]['Title'].lower():
                    ids.append(line["data"]['id'])
                    nodes.append(line)
        for line in self.total_graph["links"]:
            if line["data"]['source'] in ids and line["data"]["target"] in ids:
                links.append(line)
        return {"nodes": nodes, "links": links}
    def search_table(self,text):
        indexs_n = []
        text = text.lower()
        for line in self.total_table["Title"].values:
            if text in line.lower():
                indexs_n.append(True)
            else:
                indexs_n.append(False)
        return self.total_table[indexs_n]

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
    graph.total_table["Title"].values
    # 检索图谱（图结构）
    result = graph.search_graph("检索内容")
    # 检索文章数据（表格）
    result = graph.search_table("检索内容")

    '''
    
    '''
    # while 1:
    #     pass
