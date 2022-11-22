import logging
import sys

from neo4j import GraphDatabase
from neo4j.exceptions import ServiceUnavailable
# from config import NEO4J_HOST, NEO4J_PORT, NEO4J_USER, NEO4J_PASSWORD

class Neo4jClient:

    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        # Don't forget to close the driver connection when you are finished with it
        self.driver.close()

    @staticmethod
    def enable_log(level, output_stream):
        handler = logging.StreamHandler(output_stream)
        handler.setLevel(level)
        logging.getLogger("neo4j").addHandler(handler)
        logging.getLogger("neo4j").setLevel(level)

    def create_friendship(self, person1_name, person2_name, knows_from):
        with self.driver.session() as session:
            # Write transactions allow the driver to handle retries and transient errors
            result = session.execute_write(
                self._create_and_return_friendship, person1_name, person2_name, knows_from)
            for row in result:
                print("Created friendship between: {p1}, {p2} from {knows_from}"
                      .format(
                          p1=row['p1'],
                          p2=row['p2'],
                          knows_from=row["knows_from"]))

    @staticmethod
    def _create_and_return_friendship(tx, person1_name, person2_name, knows_from):
        # To learn more about the Cypher syntax, see https://neo4j.com/docs/cypher-manual/current/
        # The Reference Card is also a good resource for keywords https://neo4j.com/docs/cypher-refcard/current/
        query = (
            "CREATE (p1:Person { name: $person1_name }) "
            "CREATE (p2:Person { name: $person2_name }) "
            "CREATE (p1)-[k:KNOWS { from: $knows_from }]->(p2) "
            "RETURN p1, p2, k"
        )
        result = tx.run(query, person1_name=person1_name,
                        person2_name=person2_name, knows_from=knows_from)
        try:
            return [{
                        "p1": row["p1"]["name"],
                        "p2": row["p2"]["name"],
                        "knows_from": row["k"]["from"]
                    }
                    for row in result]
        # Capture any errors along with the query and data for traceability
        except ServiceUnavailable as exception:
            logging.error("{query} raised an error: \n {exception}".format(
                query=query, exception=exception))
            raise

    def find_person(self, person_name):
        with self.driver.session() as session:
            result = session.execute_read(self._find_and_return_person, person_name)
            print(result)
            for row in result:
                print("Found person: {row}".format(row=row))

    @staticmethod
    def _find_and_return_person(tx, person_name):
        query = (
            # "MATCH (n) RETURN n"
            "MATCH (n) "
            "WHERE n.title =~ $person_name "
            "RETURN n"
        )
        result = tx.run(query, person_name=person_name)
        return [row for row in result]


if __name__ == "__main__":
    bolt_url = "bolt://116.198.202.249:7687"
    user = "neo4j"
    password = "Emzujju12!"
    Neo4jClient.enable_log(logging.INFO, sys.stdout)
    app = Neo4jClient(bolt_url, user, password)
    # app.create_friendship("Alice", "David", "School")
    app.find_person("Cordycepin inhibits pancreatic cancer cell growth in vitro and in vivo via targeting FGFR2 and blocking ERK signaling")
    app.close()
