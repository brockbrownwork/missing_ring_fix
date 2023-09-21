Okay, this is set up like this:

urls_of_skus.py has a function called search_skus. It takes a list of skus, and then it iterates through each of those, and returns the list of skus

So the idea is you'll want to feed the list of urls from 

urls_of_skus.search_skus(list_of_skus) → image_scooper.scoop_image(url = some_url, sku = sku)

So, ideally, we'll be converting the output from urls_of_skus.search_skus(list_of_skus) to a parrell list, one of the skus and one of the URLS.