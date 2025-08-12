from flask import Flask, render_template
from mobileshop_eu import scrape_mobileshop_eu
from price_db import init_db, save_price, get_last_price, get_min_price, get_max_price

app = Flask(__name__)

URL = "https://www.mobileshop.eu/si/iskanje/?keyword=Xiaomi+15"

@app.route('/')
def index():
    # Initialize DB (does nothing if already exists)
    init_db()
    products = scrape_mobileshop_eu(URL)
    # Track price changes and save new prices
    for product in products:
        last_price = get_last_price(product['product_url'])
        min_price = get_min_price(product['product_url'])
        max_price = get_max_price(product['product_url'])
        product['last_price'] = last_price
        product['min_price'] = min_price
        product['max_price'] = max_price
        if last_price != product['price']:
            save_price(product)
    return render_template('index.html', products=products)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
