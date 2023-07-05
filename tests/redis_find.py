import sys
import os
sys.path.append(f'{os.path.dirname(__file__)}/../')
from botcore.bot_redis import RedisDB

redis_db = RedisDB()

data = {"title": "I have an old phone",'product':"phone", "features": ["My phone has 4 GB RAM", "Is it function well? Well"]}
b = redis_db.search_in_wanted(data)
print(b)
