import zipfile
import os
import shutil

from image_scooper import scoop_image
# url = 'https://www.zales.com/ladies-25mm-wedding-band-14k-gold/p/V-20036320?cid=PLA-goo-E-Commerce+-+PLA+-+P2+-+Bridal+-+Rings&ds_rl=1252053&ds_rl=1252056&gclid=Cj0KCQiAyracBhDoARIsACGFcS4EPGgTWJsPHmfH6ExMNXOC61_0CvQgS7-vfqWms5TgQ3vR4P5nblYaAp6wEALw_wcB&gclsrc=aw.ds'
# url = 'https://www.jared.com/vera-wang-wish-diamond-band-2-carat-tw-14k-white-gold/p/V-141065401'
url = 'https://www.jared.com/le-vian-natural-emerald-ring-78-ct-tw-diamonds-14k-honey-gold/p/V-135389207'
example_image_bytes = scoop_image(url)



def replace_image(input_docx, output_docx, bytes_of_image_to_replace, bytes_of_image_to_replace_with):
    # this takes the bytes of the image to replace and the bytes of the image to replace it with,
    # the name of the docx file to replace the image in, and the name of the output docx file

    archive = zipfile.ZipFile('test.docx')
    for file in archive.filelist:
        # if file.filename.startswith('word/media/') and file.file_size > 30:
        archive.extract(file, 'extracted_docx')

    with open("extracted_docx\\word\\media\\image2.png", 'wb') as f:
        f.write(bytes_of_image_to_replace_with)

    shutil.make_archive('test2', 'zip', 'extracted_docx')

    if os.path.exists('test2.docx'):
        os.remove('test2.docx')

    os.rename('test2.zip', 'test2.docx')

