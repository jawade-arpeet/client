from elasticsearch import Elasticsearch, helpers


class ElasticSearch:
    def __init__(self, host, username, password) -> None:
        self.__client = self.__connect(host, username, password)

    def __connect(self, host, username, password):
        return Elasticsearch(
            hosts=host,
            basic_auth=(username, password),
        )

    def ping(self):
        return self.__client.ping()

    def create_index(self, index, mappings):
        return self.__client.indices.create(index=index, mappings=mappings)

    def delete_index(self, index):
        return self.__client.indices.delete(index=index)

    def index(self, index, document):
        return self.__client.index(index=index, document=document)

    def bulk_index(self, index, documents):
        def generator():
            for doc in documents:
                yield {
                    "_index": index,
                    **doc,
                }

        return helpers.bulk(self.__client, generator())

    def search(self, index, body):
        return self.__client.search(index=index, body=body)

    def scan(self, index, body):
        return helpers.scan(self.__client, index=index, query=body)

    def update_by_query(self, index, body):
        return self.__client.update_by_query(
            index=index, body=body, refresh=True, error_trace=True
        )

    def close(self):
        self.__client.close()
