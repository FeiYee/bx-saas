# -*- coding: UTF-8 -*-
import os
import time
import pickle
import pymysql
import datetime
import pandas as pd
from copy import deepcopy

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

    def build_db2graph(self,db):

        self.main_table = {}
        self.main_graph = {}

        self.cursor = db.cursor()
        self.cursor.execute("select COLUMN_NAME from information_schema.COLUMNS where table_name = 'article';")
        for line in self.cursor.fetchall():
            self.main_table[line[0]] = []
        self.set_data()
        self.init_sec()
        self.main_graph = self.build_graph(self.main_table)
        self.temp_table = deepcopy(self.main_table)
        self.temp_graph = deepcopy(self.main_graph)

    def set_data(self):
        self.cursor.execute("SELECT * FROM article")
        while True:
            try:
                data = self.cursor.fetchone()
                for i, line in enumerate(data):
                    self.main_table[list(self.main_table.keys())[i]].append(line)
            except:
                break
        self.main_table = pd.DataFrame(self.main_table)

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
            urls.append("https://doi.org/" + line)
        self.main_table["原文链接"] = urls

        temp = []
        for line in self.main_table[self.index].values:
            temp.append(" ".join(line).replace("."," ").replace(","," ").replace("  "," ").replace("  "," ").lower())
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
                    text = text.split("#")[0]
                else:
                    terminal = text.split("#")[-1].replace(" ", "")
                    terminal = [None, int(terminal)]
                    text = text.split("#")[0]
            else:
                terminal = [None, 100]
        except:
            terminal = [None, 100]
        return terminal, text

    def search_table(self, text, return_table = False):
        terminal, text = self.teminal(text)
        text = text.lower()
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
            file_name = self.cache_path + "/SearchResult" + str(int(time.time() * 100000000000)) + ".xlsx"
            search_df.to_excel(file_name, index=None)
            return {"table": [{na: a[i] for i, na in enumerate(list(self.main_table.keys()))} for a in search_df.values],
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

    def search_graph(self, text, db):

        self.build_db2graph(db)

        search_table = self.search_table(text,return_table = True)
        result_graph = self.build_graph(search_table)

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
        for line in result_graph["links"]:
            if line["data"]["relationship"] not in classin.keys():
                classin[line["data"]["relationship"]] = 0.0
            classin[line["data"]["relationship"]] += 1.0
            try:
                up_date[line["up_date"]] += 1
            except:
                None
        classin = {"name": list(classin.keys()), "count": list(classin.values())}
        up_date = {"date": list(up_date.keys()), "count": list(up_date.values())}

        return {"nodes": result_graph["nodes"],
                "links": result_graph["links"],
                "number_nodes": float(len(result_graph["nodes"])),
                "number_links": float(len(result_graph["links"])),
                "number_article": float(len(search_table.values)),
                "nodes_count": classin,
                "up_date": up_date}


graph_service = GraphService()
