
import requests
from bs4 import BeautifulSoup as bs
import re
import webbrowser
from PIL import Image
import os
from urls_of_skus import search_sku
from google_sku import google_sku

# Given a url, this script will find the relevant ring image, download it, and return the bytes of the image

url = 'https://www.zales.com/ladies-25mm-wedding-band-14k-gold/p/V-20036320?cid=PLA-goo-E-Commerce+-+PLA+-+P2+-+Bridal+-+Rings&ds_rl=1252053&ds_rl=1252056&gclid=Cj0KCQiAyracBhDoARIsACGFcS4EPGgTWJsPHmfH6ExMNXOC61_0CvQgS7-vfqWms5TgQ3vR4P5nblYaAp6wEALw_wcB&gclsrc=aw.ds'
url = 'https://www.jared.com/vera-wang-wish-diamond-band-2-carat-tw-14k-white-gold/p/V-141065401'
# url = 'https://www.jared.com/le-vian-natural-emerald-ring-78-ct-tw-diamonds-14k-honey-gold/p/V-135389207'
url = 'https://www.kay.com/labcreated-diamonds-by-kay-anniversary-band-115-ct-tw-10k-yellow-gold/p/V-182819007'
url = 'https://www.zalesoutlet.com/oval-emerald-white-labcreated-sapphire-frame-ring-10k-gold/p/V-20509163'
def scoop_image(url:str = '', sku:str = '',
                verbose:bool = False, testing:bool = False):
    '''
    Given a url, this script will find the relevant ring image, download it, and return an Image object
    If the search is unsuccessful, it will return None
    If a sku is given, search for a relevant picture in folder 'sku_images'
    '''
    if not url and not sku:
        print("Error: no url or sku given")
        return None
    if sku:
        # search for a relevant picture in folder 'sku_images'
        # if there's no sku_images folder, create one
        if not os.path.exists('sku_images'):
            os.mkdir('sku_images')
        for file in os.listdir('sku_images'):
            if sku == file.split('.')[0]:
                print(f"Found image for {sku} in folder 'sku_images'")
                return Image.open(f'sku_images/{file}')
    if sku and not url:
        urls = search_sku(sku)
        if len(urls) == 0:
            print("Error: no url found from search functionality on sites")
            print("Trying DuckDuckGo...")
            url = google_sku(sku)
            if not url:
                print("Couldn't find the SKU on DuckDuckGo either.")
                print("Giving up.")
                return None
        print("Result of SKU url search:\n", "\n".join(urls))
        # just use the first url found if multiple are found
        if not url:
            url = urls[0]
    # scoops the image up from the given url
    # use a regular expression to grab just the home page url
    home_page = re.search('https?://[^/]+', url).group(0)
    print('homepage url:', home_page)
    print("complete url:", url)
    page = requests.get(url).text
    page = bs(page, 'html.parser')
    images = page.find_all('img')
    for i, image in enumerate(images):
        # print(str(i + 1) + " " + str(image))
        if 'class="product-gallery-image' in str(image):
            # print(image, str(image))
            ring_image = image
            break
    print(ring_image)
    ring_image_url = bs(str(ring_image), features="lxml")
    ring_image_url = home_page + str(ring_image_url.findAll('img')[0]['src'])
    if testing:
        webbrowser.open(ring_image_url)

    print('ring_image_url:', ring_image_url)
    if '.jpg' in ring_image_url:
        file_extension = '.jpg'
    elif '.png' in ring_image_url:
        file_extension = '.png'
    print('file_extension:', file_extension)
    # save the image from ring_image_url
    ring_image = requests.get(ring_image_url).content
    with open(f"ring_image{file_extension}", 'wb') as f:
        f.write(ring_image)
    ring_image = Image.open(f"ring_image{file_extension}")
    # if there's a sku provided, save the image in the sku_images folder
    if sku:
        ring_image.save(f"sku_images\\{sku}{file_extension}")
    print("finished scooping!")
    return ring_image

# test it out
if __name__ == '__main__':
    # scoop_image(url = url, sku = 'test123')
    print("Testing image scooper...")
##    test_skus = ['20509163',
##             '20344860',
##             '20283669',
##             '141365510'
##             ]
    # get the skus from active_containers_without_image.csv
    with open("active_parts_2.csv") as f:
        test_skus = f.read().split()
    test_skus = [sku.lstrip('0') for sku in test_skus][1:]
    print(test_skus)
##    with open("sku_list.txt", "r") as f:
##        test_skus = f.read().split('\n')
    for test_sku in test_skus:
        try:
            scoop_image(sku = test_sku)
        except Exception as e:
            print(f"Had some trouble with {test_sku}: {e}")
    print("...Done!")
