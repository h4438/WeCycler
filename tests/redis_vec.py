import sys
import os
sys.path.append(f'{os.path.dirname(__file__)}/../')
from botcore.redis_db import RedisDB
from botcore.test_data import TEST_WANTED_DATA, EXTRA_WANTED_DATA

redis_db = RedisDB()
data = TEST_WANTED_DATA

[redis_db.add_new_wanted(a) for a in data]
[redis_db.add_new_wanted(a) for a in EXTRA_WANTED_DATA]

print("UPLOAD DATA DONE")
