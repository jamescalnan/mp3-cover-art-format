import mutagen
import eyed3
from PIL import Image
from mutagen.id3 import ID3, APIC
from rich.console import Console
import os

c = Console()


def extract_cover_image(file_path, save_path):
    c.print(file_path)
    c.print(save_path)
    audiofile = eyed3.load(file_path)
    if audiofile.tag is None:
        c.print("No ID3 Tag in this file")
    else:
        if audiofile.tag.images:
            with open(save_path, 'wb') as img:
                img.write(audiofile.tag.images[0].image_data)
                c.print("Cover image saved as:", save_path)
        else:
            c.print("No cover image found in this file")

def square_crop_image(file_path, save_path):
    with Image.open(file_path) as im:
        width, height = im.size
        size = min(width, height)
        left = (width - size) / 2
        top = (height - size) / 2
        right = (width + size) / 2
        bottom = (height + size) / 2

        im = im.crop((left, top, right, bottom))
        im.save(save_path)
        c.print(f'Image saved as {save_path}')


files = [file for file in os.listdir() if file.split(".")[-1] == "mp3"]

c.print(files)

for file in files:
    c.print(f"Extracting cover: {file}")
    extract_cover_image(file, f'{file.replace(".mp3", "")}-image.jpg')


jpgFiles = [file for file in os.listdir() if file.split(".")[-1] == "jpg"]

for file in jpgFiles:
    c.print(f"Cropping {file}")
    square_crop_image(file, f'{file}-cropped_image.jpg')
