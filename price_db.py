def get_min_price(product_url, db_path='prices.db'):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''
        SELECT MIN(CAST(price AS FLOAT)) FROM prices WHERE product_url = ?
    ''', (product_url,))
    row = c.fetchone()
    conn.close()
    return row[0] if row and row[0] is not None else None

def get_max_price(product_url, db_path='prices.db'):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''
        SELECT MAX(CAST(price AS FLOAT)) FROM prices WHERE product_url = ?
    ''', (product_url,))
    row = c.fetchone()
    conn.close()
    return row[0] if row and row[0] is not None else None

import sqlite3
from datetime import datetime

# --- Tracked Links Table ---
def init_tracked_links_db(db_path='prices.db'):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS tracked_links (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            link TEXT NOT NULL,
            label TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def add_tracked_link(link, label, db_path='prices.db'):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('INSERT INTO tracked_links (link, label) VALUES (?, ?)', (link, label))
    conn.commit()
    conn.close()

def get_tracked_links(db_path='prices.db'):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('SELECT link, label FROM tracked_links')
    rows = c.fetchall()
    conn.close()
    return [{'link': row[0], 'label': row[1]} for row in rows]

def delete_tracked_link(label, db_path='prices.db'):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('DELETE FROM tracked_links WHERE label = ? LIMIT 1', (label,))
    conn.commit()
    conn.close()

def get_labels_from_db(db_path='prices.db'):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('SELECT DISTINCT label FROM tracked_links')
    rows = c.fetchall()
    conn.close()
    return sorted([row[0] for row in rows])

def init_db(db_path='prices.db'):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS prices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_name TEXT,
            product_url TEXT,
            price TEXT,
            image_url TEXT,
            timestamp DATETIME
        )
    ''')
    conn.commit()
    conn.close()

def save_price(product, db_path='prices.db'):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''
        INSERT INTO prices (product_name, product_url, price, image_url, timestamp)
        VALUES (?, ?, ?, ?, ?)
    ''', (
        product['name'],
        product['product_url'],
        product['price'],
        product['image_url'],
        datetime.now()
    ))
    conn.commit()
    conn.close()

def get_last_price(product_url, db_path='prices.db'):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''
        SELECT price FROM prices WHERE product_url = ? ORDER BY timestamp DESC LIMIT 1
    ''', (product_url,))
    row = c.fetchone()
    conn.close()
    return row[0] if row else None
