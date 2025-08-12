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
