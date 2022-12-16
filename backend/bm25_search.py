from elasticsearch import Elasticsearch
from elasticsearch.helpers import streaming_bulk
from tqdm import tqdm


class Searcher:
    def __init__(self, host, index_name, language="english"):
        self.es = Elasticsearch(host)
        
        self.index_name = index_name
        self.language = language
        self.mapping = {"mappings" : {
                    "properties" : {
                        "title": {"type": "text", "analyzer": self.language},
                        "text": {"type": "text", "analyzer": self.language}
                    }}}

    def create_index(self):
        print(f"Crating index \"{self.index_name}\"")
        self.es.indices.create(index=self.index_name, body=self.mapping, ignore=[400]) 
        
    def delete_index(self):
        print(f"Deleting index \"{self.index_name}\"")
        self.es.indices.delete(index=self.index_name, ignore=[400, 404])
        
    def add_corpus_to_index(self, corpus):  
        print(f"Adding documents to index \"{self.index_name}\"...")      
        actions = []
        
        for key in corpus.keys():
            actions.append({
                "_id": str(key),
                "_op_type": "index",
                "refresh": "wait_for",
                "title": corpus[key].get("title", None),
                "text": corpus[key].get("text", None),
            })
        for output in tqdm(streaming_bulk(client=self.es, index=self.index_name, actions=actions),
                           total=len(actions)):
            pass
    
    def search(self, query, size):
        req_body = {"query" : {"multi_match": {
                       "query": query, 
                       "type": "best_fields",
                       "fields": ["text", "title"],
                       "tie_breaker": 0.5
                       }}}
        res = self.es.search(search_type="dfs_query_then_fetch",
                        index = self.index_name, 
                        body = req_body, 
                        size = size)
        return res

