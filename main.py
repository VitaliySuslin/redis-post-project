import threading
import yaml

from redis_queue import put_images_to_redis
from postgres_writer import process_image_queue


if __name__ == "__main__":
    with open("config.yml", "r") as f:
        config = yaml.safe_load(f)

    threading.Thread(target=put_images_to_redis, args=(config["redis"], config["images"])).start()
    threading.Thread(target=process_image_queue, args=(config["redis"], config["postgres"])).start()
