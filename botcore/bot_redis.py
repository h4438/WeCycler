import redis
import os
from dotenv import load_dotenv
from langchain.schema import Document
from typing import List
import sys
sys.path.append(f"{os.path.dirname(__file__)}/../")
from botcore.setup import get_openai_embedding

def connect_redis(host: str = 'localhost', port: int = 6379):
    db = redis.Redis(host = host, port = port, decode_responses=True)
    return db

def test_redis(db):
    a = db.set('name', "Hieu")
    print('set:',a)
    b = db.get('name')
    print('get:',b)
    c = db.get('age')
    print('get:',c)


class BotRedis:

    def __init__(self):
        self.redis = None
        self.embedding = get_openai_embedding()
        self.index = "link"
        print('Redis client ready')
    
    def load_end_point(self):
        env_path = os.path.dirname(__file__)
        load_dotenv(f'{env_path}/../.streamlit/.env')
        key = os.getenv("REDIS_CLOUD")
        return key

    def add_doc(self, docs: List[Document]):

        if self.redis is None:
            key = self.load_end_point()
            rds = Redis.from_documents(docs, self.embedding, redis_url=key, index_name=self.index)
            self.redis = rds
            return True
        


if __name__ == '__main__':
    db = connect_redis()
    print("Running redis")
    test_redis(db)
