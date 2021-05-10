import os

from tqdm import tqdm
from PIL import Image

from pathlib import Path
from panimg import convert

root_folder = os.path.join('/mnt/d/Random/CHAOS_Train_Sets/Train_Sets/MR/')

def remove_all_but_spleen(image):
    image_data = image.load()
    height,width = image.size

    for x in range(width):
        for y in range(height):
            c = image_data[x, y]
            if(c < 240):
                image_data[x, y] = 0
            else:
                image_data[x, y] = 255
    
    image.save(image.filename)
    # print("Saved a new version of ", image.filename)

def fix_all_images():
    for image_folder in tqdm(os.listdir(root_folder)):
        labels = os.path.join(root_folder, image_folder, 'T2SPIR/Ground/')

        for f in os.listdir(labels):
            remove_all_but_spleen(Image.open(os.path.join(labels, f)))


def convert_all_images_to_mha():
    for image_folder in tqdm(os.listdir(root_folder)):
        Path(root_folder, image_folder, "T2SPIR_conv/Ground").mkdir(parents=True, exist_ok=True)
        convert(
            input_directory=Path(root_folder, image_folder, "T2SPIR/Ground"),
            output_directory=Path(root_folder, image_folder, "T2SPIR_conv/Ground"),
        )

#fix_all_images()
convert_all_images_to_mha()
