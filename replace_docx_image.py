import zipfile
import os
import shutil
from PIL import Image
import imagehash
from image_scooper import scoop_image
from time import time
from grab_sku_from_docx import grab_sku_from_docx
from tqdm import tqdm
from urls_of_skus import search_skus

# get the image to replace ready
path_of_image_to_replace = 'image_to_replace.jpeg'
hash_of_image_to_replace = imagehash.average_hash(Image.open(path_of_image_to_replace)) 

# get a sample replacement ready
carl = Image.open('carl.jpeg')

def similar_images(path) -> bool:
    # this takes the path of an image and returns True if it is similar to the image to replace
    print('path:', path)
    hash_of_image_to_replace_with = imagehash.average_hash(Image.open(path))
    cutoff = 5  # maximum bits that could be different between the hashes. 
    if abs(hash_of_image_to_replace - hash_of_image_to_replace_with) < cutoff:
        print('images are similar')
        return True
    else:
        print('images are not similar')
        return False

from image_scooper import scoop_image
some_14k_ring_url = 'https://www.zales.com/ladies-25mm-wedding-band-14k-gold/p/V-20036320?cid=PLA-goo-E-Commerce+-+PLA+-+P2+-+Bridal+-+Rings&ds_rl=1252053&ds_rl=1252056&gclid=Cj0KCQiAyracBhDoARIsACGFcS4EPGgTWJsPHmfH6ExMNXOC61_0CvQgS7-vfqWms5TgQ3vR4P5nblYaAp6wEALw_wcB&gclsrc=aw.ds'
vera_wang_url = 'https://www.jared.com/vera-wang-wish-diamond-band-2-carat-tw-14k-white-gold/p/V-141065401'
# example_image_bytes = scoop_image(url)


def replace_image(input_docx, output_docx, image_to_replace_with) -> bool:
    # this takes the name of the docx file to replace the image in, the name of the output docx file
    # and the Image object of the image to replace it with
    archive = zipfile.ZipFile(f'{input_docx}.docx')
    for file in archive.filelist:
        # if file.filename.startswith('word/media/') and file.file_size > 30:
        archive.extract(file, 'extracted_docx')
    image_count = 0
    found_similar_image = False
    for file in os.listdir('extracted_docx\\word\\media'):
        if file.endswith('.png') or file.endswith(".jpg") or file.endswith(".jpeg"):
            image_count += 1
            if image_count > 1:
                print("More than one image found, exiting")
                return False
            if similar_images(f"extracted_docx\\word\\media\\{file}"):
                image_to_replace = file
                print("Found it!!!")
                found_similar_image = True
                break
    print(f"image_count: {image_count}")
    if found_similar_image:
        print("image_to_replace:", image_to_replace)
    else:
        print("image not found")
        return False
    image_to_replace_with.save(f"extracted_docx\\word\\media\\{image_to_replace}", "JPEG")

    shutil.make_archive(f'{output_docx}', 'zip', 'extracted_docx')

    if os.path.exists(f'{output_docx}.docx'):
        os.remove(f'{output_docx}.docx')

    os.rename(f'{output_docx}.zip', f'{output_docx}.docx')
    return True

if __name__ == "__main__":
    # start = time()
    # # put carl on there
    # replace_image('test', 'test2', carl)
    # # test it with a scooped image (vera wang)
    # replace_image('test', 'test3', scoop_image(vera_wang_url))
    # # test it with a scooped image (some 14k ring)
    # replace_image('test', 'test4', scoop_image(some_14k_ring_url))
    # end = time()
    # print(f"Time taken: {end - start}")
    # print("done")
    # for every docx file in the input_docx folder, replace the image in it with the image_to_replace and
    # put it in the output_docx folder
    for file in os.listdir('input_docx'):
        if file.endswith('.docx'):
            # grab the sku from the docx file
            sku = grab_sku_from_docx(f'input_docx\\{file[:-5]}')
            print('sku:', sku)
            # grab the url of the sku
            urls = search_skus([sku])
            if len(urls) == 0:
                print(f'no urls found for {sku}')
                continue
            url = urls[0]
            # scoop the image from the sku
            ring_picture = scoop_image(url)
            replace_image(f'input_docx\\{file[:-5]}', f'output_docx\\{file[:-5]}', ring_picture)