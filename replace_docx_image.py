import zipfile
import os
import shutil
from PIL import Image
import imagehash

hash_of_image_to_replace = imagehash.average_hash(Image.open('image_to_replace.jpeg')) 

def similar_images(path):
    hash_of_image_to_replace_with = imagehash.average_hash(Image.open(path)) 
    cutoff = 5  # maximum bits that could be different between the hashes. 
    if abs(hash_of_image_to_replace - hash_of_image_to_replace_with) < cutoff:
        print('images are similar')
        return True
    else:
        print('images are not similar')
        return False

similar_images('image_to_replace2.jpeg')

from image_scooper import scoop_image
# url = 'https://www.zales.com/ladies-25mm-wedding-band-14k-gold/p/V-20036320?cid=PLA-goo-E-Commerce+-+PLA+-+P2+-+Bridal+-+Rings&ds_rl=1252053&ds_rl=1252056&gclid=Cj0KCQiAyracBhDoARIsACGFcS4EPGgTWJsPHmfH6ExMNXOC61_0CvQgS7-vfqWms5TgQ3vR4P5nblYaAp6wEALw_wcB&gclsrc=aw.ds'
# url = 'https://www.jared.com/vera-wang-wish-diamond-band-2-carat-tw-14k-white-gold/p/V-141065401'
url = 'https://www.jared.com/le-vian-natural-emerald-ring-78-ct-tw-diamonds-14k-honey-gold/p/V-135389207'
example_image_bytes = scoop_image(url)

# get the hash of the image to replace
with open("image_to_replace.jpeg", 'rb') as f:
    image_to_replace_bytes = f.read()
    image_to_replace_hash = hash(image_to_replace_bytes)

def similar_images(bytes_of_image1, bytes_of_image2):
    # this function determines how similar two images are
    # it returns a number between 0 and 1, where 0 is completely different and 1 is exactly the same
    pass

def replace_image(input_docx, output_docx, hash_of_image_to_replace, bytes_of_image_to_replace_with):
    # this takes the bytes of the image to replace and the bytes of the image to replace it with,
    # the name of the docx file to replace the image in, and the name of the output docx file

    archive = zipfile.ZipFile('test.docx')
    for file in archive.filelist:
        # if file.filename.startswith('word/media/') and file.file_size > 30:
        archive.extract(file, 'extracted_docx')

    for file in os.listdir('extracted_docx\\word\\media'):
        if file.endswith('.png'):
            with open('extracted_docx\\word\\media\\' + file, 'rb') as f:
                image_bytes = f.read()
                image_hash = hash(image_bytes)
                if image_hash == hash_of_image_to_replace:
                    image_to_replace = file
                    print("Found it!!!")
                    break
    print("image_to_replace:", image_to_replace)

    with open("extracted_docx\\word\\media\\image2.png", 'wb') as f: # TODO: replace path with path of image to replace
        f.write(bytes_of_image_to_replace_with)

    shutil.make_archive('test2', 'zip', 'extracted_docx')

    if os.path.exists('test2.docx'):
        os.remove('test2.docx')

    os.rename('test2.zip', 'test2.docx')

if __name__ == "__main__":
    replace_image('test.docx', 'test2.docx', image_to_replace_hash, example_image_bytes)
    print("done")