from typing import Type, TypeVar, List
from fastapi import File, Form, UploadFile
from fastapi.encoders import jsonable_encoder
from sqlalchemy import func, or_
from sqlalchemy.orm import Session

from ..model.graph import Graph
from ..schema.graph_schema import GraphSchema

from app.datum.service.article_service import article_service
import re

GraphModelType = TypeVar("GraphModelType", bound=Graph)


class GraphService:

    def __init__(self, model: Type[GraphModelType]):
        self.model = model
        self.articles = False

    def create(self, graph_schema: GraphSchema, db: Session) -> Graph:
        data = jsonable_encoder(graph_schema)
        graph = self.model(**data)
        # article.created_by = current_user.id
        db.add(graph)
        db.commit()
        db.refresh(graph)
        # print(data)
        return data

    def gererate_articles(self,db: Session):
        if not self.articles:
            articles = article_service.find_by_title(title="", db=db)
            articles_list = []
            for article in articles:
                articles_list.append(article.__dict__)
            self.articles = articles_list

    def find_by_keyword(self, keyword: str, db: Session) -> List[tuple[Graph]]:
        command_range, keyword = self.teminal(keyword)
        articles = article_service.find_by_title(title=keyword, db=db)

        self.gererate_articles(db)
        article_ids = []
        article_dict = {}
        for article in articles:
            article_ids.append(article.id)
            article_dict[article.id] = article.__dict__

        filters = [or_(
            self.model.article_id.in_(article_ids),
            self.model.ent1.like('%{keyword}%'.format(keyword=keyword)),
            self.model.ent2.like('%{keyword}%'.format(keyword=keyword)),
            self.model.rela.like('%{keyword}%'.format(keyword=keyword))
        )]

        graphs = db.query(self.model).filter(*filters).all()
        # db.query(self.model).filter(self.model.ent1.like('%{keyword}%'.format(keyword=keyword))).all()

        if command_range[0] == None and command_range[1] == None:
            graphs = graphs
        elif command_range[0] == None:
            graphs = graphs[:command_range[1]]#graph_table.head(command_range[1] * 20)
        elif command_range[1] == None:
            #             print(graph_table.values.shape[0],ranges[0])
            graphs = graphs[-command_range[1]:]
        #             print(graph_table)
        else:
            graphs = graphs[command_range[0]:command_range[1]]



        graph_dict = []
        for graph in graphs:
            data = graph.__dict__
            # data['article'] = article_dict.get(graph.article_id)
            graph_dict.append(data)
        graph_dict = self.gererate_graph(graph_dict)
        graph_dict["links"], graph_dict["number_article"] = self.link_add_info(graph_dict["links"], self.articles)
        return graph_dict

    def search_graph(self, keyword: str, db: Session):
        graphs = self.find_by_keyword(keyword=keyword, db=db)
        return graphs

    def link_add_info(self,links, articles):
        '''
        links： link_list
        articles: articles_list
        '''
        num_article = 0
        for link in links:
            print(link["data"]['article_id'])
            article_id = link["data"]['article_id']
            article = next((article for article in articles if article['id'] == article_id), None)

            if article:
                link['data']['title'] = article['title']
                link['data']['summary'] = article['summary']
                link['data']['author'] = str(article['author']).replace(" ;@;","、")
                # link['data']['molecular'] = str(article['molecular']).replace(" ;@;","、")
                link['data']['journal'] = article['journal']
                link['data']['result'] = str(article['result']).replace(" ;@;","、")
                link['data']['drugs'] = str(article['drugs']).replace(" ;@;","、")
                link['data']['disease'] = str(article['disease']).replace(" ;@;","、")
                link['data']['indicator'] = str(article['indicator']).replace(" ;@;","、")
                link['data']['pathway_target'] = str(article['pathway_target']).replace(" ;@;","、")
                link['data']['side_effect'] = str(article['side_effect']).replace(" ;@;","、")
                link['data']['sample_count'] = str(article['sample_count']).replace(" ;@;","、")
                link['data']['date'] = str(article['date']).replace(" ;@;","、")

                other = ""

                if len(str(article['microbe']).replace(" ;@;","、")) > 1:
                    other += "Microbe：" + str(article['microbe']).replace(" ;@;","、") + "\n"
                if len(str(article['cell']).replace(" ;@;","、")) > 1:
                    other += "Cell：" + str(article['cell']).replace(" ;@;","、") + "\n"
                if len(str(article['gene']).replace(" ;@;","、")) > 1:
                    other += "Gene：" + str(article['gene']).replace(" ;@;","、") + "\n"

                link['data']['other'] = other
                num_article += 1
            else:
                link['data']['title'] = "未知"
                link['data']['summary'] = "未知"
                link['data']['author'] = "未知"
                # link['data']['molecular'] = "未知"
                link['data']['journal'] = "未知"
                link['data']['result'] = "未知"
                link['data']['drugs'] = "未知"
                link['data']['disease'] = "未知"
                link['data']['indicator'] = "未知"
                link['data']['side_effect'] = "未知"
                link['data']['sample_count'] = "未知"
                link['data']['pathway_target'] = "未知"
                link['data']['other'] = "未知"

        return links,float(num_article)


    def gererate_graph(self,ori_data):
        # 将find_by_keyword得到的list转为graph格式
        nodes = []
        links = []
        id_counter = 1

        for entry in ori_data:
            ent1 = entry['ent1']
            ent2 = entry['ent2']
            rela = entry['rela']
            article_id = entry['article_id']

            # Update nodes list
            node1 = next((node for node in nodes if node['data']['name'] == ent1), None)
            if node1 is None:
                node1 = {"data": {'id': id_counter, 'name': ent1, 'num': 1, 'size': 20, 'color': 0}}
                nodes.append(node1)
                id_counter += 1
            else:
                node1['data']['num'] += 1
                node1['data']['size'] += 10
                if node1['data']['size'] > 80:
                    node1['data']['size'] = 80

                node1['data']['color'] = int(node1['data']['size'] % 30)
            node2 = next((node for node in nodes if node['data']['name'] == ent2), None)
            if node2 is None:
                node2 = {"data": {'id': id_counter, 'name': ent2, 'num': 1, 'size': 20, 'color': 0}}
                nodes.append(node2)
                id_counter += 1
            else:
                node2['data']['num'] += 1
                node2['data']['size'] += 10
                if node2['data']['size'] > 80:
                    node2['data']['size'] = 80

                node2['data']['color'] = int(node2['data']['size'] % 30)

            # Update links list
            link = {"data": {'source': node1['data']['id'], 'name': rela, 'target': node2['data']['id'],
                             'article_id': article_id}}
            links.append(link)
            # 'number_nodes', 'number_links', 'number_article', 'nodes_count', 'up_date'
        return {"nodes": nodes, "links": links, "number_nodes": float(len(nodes)),
                "number_links": float(len(links))}

    def teminal(self, text):
        '''
        命令设计：
            text#500    //前500
            text#!500    //后500
            text#500-600  //500-600
            text#all   //所有
            text    //前100条
        '''
        text = re.sub(r"\s+", " ", text)

        command_range = [None, 30]

        if "#" in text:
            parts = text.split("#")
            text = parts[0]

            range_text = parts[-1].replace(" ", "").lower()

            if "-" in range_text:
                range_parts = range_text.split("-")
                command_range = [int(range_parts[0]) if range_parts[0] else None,
                                 int(range_parts[1]) if range_parts[1] else None]
            elif range_text == "all":
                command_range = [None, None]
            elif "!" in range_text or "！" in range_text:
                range_value = int(re.sub(r"[^0-9]", "", range_text))
                command_range = [-range_value, None]
            else:
                command_range = [None, int(range_text)]

        return command_range, text


graph_service = GraphService(Graph)
