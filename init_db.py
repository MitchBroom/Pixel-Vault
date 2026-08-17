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
    ("Cyber Odyssey 2088", "Open-world futuristic RPG.", 25.00, 59.99, "/static/images/Cyber Odyssey 2088.png"),
    ("Pixel Dungeon Crawl", "Retro roguelike dungeon explorer.", 4.00, 14.99, "/static/images/Pixel Dungeon Crawl.png"),
    ("Galactic Commander", "Real-time space strategy simulator.", 15.00, 39.99, "/static/images/Galactic Commander.png"),
    ("Shadow Rogue: Reborn", "Stealth-action platforming adventure.", 8.00, 19.99, "/static/images/Shadow Rogue Reborn.png"),
    ("Apex Speed Drift", "High-octane arcade street racing.", 18.00, 49.99, "/static/images/Apex Speed Drift.png"),
    ("Mythic Realms MMORPG", "Fantasy multiplayer online quest.", 20.00, 49.99, "/static/images/Mythic Realms MMORPG.png"),
    ("Eerie Whispers", "Psychological survival horror story.", 10.00, 29.99, "/static/images/Eerie Whispers.png"),
    ("Cozy Island Builder", "Relaxing sandbox farming simulator.", 6.00, 24.99, "/static/images/Cozy Island Builder.png"),
    ("Mech Tactics Prime", "Turn-based tactical mecha combat.", 12.00, 34.99, "/static/images/Mech Tactics Prime.png"),
    ("Neon Strike Ops", "Competitive fast-paced multiplayer FPS.", 14.00, 29.99, "/static/images/Neon Strike Ops.png")
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