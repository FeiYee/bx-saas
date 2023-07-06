# -*- coding: UTF-8 -*-
import os
import time
import pickle
import pymysql
import datetime
import pandas as pd
from copy import deepcopy
import collections
from collections import Counter
def mkdir(path):
    '''
    创建目录
    '''
    folder = os.path.exists(path)

    if not folder:
        os.makedirs(path)
class GraphService:
    def __init__(self):
        self.main_table = {}
        self.main_graph = {}
        self.index = ['title', 'summary', 'author', 'molecular', 'journal',
       'result', 'effect', 'sample_count',
       'indicator', 'group', 'drugs', 'disease', 'side_effect', 'microbe',
       'cell', 'gene', 'pathway_target']
        self.graph_rela = ['molecular','result', 'effect', 'sample_count','indicator', 'group', 'drugs', 'disease', 'side_effect', 'microbe','cell', 'gene', 'pathway_target']
        self.temp_table = deepcopy(self.main_table)
        self.temp_graph = deepcopy(self.main_graph)
        self.cache_path = "temp"
        self.conn = self.mysql_conn()
        
        self.build_db2graph()
        
    def mysql_conn(self):
        conn = pymysql.connect(
            host='43.154.134.150',  # MySQL服务器地址
            port=3306,         # MySQL服务器端口号，默认为3306
            user='root',       # 用户名
            password='Emzujju12!',  # 密码
            database='bx_saas',  # 数据库名称
            charset='utf8mb4',  # 字符编码
            cursorclass=pymysql.cursors.DictCursor  # 游标类型
        )
        return conn
    
    def release(self):
        
#         self.cursor.close()
        self.conn.close()
        return True
    
    def build_db2graph(self):

        self.main_table = {}
        self.main_graph = {}
        
        self.set_data()
        self.init_sec()
        self.main_graph = self.build_graph(self.main_table)
        self.temp_table = deepcopy(self.main_table)
        self.temp_graph = deepcopy(self.main_graph)

    def set_data(self):
        query = "SELECT * FROM article;"
        
        cursor = self.conn.cursor()
        # 执行 SQL 查询语句
        cursor.execute(query)

        # 获取查询结果
        result = cursor.fetchall()

        # 获取查询结果中的列名
        column_names = [i[0] for i in cursor.description]
        cursor.close()
        # 将查询结果转换为 DataFrame
        self.main_table = pd.DataFrame(result, columns=column_names).fillna("")

    def init_sec(self):
        '''
        小问题矫正
        '''
        for key in list(self.main_table.keys()):
            try:
                temp = []
                for line in self.main_table[key].values:
                    temp.append(line.strip())
                self.main_table[key] = temp
            except:
                None
        urls = []
        for line in self.main_table["doi"].values:
            try:
                urls.append("https://doi.org/" + line)
            except:
                urls.append("无可用")
                
        self.main_table["原文链接"] = urls

        temp = []
        for line in self.main_table[self.index].values:
            try:
#                 print(line)
                line = [item if item is not None else '' for item in line]
                temp.append(" ".join(line).replace("."," ").replace(","," ").replace("  "," ").replace("  "," ").lower())
            except:
                print(temp[-1])
                print("\n\n")
                print(line)
        self.main_table["search_index"] = temp

    def teminal(self, text):
        '''
        命令设计：
            text#500    //前500
            text#!500    //后500
            text#500-600  //500-600
            text#all   //所有
            text    //前100条
        '''
        text = text.replace("  ", " ").replace("  ", " ")\
            .replace("  ", " ").replace("  ", " ")\
            .replace("  "," ").replace("  ", " ")
        try:
            if "#" in text:
                if "-" in text.split("#")[-1]:
                    terminal = text[1:].split(" ")[0].replace(" ", "").split("-")
                    terminal = [None if terminal[0] == "" else int(terminal[0]),
                                None if terminal[1] == "" else int(terminal[1])]
                    text = text.split("#")[0]
                elif "all" == text.split("#")[-1].replace(" ", "").lower():
                    terminal = [None, None]
                    text = text.split("#")[0]
                elif "!" in text.split("#")[-1] or "！" in text.split("#")[-1]:
                    terminal = text.split("#")[-1].replace(" ", "").replace("!", "").replace("！", "")
                    terminal = [-int(terminal), None]
#                     print(terminal)
                    text = text.split("#")[0]
                else:
                    terminal = text.split("#")[-1].replace(" ", "")
                    terminal = [None, int(terminal)]
                    text = text.split("#")[0]
            else:
                terminal = [None, 30]
        except:
            terminal = [None, 30]
        return terminal, text

    def search_table(self, text, return_table = False):
        terminal, text = self.teminal(text)
        text = text.lower()
        self.main_table["search_index"] = self.main_table["search_index"].astype(str)
        search_df = self.main_table[self.index][self.main_table["search_index"].str.contains(text)]


        if return_table:
            return search_df
        else:
            try:
                mkdir(self.cache_path)
            except:
                None
            try:
                mkdir(self.cache_path + "/SearchResult")
            except:
                None
            file_name = self.cache_path + "/SearchResult/" + str(int(time.time() * 100000000000)) + ".xlsx"
            search_df.to_excel(file_name, index=None)
