import sqlite3

connection = sqlite3.connect("pixelvault.db")
cursor = connection.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT NOT NULL,
        cost_price REAL NOT NULL,
        sell_price REAL NOT NULL,
        image TEXT NOT NULL
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_number TEXT NOT NULL UNIQUE,
        email TEXT NOT NULL,
        phone TEXT NOT NULL,
        suburb TEXT NOT NULL,
        total_cost REAL NOT NULL,
        total_sale REAL NOT NULL,
        profit REAL NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS order_items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_id INTEGER NOT NULL,
        product_id INTEGER NOT NULL,
        product_title TEXT NOT NULL,
        quantity INTEGER NOT NULL,
        cost_price REAL NOT NULL,
        sell_price REAL NOT NULL,
        FOREIGN KEY (order_id) REFERENCES orders(id),
        FOREIGN KEY (product_id) REFERENCES products(id)
    )
""")

cursor.execute("DELETE FROM products")

products = [
]

cursor.executemany("""
    INSERT INTO products
    (title, description, cost_price, sell_price, image)
    VALUES (?, ?, ?, ?, ?)
""", products)

cursor.execute("SELECT COUNT(*) FROM products")
product_count = cursor.fetchone()[0]

print(f"Products in database: {product_count}")

connection.commit()
connection.close()

print("Pixel Vault database created successfully.")