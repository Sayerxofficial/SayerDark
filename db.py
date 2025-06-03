import sqlite3
import json
import os
import shutil
from datetime import datetime
from config import DATABASE_FILE

conn = sqlite3.connect(DATABASE_FILE)
cursor = conn.cursor()

def backup_database():
    """Create a backup of the database"""
    try:
        backup_dir = "backups"
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)
            
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = os.path.join(backup_dir, f"database_{timestamp}.db")
        
        shutil.copy2(DATABASE_FILE, backup_file)
        print(f"Database backed up to {backup_file}")
        return True
    except Exception as e:
        print(f"Error backing up database: {str(e)}")
        return False

def setup_db():
    # Drop old tables if they exist
    cursor.execute('DROP TABLE IF EXISTS products')
    cursor.execute('DROP TABLE IF EXISTS markets')
    
    # Products table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            market TEXT,
            product_name TEXT,
            price TEXT,
            url TEXT,
            last_seen TEXT,
            first_seen TEXT,
            price_history TEXT,
            UNIQUE(market, product_name)
        )
    ''')
    
    # Markets table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS markets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE,
            url TEXT,
            last_check TEXT,
            status TEXT,
            error_count INTEGER DEFAULT 0
        )
    ''')
    
    conn.commit()

def add_or_update_product(market, product_name, price, url=None):
    """Add or update product with error handling"""
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()
        
        # Check if product exists
        cursor.execute("""
            SELECT id, price, price_history FROM products 
            WHERE market = ? AND product_name = ?
        """, (market, product_name))
        
        result = cursor.fetchone()
        
        if result:
            # Update existing product
            product_id, old_price, price_history = result
            price_history = json.loads(price_history) if price_history else []
            
            # Add new price to history if changed
            if old_price != price:
                price_history.append({
                    'price': price,
                    'timestamp': datetime.now().isoformat()
                })
            
            cursor.execute("""
                UPDATE products 
                SET price = ?, url = ?, last_seen = CURRENT_TIMESTAMP, price_history = ?
                WHERE id = ?
            """, (price, url, json.dumps(price_history), product_id))
        else:
            # Add new product
            price_history = [{
                'price': price,
                'timestamp': datetime.now().isoformat()
            }]
            
            cursor.execute("""
                INSERT INTO products (market, product_name, price, url, price_history)
                VALUES (?, ?, ?, ?, ?)
            """, (market, product_name, price, url, json.dumps(price_history)))
        
        conn.commit()
        return True
    except sqlite3.Error as e:
        print(f"Database error: {str(e)}")
        return False
    finally:
        if conn:
            conn.close()

def product_exists(market, product_name):
    cursor.execute('SELECT * FROM products WHERE market=? AND product_name=?', 
                  (market, product_name))
    return cursor.fetchone()

def update_market_status(market_name, status, error_count=0):
    """Update market status with error handling"""
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT OR REPLACE INTO markets (name, last_check, status, error_count)
            VALUES (?, ?, ?, ?)
        """, (market_name, datetime.now().isoformat(), status, error_count))
        
        conn.commit()
        return True
    except sqlite3.Error as e:
        print(f"Database error: {str(e)}")
        return False
    finally:
        if conn:
            conn.close()

def get_market_stats(market_name):
    cursor.execute('''
        SELECT COUNT(*) as total_products,
               COUNT(CASE WHEN last_seen > datetime('now', '-1 day') THEN 1 END) as active_products,
               COUNT(CASE WHEN price_history != '[]' THEN 1 END) as products_with_price_changes
        FROM products
        WHERE market = ?
    ''', (market_name,))
    return cursor.fetchone()