#             temp_dict = []
#             for a in search_df.values:
#                 for i, na in enumerate(list(search_df.keys())):
#                     temp_dict.append({na:a[i]})
            table = [{na: [item if item is not None else '' for item in a][i] for i, na in enumerate(list(search_df.keys()))} for a in search_df.values]
            return {"table": table,
                    "number_article": float(len(search_df.values)),
                    "file_name": file_name}
        
    def build_graph(self, table):
        '''
        根据表格构建图谱
        '''
        nodes = []
        links = []
        index = 0
        main_nodes = 0
        for line in table.values:
            nodes.append({"data": {"id": index, "name": line[0]}})
            main_nodes = index
            index += 1
            for i, rela in enumerate(table.keys()):
                if line[i] != "":
                    try:
                        nodes[-1]["data"][rela] = line[i].replace("@;", "")
                    except:
                        nodes[-1]["data"][rela] = line[i]

            for i, rela in enumerate(self.graph_rela):
                nodes.append({"data": {"id": index, "name": line[list(table.keys()).index(rela)]}})
                links.append({"data": {"source": main_nodes, "target": index, "relationship": rela}})
                index += 1
                for i, rela in enumerate(table.keys()):
                    if line[list(table.keys()).index(rela)] != "":
                        try:
                            nodes[-1]["data"][rela] = line[i].replace("@;", "")
                        except:
                            nodes[-1]["data"][rela] = line[i]
        self.temp_graph = {"nodes": nodes, "links": links}
        return self.temp_graph


    def search_graph(self,text,db = None):
        text = text.lower()
        ranges, text = self.teminal(text)

        node_properties = ['id', 'name', 'title', 'summary', 'author', 'molecular', 'journal', 'result', 'drugs', 'disease']
        query = "SELECT * FROM graphs;"
        # 执行 SQL 查询语句
        cursor = self.conn.cursor()
        cursor.execute(query)

        # 获取查询结果
        result = cursor.fetchall()

        # 获取查询结果中的列名
        column_names = [i[0] for i in cursor.description]

        # 将查询结果转换为 DataFrame
        graph_table = pd.DataFrame(result, columns=column_names).sample(frac=1, random_state=42)
        if ranges[0] == None and ranges[1] == None:
            graph_table = graph_table
        elif ranges[0] == None:
            graph_table = graph_table.head(ranges[1] * 20)
        elif ranges[1] == None:
#             print(graph_table.values.shape[0],ranges[0])
            graph_table = graph_table.tail( - ranges[0] * 20)
#             print(graph_table)
        else:
            graph_table = graph_table.iloc[ranges[0]:ranges[1]]
        cursor.close()
#         conn.close()
#         temp_table = [item if item is not None else '' for item in graph_table.values]
        search_index = []
        for line in graph_table.values:
            line = [item if item is not None else '' for item in line]
            search_index.append(" ".join(line))
#             print(line)
        graph_table["search_index"] = search_index
        graph_table["search_index"] = graph_table["search_index"].astype(str)


        df = graph_table[["title","ent1","rela","ent2"]][graph_table["search_index"].str.contains(text)]

        rela_properties = ['summary', 'author', 'molecular', 'journal', 'result', 'drugs', 'disease']
        # Create a list of all unique nodes
        nodes = set(df['ent1']).union(set(df['ent2']))
        nodes_size_dict = Counter(list(df['ent1'].values) + list(df['ent2'].values))
        # Map each node to a unique ID
        node_to_id = {node: i for i, node in enumerate(nodes)}

        # Create a dictionary to store the graph
        graph = {'nodes': [], 'links': []}

        # Add each node to the graph
        for node, node_id in node_to_id.items():
            size = nodes_size_dict[node]
            if size < 20:
                size = 20
            else:
                size += 2
            
            if size > 80:
                size = 80
            graph['nodes'].append({"data":{'id': node_id, 'name': node, 'size':size ,'color': int(nodes_size_dict[node])%30}})
            

        total_article = []
        # Add each relationship to the graph
        for _, row in df.iterrows():
            start_id = node_to_id[row['ent1']]
            end_id = node_to_id[row['ent2']]
            rela = row['rela']
            graph['links'].append({"data":{'source': start_id, 'name': rela, 'target': end_id,'title':row["title"]}})
            total_article.append(row["title"])
            for cc in rela_properties:
                graph['links'][-1]["data"][cc] = "NULL"

        # Sort the nodes and relationships by ID
        graph['nodes'] = sorted(graph['nodes'], key=lambda x: x["data"]['id'])
        graph['links'] = sorted(graph['links'], key=lambda x: (x["data"]['source'], x["data"]['target'], x["data"]['name']))


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
        for line in graph["links"]:
            if line["data"]["name"] not in classin.keys():
                classin[line["data"]["name"]] = 0.0
            classin[line["data"]["name"]] += 1.0
            try:
                up_date[line["up_date"]] += 1
            except:
                None
        self.temp_graph = graph
        
        article_num = len(list(set(total_article)))
        
        return {"nodes": graph["nodes"],
        "links": graph["links"],
        "number_nodes": float(len(graph["nodes"])),
        "number_links": float(len(graph["links"])),
        "number_article": float(article_num),
        "nodes_count": classin,
        "up_date": up_date}
graph_service = GraphService()