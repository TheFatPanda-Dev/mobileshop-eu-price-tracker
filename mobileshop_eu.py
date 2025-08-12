from urllib.parse import urljoin
from bs4 import BeautifulSoup
import requests

def scrape_mobileshop_eu(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    products = []
    for item in soup.select('.product-module'):
        name = item.select_one('.product-name')
        price = item.select_one('.price')
        image_url = None
        product_url = None
        # Try to get the product URL from the first <a> inside product-module
        link = item.select_one('a')
        if link and link.has_attr('href'):
            product_url = link['href']
            if product_url and not product_url.startswith('http'):
                product_url = urljoin(url, product_url)
        figure = item.select_one('figure')
        if figure:
            img = figure.select_one('a img') or figure.select_one('img')
            if img:
                # Prefer data-src over src
                if img.has_attr('data-src'):
                    image_url = img['data-src']
                elif img.has_attr('src'):
                    image_url = img['src']
                # Fix relative URLs
                if image_url and not image_url.startswith('http'):
                    image_url = urljoin(url, image_url)
        if name and price:
            products.append({
                'name': name.get_text(strip=True),
                'price': price.get_text(strip=True),
                'image_url': image_url,
                'product_url': product_url
            })
    return products
