
import requests
from bs4 import BeautifulSoup as bs
import re
import webbrowser

# Given a url, this script will find the relevant ring image, download it, and return the bytes of the image

url = 'https://www.zales.com/ladies-25mm-wedding-band-14k-gold/p/V-20036320?cid=PLA-goo-E-Commerce+-+PLA+-+P2+-+Bridal+-+Rings&ds_rl=1252053&ds_rl=1252056&gclid=Cj0KCQiAyracBhDoARIsACGFcS4EPGgTWJsPHmfH6ExMNXOC61_0CvQgS7-vfqWms5TgQ3vR4P5nblYaAp6wEALw_wcB&gclsrc=aw.ds'
url = 'https://www.jared.com/vera-wang-wish-diamond-band-2-carat-tw-14k-white-gold/p/V-141065401'
url = 'https://www.jared.com/le-vian-natural-emerald-ring-78-ct-tw-diamonds-14k-honey-gold/p/V-135389207'

def scoop_image(url):
    # use a regular expression to grab just the home page url
    home_page = re.search('https?://[^/]+', url).group(0)
    print('homepage url:', home_page)
    print("complete url:", url)
    page = requests.get(url).text
    page = bs(page, 'html.parser')
    images = page.find_all('img')
    for image in images:
        if 'class="product-gallery-image"' in str(image):
            # print(image, str(image))
            ring_image = image
            break
    print(ring_image)
    ring_image_url = bs(str(ring_image))
    ring_image_url = home_page + str(ring_image_url.findAll('img')[0]['src'])
    webbrowser.open(ring_image_url)

    print('ring_image_url:', ring_image_url)
    if '.jpg' in ring_image_url:
        file_extension = '.jpg'
    elif '.png' in ring_image_url:
        file_extension = '.png'
    print('file_extension:', file_extension)
    ring_image = requests.get(ring_image_url).content
    with open(f"ring_image{file_extension}", 'wb') as f:
        f.write(ring_image)
    print("finished!")
    return ring_image

# test it out
scoop_image(url)