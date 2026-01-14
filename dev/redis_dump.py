import redis
import sys

# Configuration - Update these if needed
HOST = "localhost"
PORT = 6379
DB = 0  # Change to your database index
PASSWORD = None  # Set if your Redis requires authentication
DECODE = True  # Keep True for readable strings


def connect_to_redis():
    try:
        r = redis.Redis(
            host=HOST, port=PORT, db=DB, password=PASSWORD, decode_responses=DECODE
        )
        r.ping()
        print(f"Connected to Redis (host={HOST}, port={PORT}, db={DB})\n")
        return r
    except redis.ConnectionError as e:
        print(f"Error connecting to Redis: {e}")
        sys.exit(1)


def pretty_print_value(r, key):
    key_type = r.type(key)
    type_str = key_type.decode() if isinstance(key_type, bytes) else key_type
    print(f"Key: {key} | Type: {type_str}")

    if type_str == "string":
        value = r.get(key)
        print(f"  Value: {value}\n")

    elif type_str == "hash":
        value = r.hgetall(key)
        if not value:
            print("  (empty hash)\n")
        else:
            print("  Fields:")
            for field, val in value.items():
                print(f"    {field}: {val}")
            print()

    elif type_str == "list":
        value = r.lrange(key, 0, -1)
        print(f"  Length: {len(value)} | Elements:")
        for i, item in enumerate(value):
            print(f"    [{i}]: {item}")
        print()

    elif type_str == "set":
        value = r.smembers(key)
        members = sorted(value) if value else []
        print(f"  Members ({len(members)}): {members}\n")

    elif type_str == "zset":
        value = r.zrange(key, 0, -1, withscores=True)
        print(f"  Members ({len(value)}):")
        for member, score in value:
            print(f"    {member}: {score}")
        print()

    elif type_str == "stream":
        # Properly handle streams
        entries = r.xrange(key)  # Gets all entries
        info = r.xinfo_stream(key)

        print(f"  Stream Info:")
        print(f"    Length (entries): {info['length']}")
        print(
            f"    First Entry ID: {info.get('first-entry', [None, {}])[0] if info.get('first-entry') else 'N/A'}"
        )
        print(
            f"    Last Entry ID: {info.get('last-entry', [None, {}])[0] if info.get('last-entry') else 'N/A'}"
        )
        print(f"    Groups: {info['groups']}")

        if entries:
            print(f"  Entries ({len(entries)}):")
            for entry_id, fields in entries:
                print(f"    → ID: {entry_id}")
                for field, value in fields.items():
                    print(f"       {field}: {value}")
        else:
            print("  (no entries yet)")
        print()

    else:
        print(
            f"  Warning: Unsupported or unknown type: {type_str} (raw dump not shown)\n"
        )


def main():
    r = connect_to_redis()

    print("Scanning all keys in the database...\n")
    count = 0
    cursor = "0"
    while cursor != 0:
        cursor, keys = r.scan(cursor=cursor, count=100)
        for key in keys:
            if isinstance(key, bytes):
                key = key.decode()
            pretty_print_value(r, key)
            count += 1

    if count == 0:
        print("No keys found in this database.")
    else:
        print(f"Total keys scanned: {count}")


if __name__ == "__main__":
    main()
