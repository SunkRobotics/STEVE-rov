from exif import Image
import os

# directory = "rpi-image-more-metadata"
directory = "images"
for file in os.listdir(directory):
    filename = os.fsdecode(file)
    print(filename)
    image = Image(f"{directory}/{filename}")
    image.model = "fdskfdsaljfsafdsafdsafdsaasdfkjhgasdfkjgasdfkjgasdkfjgasdf"
    # image.focal = "2.75"
    # image.focal_length_in_35mm_film = "15"
    # image.x_resolution = 72
    # image.y_resolution = 72
    # image.resolution_unit = "inches"
    with open(f"{directory}/{filename}", 'wb') as f:
        print(f"Writing image{filename}...")
        f.write(image.get_file())
