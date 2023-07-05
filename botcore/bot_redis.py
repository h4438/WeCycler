import redis
import os
from dotenv import load_dotenv
from langchain.schema import Document
from typing import List, Dict
import json
from langchain.vectorstores.redis import Redis
import sys
sys.path.append(f"{os.path.dirname(__file__)}/../")
from botcore.setup import get_openai_embeddings, load_my_env

def connect_redis():
    load_my_env()
    host = os.getenv("REDIS_HOST")
    password = os.getenv("REDIS_PASS")
    port = os.getenv("REDIS_PORT")
    db = redis.Redis(host = host, port = port, password=password, decode_responses=True)
    return db

class RedisDB:

    def __init__(self):

        load_my_env()
        self.embeddings = get_openai_embeddings()
        self.url = os.getenv("REDIS_CLOUD")
        self.limit = 0.2

    def json_to_doc(self, data: Dict, meta_info: Dict = None) -> Document:
        """
            data = {"title": str, "features": [], "post_id": str, ...}
        """
        feats = ", ".join([i for i in data['features']])
        txt = f"{data['title']}. {feats}"
        return Document(page_content=txt, metadata=meta_info)

    def add_doc(self, doc: Document, index_name: str):
        try:
            
            Redis.from_documents([doc], self.embeddings, redis_url=self.url, index_name=index_name)

            return True
        except:
            print("An exception occurred when adding new doc")
            return False

    ## add
    def add_new_wanted(self, data: Dict):
        p =  data["product"].replace(" ","_")
        index = f"wanted:{p}"
        doc = self.json_to_doc(data, {"type": index})
        return self.add_doc(doc, index)

    def add_new_stock(self, data: Dict):
        p =  data["product"].replace(" ","_")
        index = f"stock:{p}"
        doc = self.json_to_doc(data, {"type": index})
        return self.add_doc(doc, index)
        
    ## search
    def search_in_wanted(self, data: Dict):
        p =  data["product"].replace(" ","_")
        index = f"wanted:{p}"
        return self.search_doc(data, index)

    def search_in_stock(self, data: Dict):
        p =  data["product"].replace(" ","_")
        index = f"stock:{p}"
        return self.search_doc(data, index)

    def search_doc(self, data: Dict, index_name: str):
        redis = Redis(redis_url = self.url, index_name = index_name,\
                    embedding_function=self.embeddings.embed_query)
        
        doc = self.json_to_doc(data, {"type": index_name})
        query = doc.page_content
        try:
            print("Start searching")
            results = redis.similarity_search_limit_score(query, score_threshold=self.limit)
            return results
        except:
            print("Error occurred when finding documents")
            return False


class RedisVectorDB:

    def __init__(self):
        load_my_env()
        self.embeddings = get_openai_embeddings()
        self.url = os.getenv("REDIS_CLOUD")
        
        self.redis = {}
        self.redis['wanted'] = Redis(redis_url = self.url, index_name = "wanted",\
                embedding_function=self.embeddings.embed_query)
        self.redis['stock'] = Redis(redis_url = self.url, index_name = "stock",\
                embedding_function=self.embeddings.embed_query)
        
        self.limit = 0.2
        print("Vector DB is ready")
    
    def json_to_doc(self, data: Dict, meta_info: Dict = None) -> Document:
        """
            data = {"title": str, "features": [], "post_id": str, ...}
        """
        feats = ", ".join([i for i in data['features']])
        txt = f"{data['title']}. {feats}"
        return Document(page_content=txt, metadata=meta_info)

    ## add
    def add_new_wanted(self, data: Dict):
        doc = self.json_to_doc(data, {"type": "wanted"})
        return self.add_doc(doc, 'wanted')

    def add_new_stock(self, data: Dict):
        doc = self.json_to_doc(data, {"type": "stock"})
        return self.add_doc(doc, 'stock')
    
    def add_doc(self, doc: Document, index_name: str):
        try:
            self.redis[index_name].add_documents([doc])
            return True
        except:
            print("An exception occurred when adding new doc")
            return False

    def add_new_doc(self, doc: Document, index_name: str):
        try:
            if self.redis[index_name] is None:
                self.redis[index_name] = Redis.from_documents([doc], self.embeddings, redis_url=self.url, index_name=index_name)
            else: 
                self.redis[index_name].add_documents([doc])
            return True
        except:
            print("An exception occurred when adding document") 
            return False
    
    ## search
    def search_stock(self, wanted_data: str):
        return self.search_doc(wanted_data, "stock")

    def search_wanted(self, stock_data: Dict):
        return self.search_doc(stock_data, 'wanted')

    def search_doc(self, data: Dict, index_name: str):
        self.add_new_stock(data)
        doc = self.json_to_doc(data, {"type": index_name})
        query = doc.page_content
        try:
            results = self.redis[index_name].similarity_search_limit_score(query, score_threshold=self.limit)
            return results
        except:
            print("Error occurred when finding documents")
            return False
