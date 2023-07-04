import sys
import os
sys.path.append(f'{os.path.dirname(__file__)}/../')
from botcore.bot_redis import RedisVectorDB
from botcore.test_data import TEST_WANTED_DATA 

redis_db = RedisVectorDB()
data = TEST_WANTED_DATA

[redis_db.add_new_wanted(a) for a in data]

b = redis_db.search_wanted("I have an old Asus laptop. It has 8 GB RAM.")
print(b)
