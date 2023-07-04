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

def connect_redis(host: str = 'localhost', port: int = 6379):
    db = redis.Redis(host = host, port = port, decode_responses=True)
    return db


class RedisVectorDB:

    def __init__(self):
        load_my_env()
        self.embeddings = get_openai_embeddings()
        self.url = os.getenv("REDIS_CLOUD")
        self.redis = {'wanted': None, 'stock': None}
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
        return self.add_new_doc(doc, 'wanted')

    def add_new_stock(self, data: Dict):
        doc = self.json_to_doc(data, {"type": "stock"})
        return self.add_new_doc(doc, 'stock')
    
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
        if self.redis is None:
            print("Redis is not initialized. Please add a document first")
            return False
        doc = self.json_to_doc(data, {"type": index_name})
        query = doc.page_content
        try:
            results = self.redis[index_name].similarity_search_limit_score(query, score_threshold=self.limit)
            return results
        except:
            print("Error occurred when finding documents")
            return False
