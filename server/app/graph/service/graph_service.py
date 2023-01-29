# -*- coding: UTF-8 -*-
import os
import time
import pickle
import MySQLdb
import datetime
import pandas as pd
from copy import deepcopy


class SQLHandle():
    def __init__(self):
        self.db = MySQLdb.connect("localhost", "Bailing", "Emzujju12!", "TESTDB", charset='utf8')
        self.cursor = self.db.cursor()
        self.sql = "SELECT * FROM EMPLOYEE WHERE INCOME > %s" % (1000)
        self.table_head = ['title', 'summary', 'author', 'Date', 'Molecular', '期刊', 'Doi', 'PMID',
       '被引次数', 'index_file', '结论-Result', '疗效', '样本量-Sample Count',
       '临床指标-Indicator', '分组-Group', '药物-Drugs', '疾病-Disease',
       '副作用-Side Effect', '微生物', '细胞', '基因-Gene', '通路/靶标-Pathway/Target']
    def get_article_table(self):

        temp_db = {}
        try:
            # 执行SQL语句
            self.cursor.execute(self.sql)
            # 获取所有记录列表
            results = self.cursor.fetchall()
            for row in results:
                for i, key in enumerate(self.table_head):
                    temp_db[key].append(row[i])
        except:
            None
        return pd.DataFrame(temp_db).fillna("")

def mkdir(path):
    '''
    创建目录
    '''
    folder = os.path.exists(path)

    if not folder:
        os.makedirs(path)

def get_files(path):
    '''
    获取所有文件目录
    '''
    temp = []
    for line in os.listdir(path):
        temp.append(os.path.join(path, line))
    return temp

class GraphService():
    def __init__(self):
        self.root_path = "Dataset/"
        self.cache_path = self.root_path + "Cache/"
        self.pdf_files = get_files(self.root_path + "PDFs")
        self.extract_files = get_files(self.root_path + "Extract")
        self.ip_host_url = "http://43.154.134.150:7096/"

        self.graph_rela = ['结论-Result', '疗效', '样本量-Sample Count',
                           '临床指标-Indicator', '分组-Group', '药物-Drugs', '疾病-Disease',
                           '副作用-Side Effect', '微生物', '细胞', '基因-Gene', '通路/靶标-Pathway/Target']
        self.mdb = SQLHandle()
        self.main_table = self.mdb.get_article_table()
        self.mdb.db.close()

        self.init_sec()
        self.main_graph = self.build_graph(self.main_table)

        self.temp_graph = deepcopy(self.main_graph)
        self.temp_table = deepcopy(self.main_table)

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
        for line in self.main_table["Doi"].values:
            urls.append("https://doi.org/" + line)
        self.main_table["原文链接"] = urls

    def save_cache(self, data, name):
        mkdir(self.cache_path)
        pic_file = open(self.cache_path + "\\" + name + ".pickle", "wb")
        pickle.dump(data, pic_file)
        pic_file.close()

    def load_cache(self, name):
        try:
            with open(self.cache_path + "\\" + name + ".pickle", 'rb') as f:
                data = pickle.load(f)
            return data
        except:
            return None

    def search_graph(self, text):
        search_table = self.search_data(text)
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

    def search_table(self, text):

        search_df = self.search_data(text)

        file_name = self.cache_path + "\\SearchResult" + str(int(time.time() * 100000000000)) + ".xlsx"
        search_df.to_excel(file_name, index=None)
        return {"table": [{na: a[i] for i, na in enumerate(list(self.main_table.keys()))} for a in search_df.values],
                "number_article": float(len(search_df.values)),
                "file_name": file_name}

    def search_data(self, text):
        '''
        检索表格
        '''
        terminal, text = self.teminal(text)
        indexs_n = []
        text = text.lower()
        index = 0
        for i, line in enumerate(self.main_table.values):
            temp = ""
            for subline in line:
                temp += str(subline)
            line = temp
            if text in line.lower():
                indexs_n.append(True)
            else:
                indexs_n.append(False)

        search_df = self.main_table[indexs_n]
        temp = {}

        for i, line in enumerate(list(search_df.keys())):
            temp[line] = search_df.values[terminal[0]:terminal[1], i]
        search_df = pd.DataFrame(temp)
        self.temp_table = search_df
        return search_df

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

    def get_title(self):
        '''
        获取所有文章名称
        '''
        return list(self.main_table["title"].values)

    def get_extract(self, title):
        '''
        获取PDFs提取到的图像和表格
        '''
        try:
            file_name = self.main_table[self.main_table["title"].values == title]["index_file"][0]
            PDF_Name = os.path.join(self.ip_host_url,self.root_path, "PDFs", file_name + ".pdf").replace(self.root_path,"static/")
            extract = []
            for line in get_files(os.path.join(self.root_path, "Extract", file_name, "png")):
                extract.append({"type": 0, "url": self.ip_host_url + line.replace(self.root_path,"static/")})
            for line in get_files(os.path.join(self.root_path, "Extract", file_name, "xlsx")):
                extract.append({"type": 1, "url": self.ip_host_url + line.replace(self.root_path,"static/")})
            return {"files": extract, "archive": os.path.join(self.ip_host_url,self.root_path, "Extract", file_name + ".zip").replace(self.root_path,"static/"),
                    "pdf": PDF_Name}
        except:
            return {"files": [], "archive": "", "pdf": ""}

if __name__ == '__main__':
    '''
    Sample
    '''

    graph = GraphService()

    graph.main_graph  # 所有图谱（图结构）

    graph.main_table  # 所有文章数据（表格）

    graph.get_title()  # 所有文章名

    result = graph.search_graph("yphylla-Derived")  # 检索图谱（图结构）

    result = graph.search_table("yphylla-Derived")  # 检索文章数据（表格）

    title = "A meta-analysis of the clinical efficacy and safety of Bailing capsules in the treatment of nephrotic syndrome"
    result = graph.get_extract(title)  # 获取图片、表格、打包文件、PDF 注意：检索内容需传入完整Title信息
    print(result)