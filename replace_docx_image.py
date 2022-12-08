import zipfile
import os
import shutil
from PIL import Image
import imagehash
from image_scooper import scoop_image
import time
from grab_sku_from_docx import grab_sku_from_docx
from tqdm import tqdm
from urls_of_skus import search_skus

image_limit = 4 # the maximum number of images in a document for it to be valid to replace the image
verbose = False

# get the image to replace ready
path_of_image_to_replace = 'image_to_replace.jpeg'
hash_of_image_to_replace = imagehash.average_hash(Image.open(path_of_image_to_replace)) 

# get a sample replacement ready
carl = Image.open('carl.jpeg')

def similar_images(path:str) -> bool:
    # this takes the path of an image and returns True if it is similar to the image to replace
    if verbose: print('path:', path)
    hash_of_image_to_replace_with = imagehash.average_hash(Image.open(path))
    cutoff = 5  # maximum bits that could be different between the hashes. 
    if abs(hash_of_image_to_replace - hash_of_image_to_replace_with) < cutoff:
        if verbose: print('images are similar')
        return True
    else:
        if verbose: print('images are not similar')
        return False

from image_scooper import scoop_image
some_14k_ring_url = 'https://www.zales.com/ladies-25mm-wedding-band-14k-gold/p/V-20036320?cid=PLA-goo-E-Commerce+-+PLA+-+P2+-+Bridal+-+Rings&ds_rl=1252053&ds_rl=1252056&gclid=Cj0KCQiAyracBhDoARIsACGFcS4EPGgTWJsPHmfH6ExMNXOC61_0CvQgS7-vfqWms5TgQ3vR4P5nblYaAp6wEALw_wcB&gclsrc=aw.ds'
vera_wang_url = 'https://www.jared.com/vera-wang-wish-diamond-band-2-carat-tw-14k-white-gold/p/V-141065401'

def replace_image(input_docx:str, output_docx:str, image_to_replace_with:Image) -> bool:
    '''
    This takes the name of the docx file to replace the image in, the name of the output docx file
    and the Image object of the image to replace it with
    and returns True if it was successful and False if it was not
    '''
    archive = zipfile.ZipFile(f'{input_docx}.docx')
    for file in archive.filelist:
        # if file.filename.startswith('word/media/') and file.file_size > 30:
        archive.extract(file, 'extracted_docx')
    image_count = 0
    found_similar_image = False
    for file in os.listdir('extracted_docx\\word\\media'):
        if file.endswith('.png') or file.endswith(".jpg") or file.endswith(".jpeg"):
            image_count += 1
            if image_count > image_limit:
                if verbose: print("More than one image found, exiting")
                return False
            if similar_images(f"extracted_docx\\word\\media\\{file}"):
                image_to_replace = file
                if verbose: print("Found it!!!")
                found_similar_image = True
                break
    if verbose: print(f"image_count: {image_count}")
    if found_similar_image:
        if verbose: print("image_to_replace:", image_to_replace)
    else:
        if verbose: print("image not found")
        return False
    image_to_replace_with.save(f"extracted_docx\\word\\media\\{image_to_replace}", "JPEG")

    shutil.make_archive(f'{output_docx}', 'zip', 'extracted_docx')

    if os.path.exists(f'{output_docx}.docx'):
        os.remove(f'{output_docx}.docx')

    os.rename(f'{output_docx}.zip', f'{output_docx}.docx')
    return True

if __name__ == "__main__":
    for file in tqdm(os.listdir('input_docx'), desc='replacing images...'):
        if file.endswith('.docx'):
            # grab the sku from the docx file
            sku = grab_sku_from_docx(f'input_docx\\{file[:-5]}')
            if not sku:
                if verbose: print(f'no sku found for {file}')
                continue
            if verbose: print('sku:', sku)
            # grab the url of the sku TODO: get rid of redundant calls to search_skus if image already exists
            ring_picture = scoop_image(sku = sku)
            if ring_picture != None:
                print("Ring picture already exists!")
                replace_image(f'input_docx\\{file[:-5]}', f'output_docx\\{file[:-5]}', ring_picture)
                continue
            urls = search_skus([sku])
            if len(urls) == 0:
                if verbose: print(f'no urls found for {sku}')
                continue
            url = urls[0]
            # scoop the image from the sku, persist for 100 seconds if it fails
            start = time.time()
            end = start + 100
            while time.time() < end:
                try:
                    ring_picture = scoop_image(url = url, sku = sku)
                    break
                except Exception as e:
                    if verbose: print(f'error scooping image from {url}: {e}')
                    time.sleep(1)
            # if the image was not scooped, continue to the next docx file
            if ring_picture is None:
                if verbose: print(f'no image found for {sku}')
                continue
            replace_image(f'input_docx\\{file[:-5]}', f'output_docx\\{file[:-5]}', ring_picture)
    # for every docx file in the input_docx folder, copy the ones that don't already exist in the output_docx folder
    # to the output_docx folder, use tqdm to show progress and make it say "copying over docx files"

    for file in tqdm(os.listdir('input_docx'), desc='copying over unmodified docx files'):
        if file.endswith('.docx'):
            if not os.path.exists(f'output_docx\\{file[:-5]}.docx'):
                shutil.copyfile(f'input_docx\\{file}', f'output_docx\\{file}')
    # open up the output_docx folder
    os.startfile('output_docx')