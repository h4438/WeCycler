import redis


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

if __name__ == '__main__':
    db = connect_redis()
    print("Running redis")
    test_redis(db)
