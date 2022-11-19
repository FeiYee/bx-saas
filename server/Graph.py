from py2neo import Graph


class GraphNeo():
    def __init__(self):
        # 连接neo4j数据库，输入地址、用户名、密码
        self.graph = Graph("neo4j://127.0.0.1:7687", auth=("neo4j", "Emzujju12!"))
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


    def get_total_graph(self):
        select_rel_sql = "MATCH ()-[r]->() RETURN r"
        select_nodes_sql = "MATCH (n) RETURN n"

        print("Neo4j加载中...")
        self.relation_result = self.graph.run(select_rel_sql).data()
        self.nodes_result = self.graph.run(select_nodes_sql).data()

        edges, nodes = self.build_graph(self.nodes_result,self.relation_result)
        self.total_data = {"nodes": nodes, "links": edges}
        print("Neo4j加载成功！")
        return self.total_data

    def get_seach_graphs(self, text):
        search_nodes_sql = "MATCH (n) WHERE n.name=~'.*" + text + ".*' RETURN n"
        search_rel_sql = "MATCH (n) WHERE n.name=~'.*" + text + ".*' MATCH (n)-[r]->() RETURN r"

        print("Neo4j检索中...")
        relation_result = self.graph.run(search_rel_sql).data()
        nodes_result = self.graph.run(search_nodes_sql).data()

        edges, nodes = self.build_graph(nodes_result,relation_result)
        search_data = {"nodes": nodes, "links": edges}
        print("Neo4j检索完成！")
        return search_data

if __name__ == '__main__':
    '''
    Sample
    '''
    graph = GraphNeo()
    '''
    加载所有数据
    '''
    total_data = graph.get_total_graph()

    '''
    检索数据
    '''
    search_data = graph.get_seach_graphs("检索内容")