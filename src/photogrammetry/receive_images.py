import exif
import os
from pathlib import Path
import shutil
from datetime import datetime
from websockets.sync.client import connect

IMAGES_DIR = Path(__file__).parent.resolve().as_posix() + "/images/"


def main():
    if os.path.isdir(IMAGES_DIR):
        shutil.rmtree(IMAGES_DIR)
        os.mkdir(IMAGES_DIR)

    with connect("ws://192.168.100.2:3000") as websocket:
        count = 0
        image_num = 0
        for message in websocket:
            if count % 10 == 0:
                image = exif.Image(message)
                image.model = "imx708_wide"
                image.lens_model = "imx708_wide"
                image.focal_length = "2.75"
                image.make = "Raspberry Pi"
                image.datetime_original = (
                    datetime.now().strftime("%Y:%m:%d %H:%M:%S.%f")
                )
                with open(f'{IMAGES_DIR}image{image_num}.jpg', 'wb') as f:
                    print(f"Writing image{image_num}.jpg...")
                    f.write(image.get_file())

                image_num += 1
            count += 1


if __name__ == "__main__":
    main()
