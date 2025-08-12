
from flask import Flask, render_template, request, redirect, url_for
from mobileshop_eu import scrape_mobileshop_eu
from price_db import init_db, save_price, get_last_price, get_min_price, get_max_price
import json
import os

app = Flask(__name__)

TRACKED_FILE = 'tracked_links.json'

def load_tracked():
    if not os.path.exists(TRACKED_FILE):
        return []
    with open(TRACKED_FILE, 'r') as f:
        return json.load(f)

def save_tracked(tracked):
    with open(TRACKED_FILE, 'w') as f:
        json.dump(tracked, f)

def get_labels(tracked):
    return sorted(list(set(item['label'] for item in tracked)))

@app.route('/', methods=['GET'])
def index():
    init_db()
    tracked = load_tracked()
    label = request.args.get('label')
    labels = get_labels(tracked)
    if label:
        filtered = [item for item in tracked if item['label'] == label]
        tracked_items = []
        for item in filtered:
            products = scrape_mobileshop_eu(item['link'])
            for product in products:
                last_price = get_last_price(product['product_url'])
                min_price = get_min_price(product['product_url'])
                max_price = get_max_price(product['product_url'])
                product['last_price'] = last_price
                product['min_price'] = min_price
                product['max_price'] = max_price
                if last_price != product['price']:
                    save_price(product)
                tracked_items.append(product)
    else:
        tracked_items = []
    return render_template(
        'index.html',
        labels=labels,
        selected_label=label,
        tracked_items=tracked_items,
        products=[]
    )

@app.route('/add_track', methods=['POST'])
def add_track():
    link = request.form.get('link')
    label = request.form.get('label')
    if not link or not label:
        return redirect(url_for('index'))
    tracked = load_tracked()
    # Prevent duplicates (same link and label)
    for item in tracked:
        if item['link'] == link and item['label'] == label:
            return redirect(url_for('index', label=label))
    tracked.append({'link': link, 'label': label})
    save_tracked(tracked)
    return redirect(url_for('index', label=label))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
