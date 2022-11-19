from py2neo import Graph
from config import NEO4J_HOST, NEO4J_PORT, NEO4J_USER, NEO4J_PASSWORD
import pandas as pd


class GraphNeo():
    def __init__(self,neo4j_host,neo4j_port,neo4j_user,neo4j_password):
        # 连接neo4j数据库，输入地址、用户名、密码
        self.graph = Graph("neo4j://" + neo4j_host + ":" + neo4j_port, auth=(neo4j_user, neo4j_password))
        self.session = {}

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

    def get_seach_graphs(self, text = ""):
        if text == "":
            search_rel_sql = "MATCH ()-[r]->() RETURN r"
            search_nodes_sql = "MATCH (n) RETURN n"
        else:
            search_nodes_sql = "MATCH (n) WHERE n.name=~'.*" + text + ".*' RETURN n"
            search_rel_sql = "MATCH (n) WHERE n.name=~'.*" + text + ".*' MATCH (n)-[r]->() RETURN r"

        print("Neo4j检索中...")
        relation_result = self.graph.run(search_rel_sql).data()
        nodes_result = self.graph.run(search_nodes_sql).data()

        edges, nodes = self.build_graph(nodes_result,relation_result)
        search_data = {"nodes": nodes, "links": edges}
        print("Neo4j检索完成！")
        return search_data

    def get_search_table(self,text = ""):
        if text == "":
            search_nodes_sql = "MATCH (n:Title) RETURN n"
        else:
            search_nodes_sql = "MATCH (n:Title) WHERE n.name=~'.*" + text + ".*' RETURN n"
        nodes_result = self.graph.run(search_nodes_sql).data()

        nodes_result = list(map(self.build_nodes, nodes_result))
        temp_dict = {"id":[],"Drugs":[],"Group":[],"Abstract":[],"Title":[],"Molecular":[],"Indicator":[],"Result":[],"Side Effect":[],"Pathway/Target":[],"Year":[],"Sample count":[],"Author":[]}
        for line in nodes_result:
            for sub_line in temp_dict.keys():
                temp_dict[sub_line].append(line["data"][sub_line])
        return pd.DataFrame(temp_dict)


if __name__ == '__main__':
    '''
    Sample
    '''
    graph = GraphNeo(NEO4J_HOST, NEO4J_PORT, NEO4J_USER, NEO4J_PASSWORD)
    '''
    加载所有数据
    '''
    total_graph = graph.get_seach_graphs()
    '''
    检索数据
    '''
    search_graph = graph.get_seach_graphs("检索内容")

    '''
    加载所有文章信息
    '''
    total_data = graph.get_search_table()

    '''
    检索指定文章信息
    '''
    search_data = graph.get_search_table("检索内容")
