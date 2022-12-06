import requests
import webbrowser
import threading
from time import sleep, time

stores = ['zales', 'zalesoutlet', 'jared', 'kay', 'peoplesjewellers']

def search_sku(store_name, sku):
    r = requests.get(f"http://www.{store}.com/search?text={sku}")
    if not "search" in r.url:
        webbrowser.open(r.url)

def search_skus(sku_list):
    start = time()
    for sku in sku_list:
        threads = []
        for store in stores:
            thread = threading.Thread(target = search_sku, args = (store, sku))
            threads.append(thread)
            thread.start()
        count = 0
        print("Loading...")
        while any([i.is_alive() for i in threads]):
            done = [not i.is_alive() for i in threads].count(True)
            if done != count:
                count = done
                print("{0}/{1} sites checked...".format(done, len(stores)))
    print("Done!")
    end = time()
    print(f"Time taken: {end - start} seconds.")
    # google = input("Would you like to run a google query of the SKU? (y/n) > ")
    # if google.lower() == "y":
    #     webbrowser.open(f'https://www.google.com/search?q="{sku}"')
