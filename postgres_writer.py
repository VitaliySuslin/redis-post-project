import psycopg2
import redis
from datetime import datetime


def process_image_queue(redis_config, postgres_config):
    r = redis.Redis(**redis_config)

    conn = psycopg2.connect(**postgres_config)
    cur = conn.cursor()

    while True:
        image_data = r.rpop("image_queue")
        if not image_data:
            break
        image_size = len(image_data)
        created_at = datetime.utcnow()
        cur.execute("INSERT INTO images (created_at, size) VALUES (%s, %s)", (created_at, image_size))
        conn.commit()
    cur.close()
    conn.close()