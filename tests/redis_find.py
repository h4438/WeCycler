import sys
import os
sys.path.append(f'{os.path.dirname(__file__)}/../')
from botcore.redis_db import RedisDB

redis_db = RedisDB()
data = {"title": "I have an old laptop","product":"laptop", "features": ["My laptop has 4 GB RAM", "Is it function well? Well", "Does it have warranty: Yes"]}
data = {"title": "I have a TV", "product": "TV", "features": ["Does the TV still working? Very well", "Does it have any damages? It is still fine"]}
b = redis_db.search_in_wanted(data)
print(b)
