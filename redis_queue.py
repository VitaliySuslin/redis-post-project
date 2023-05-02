import os
import redis
from PIL import Image
import glob


def put_images_to_redis(redis_config, images_config):
    r = redis.Redis(**redis_config)


    for image_path in glob.glob(os.path.join(images_config["folder_path"], "*")):
        try:
            with Image.open(image_path) as img:
                img.verify()
            with open(image_path, "rb") as f:
                image_data = f.read()
            r.lpush(images_config["queue_name"], image_data)
        except IOError:
            pass