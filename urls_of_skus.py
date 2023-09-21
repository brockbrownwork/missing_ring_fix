import requests
import webbrowser
import threading
from time import sleep, time

stores = ['zales', 'zalesoutlet', 'jared', 'kay', 'peoplesjewellers']

def search_sku(store_name, sku, results):
    r = requests.get(f"http://www.{store_name}.com/search?text={sku}")
    if not "search" in r.url:
        # webbrowser.open(r.url)
        results.append(r.url)

def search_skus(sku_list):
    start = time()
    results = []
    for sku in sku_list:
        threads = []
        for store in stores:
            thread = threading.Thread(target = search_sku, args = (store, sku, results))
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
    return results
    # google = input("Would you like to run a google query of the SKU? (y/n) > ")
    # if google.lower() == "y":
    #     webbrowser.open(f'https://www.google.com/search?q="{sku}"')

# test it out

if __name__ == "__main__":
    test_sku = ['1234']
    print(f"results for {test_sku}:", search_skus(test_sku))
