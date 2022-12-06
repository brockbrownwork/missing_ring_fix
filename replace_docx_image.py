import zipfile
import os
import shutil
from PIL import Image
import imagehash

hash_of_image_to_replace = imagehash.average_hash(Image.open('image_to_replace.jpeg')) 

bytes_of_image_to_replace_with = open('image_to_replace_with.jpeg', 'rb').read()

def similar_images(path):
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
# url = 'https://www.zales.com/ladies-25mm-wedding-band-14k-gold/p/V-20036320?cid=PLA-goo-E-Commerce+-+PLA+-+P2+-+Bridal+-+Rings&ds_rl=1252053&ds_rl=1252056&gclid=Cj0KCQiAyracBhDoARIsACGFcS4EPGgTWJsPHmfH6ExMNXOC61_0CvQgS7-vfqWms5TgQ3vR4P5nblYaAp6wEALw_wcB&gclsrc=aw.ds'
# url = 'https://www.jared.com/vera-wang-wish-diamond-band-2-carat-tw-14k-white-gold/p/V-141065401'
url = 'https://www.jared.com/le-vian-natural-emerald-ring-78-ct-tw-diamonds-14k-honey-gold/p/V-135389207'
# example_image_bytes = scoop_image(url)


def replace_image(input_docx, output_docx):
    # this takes the bytes of the image to replace and the bytes of the image to replace it with,
    # the name of the docx file to replace the image in, and the name of the output docx file

    archive = zipfile.ZipFile(f'{input_docx}.docx')
    for file in archive.filelist:
        # if file.filename.startswith('word/media/') and file.file_size > 30:
        archive.extract(file, 'extracted_docx')

    found_similar_image = False
    for file in os.listdir('extracted_docx\\word\\media'):
        if file.endswith('.png') or file.endswith(".jpg") or file.endswith(".jpeg"):
            if similar_images(f"extracted_docx\\word\\media\\{file}"):
                image_to_replace = file
                print("Found it!!!")
                found_similar_image = True
                break
    if found_similar_image:
        print("image_to_replace:", image_to_replace)
    else:
        print("image not found")
        return False

    with open(f"extracted_docx\\word\\media\\{image_to_replace}", 'wb') as f: # TODO: replace path with path of image to replace
        f.write(bytes_of_image_to_replace_with)

    shutil.make_archive(f'{output_docx}', 'zip', 'extracted_docx')

    if os.path.exists(f'{output_docx}.docx'):
        os.remove(f'{output_docx}.docx')

    os.rename(f'{output_docx}.zip', f'{output_docx}.docx')
    return True

if __name__ == "__main__":
    replace_image('test', 'test2')
    print("done")