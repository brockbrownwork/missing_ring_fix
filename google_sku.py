from urllib.parse import urlparse
from duckduckgo_search import DDGS

def google_sku(sku):
    results = []
    sku = sku.lstrip('0')
    with DDGS() as search:
        for result in search.text(sku):
            results.append(result)
    possible_urls = []
    urls = [result["href"] for result in results]
    domains = [urlparse(url).netloc.split(".")[-2] for url in urls]
    for i, domain in enumerate(domains):
        if domain in valid_domains:
            possible_urls.append(urls[i])
    print("urls:", urls)
    print("domains:", domains)
    print("matching urls:", possible_urls)
    for url in possible_urls:
        if url.split("-")[-1] == sku:
            print(f"Found {sku} at {url}!")
            return url

valid_domains = ["zales", "kay", "jared"]

if __name__ == "__main__":
    print("Hello, test...")
    sku = '0886690700'
    google_sku(sku)


print("...done!")
