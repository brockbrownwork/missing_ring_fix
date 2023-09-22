import requests
import webbrowser
import threading
from time import sleep, time

stores = ['zales', 'zalesoutlet', 'jared', 'kay', 'peoplesjewellers']
# stores = ['zalesoutlet', 'peoplesjewellers']

def search_store_for_sku(store_name, sku, results):
    '''
    This is a helper function for search_sku, it helps facilitate
    threading :)
    '''
    r = requests.get(f"http://www.{store_name}.com/search?text={sku}")
    # if the request was unsuccessful, give up
    if r.status_code != 200:
        print(f"Request for http://www.{store_name}.com/search?text={sku} was unsuccessful.")
        return
    # if the request is a product page and not a search result, add the url to the list of results
    if not "search" in r.url:
        results.append(r.url)

def search_sku(sku):
    '''
    Return a list of URLS for a given SKU
    '''
    start = time()
    results = []
    threads = []
    for store in stores:
        thread = threading.Thread(target = search_store_for_sku, args = (store, sku, results))
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

# test it out

if __name__ == "__main__":
    print("Testing...")
    test_skus = ['20509163',
                 '20344860',
                 '20283669'
                 ]
    # test_sku = '1234'
    for test_sku in test_skus:
        print(f"results for {test_sku}:", search_sku(test_sku))
