import redis

def list_redis_databases(
    host="localhost",
    port=6379,
    password=None,
    db=0
):
    r = redis.Redis(
        host=host,
        port=port,
        password=password,
        db=db,
        decode_responses=True
    )

    info = r.info("keyspace")

    if not info:
        print("No databases with keys found.")
        return

    print("Redis databases:")
    for db_name, stats in info.items():
        print(
            f"- {db_name} | "
            f"keys={stats.get('keys')} | "
            f"expires={stats.get('expires')} | "
            f"avg_ttl={stats.get('avg_ttl')}"
        )

if __name__ == "__main__":
    list_redis_databases()

