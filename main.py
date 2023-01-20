import mutagen
import eyed3
from PIL import Image
from mutagen.id3 import ID3, APIC
from mutagen.mp3 import MP3
from rich.console import Console
import os

c = Console()


def extract_cover_image(file_path, save_path):
    c.print(file_path)
    c.print(save_path)
    audiofile = eyed3.load(file_path)
    try:

        if audiofile.tag is None:
            c.print("No ID3 Tag in this file")
        else:
            if audiofile.tag.images:
                with open(save_path, 'wb') as img:
                    img.write(audiofile.tag.images[0].image_data)
                    c.print("Cover image saved as:", save_path)
            else:
                c.print("No cover image found in this file")
    except AttributeError as e:
        c.print(e)

def remove_black_bars(file_path, save_path):
    try:
        with Image.open(file_path) as im:
            # Convert the image to grayscale
            im_copy = im.convert("L")
            
            # Get the image width and height
            width, height = im_copy.size
            # Create an empty list to store the pixel values of the top and bottom rows
            top_pixels = []
            bottom_pixels = []

            for i in range(int(height/2)):
                # c.print(im.getpixel((0, i)))
                top_pixels.append(im_copy.getpixel((0, i)))
                bottom_pixels.append(im_copy.getpixel((0, (height-1) - i)))


            # Iterate over the top and bottom rows of the image
            # Get the average pixel value of the top and bottom rows
            top_avg = sum(top_pixels) / len(top_pixels)
            bottom_avg = sum(bottom_pixels) / len(bottom_pixels)
            
            # Get the position of the first non-black pixel from the top and bottom
            top_pos = 0
            bottom_pos = 0
            for i, brightness_val in enumerate(top_pixels):
                if brightness_val not in [0,1,2,3]:
                    top_pos = i
                    break
            for i, brightness_val in enumerate(top_pixels):
                if brightness_val not in [0,1,2,3]:
                    bottom_pos = (height -1) - i
                    break
            

            # Print the top_pos and bottom_pos to check if they are within the bounds of the image
            im = im.convert("RGB")
            
            # Crop the image
            im = im.crop((0, top_pos + 5, width, bottom_pos - 5))

            im.save(save_path)
    except SystemError as e:
        c.print(e)


def square_crop_image(file_path, save_path):
    try:
        with Image.open(file_path) as im:
            width, height = im.size
            size = min(width, height)
            left = (width - size) / 2
            top = (height - size) / 2
            right = (width + size) / 2
            bottom = (height + size) / 2

            im = im.crop((left, top, right, bottom))
            im.save(save_path)
            print(f'Image saved as {save_path}')
    except:
        c.print("[red]error")

files = [file for file in os.listdir() if file.split(".")[-1] == "mp3"]

c.print(files)

for file in files:
    c.print(f"Extracting cover: {file}")
    extract_cover_image(file, f'C:/Users/James/Desktop/kms/images/{file.replace(".mp3", "")}.jpg')


jpgFiles = [file for file in os.listdir("C:/Users/James/Desktop/kms/images/") if file.split(".")[-1] == "jpg"]

c.print(jpgFiles)
input()
for file in jpgFiles:
    c.print(f"Cropping {file}")
    remove_black_bars(f'C:/Users/James/Desktop/kms/images/{file}', f'C:/Users/James/Desktop/kms/cropped/{file}')

croppedFiles = [file for file in os.listdir("C:/Users/James/Desktop/kms/cropped/") if file.split(".")[-1] == "jpg"]

c.print(croppedFiles)

for file in croppedFiles:
    c.print(f"squaring: {file}")
    square_crop_image(f'C:/Users/James/Desktop/kms/cropped/{file}', f'C:/Users/James/Desktop/kms/finished/{file}')


full_songs = os.listdir("C:/Users/James/Desktop/kms/songs")




def string_match(string1, string2):
    # Get the length of the shorter string
    shorter_length = min(len(string1), len(string2))
    matching_characters = 0

    # Iterate over the characters of the shorter string
    for i in range(shorter_length):
        if string1[i] == string2[i]:
            matching_characters += 1

    # Calculate the percentage of similarity
    similarity = (matching_characters / shorter_length) * 100

    return similarity

def findMatchingAlbumCover(songName):
    available_Covers = os.listdir("C:/Users/James/Desktop/kms/cropped/")

    for availableCover in available_Covers:
        match = string_match(songName, availableCover)
        if match > 50:
            return availableCover

    return None

c.print("\n\n\n\n")

for songName in full_songs:
    try:
        songCover = findMatchingAlbumCover(songName)

        audio = ID3(f"C:/Users/James/Desktop/kms/songs/{songName}")

        audiofile = MP3(f"C:/Users/James/Desktop/kms/songs/{songName}")
        picture_path = f"C:/Users/James/Desktop/kms/finished/{songCover}"

        keys_to_pop = ["COMM:ID3v1 Comment:eng", "TXXX:Description", "COMM::eng", "APIC:cover.jpg", "APIC:Cover (front)"]

        for key_to_pop in keys_to_pop:
            try:
                audiofile.pop(key_to_pop)
                c.print(f"[green]Succeeded in removing: {key_to_pop}")
            except Exception as e:
                c.print(f"[red]Failed to remove : {key_to_pop}")


        audiofile.tags.add(APIC(mime='image/jpeg', type=3, desc=u'Cover (front)', data=open(picture_path, 'rb').read()))

        audiofile.save()

        # c.print(f"{songName} : {findMatchingAlbumCover(songName)}")
        c.print(f"[green]Songname: {songName}")
    except Exception as e:
        c.print(f"[red]error: {e}")