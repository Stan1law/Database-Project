import sqlite3

def connect_db():

    conn = sqlite3.connect("computer_shop.db")
    cursor = conn.cursor()

    # PRODUCTS TABLE
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        brand TEXT,
        price REAL,
        stock INTEGER
    )
    """)

    # QUOTATIONS TABLE
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS quotations (
        quotation_id INTEGER PRIMARY KEY AUTOINCREMENT,
        quotation_number TEXT,
        customer_name TEXT,
        total_amount REAL
    )
    """)

    # QUOTATION ITEMS TABLE
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS quotation_items (
        item_id INTEGER PRIMARY KEY AUTOINCREMENT,
        quotation_id INTEGER,
        product_name TEXT,
        price REAL,
        quantity INTEGER,
        total REAL
    )
    """)

    conn.commit()
    conn.close()

    print("Database ready!")