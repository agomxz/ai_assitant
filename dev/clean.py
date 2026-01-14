import redis

def clean_redis_db(
    host="localhost",
    port=6379,
    db=0,
    password=None,
):
    r = redis.Redis(
        host=host,
        port=port,
        db=db,
        password=password,
        decode_responses=True,
    )

    r.flushdb()
    print(f"Redis DB {db} cleaned successfully")


if __name__ == "__main__":
    clean_redis_db()
