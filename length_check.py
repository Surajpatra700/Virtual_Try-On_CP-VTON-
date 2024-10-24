import os
from PIL import Image

directory = "C:\\Users\\suraj\\OneDrive\\Desktop\\Program Files\\cp-vton+_network\\cp-vton-plus-2\\data\\test\\cloth"

def count_images(directory):
    image_count = 0
    for filename in os.listdir(directory):
        # Check if the file is an image file based on its extension
        if filename.endswith('.jpg') or filename.endswith('.jpeg') or filename.endswith('.png') or filename.endswith('.gif'):
            try:
                # Attempt to open the file as an image
                with Image.open(os.path.join(directory, filename)) as img:
                    image_count += 1
            except (IOError, OSError):
                # Handle any errors that occur when trying to open the file
                pass
    return image_count

image_count = count_images(directory)
print(f"Number of images in {directory}: {image_count}")