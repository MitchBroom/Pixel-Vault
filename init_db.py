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
    ("Cyber Odyssey 2088", "Open-world futuristic RPG.", 25.00, 59.99, "https://picsum.photos/seed/cyber/300/200"),
    ("Pixel Dungeon Crawl", "Retro roguelike dungeon explorer.", 4.00, 14.99, "https://picsum.photos/seed/dungeon/300/200"),
    ("Galactic Commander", "Real-time space strategy simulator.", 15.00, 39.99, "https://picsum.photos/seed/galaxy/300/200"),
    ("Shadow Rogue: Reborn", "Stealth-action platforming adventure.", 8.00, 19.99, "https://picsum.photos/seed/rogue/300/200"),
    ("Apex Speed Drift", "High-octane arcade street racing.", 18.00, 49.99, "https://picsum.photos/seed/racing/300/200"),
    ("Mythic Realms MMORPG", "Fantasy multiplayer online quest.", 20.00, 49.99, "https://picsum.photos/seed/realm/300/200"),
    ("Eerie Whispers", "Psychological survival horror story.", 10.00, 29.99, "https://picsum.photos/seed/horror/300/200"),
    ("Cozy Island Builder", "Relaxing sandbox farming simulator.", 6.00, 24.99, "https://picsum.photos/seed/cozy/300/200"),
    ("Mech Tactics Prime", "Turn-based tactical mecha combat.", 12.00, 34.99, "https://picsum.photos/seed/mech/300/200"),
    ("Neon Strike Ops", "Competitive fast-paced multiplayer FPS.", 14.00, 29.99, "https://picsum.photos/seed/strike/300/200")
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