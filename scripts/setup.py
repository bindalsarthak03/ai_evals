import sqlite3

conn = sqlite3.connect("data/sample_db.sqlite")
cursor = conn.cursor()

# Create tables
cursor.execute("""
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    name TEXT,
    city TEXT,
    signup_date TEXT
)
""")

cursor.execute("""
CREATE TABLE products (
    id INTEGER PRIMARY KEY,
    name TEXT,
    price INTEGER
)
""")

cursor.execute("""
CREATE TABLE orders (
    id INTEGER PRIMARY KEY,
    user_id INTEGER,
    product_id INTEGER,
    quantity INTEGER,
    order_date TEXT
)
""")

# Insert users
users = [
    (1,'Alice','New York','2024-01-05'),
    (2,'Bob','London','2024-01-15'),
    (3,'Charlie','Delhi','2024-02-10'),
    (4,'David','Berlin','2024-02-20'),
    (5,'Eva','Paris','2024-03-01'),
    (6,'Frank','Toronto','2024-03-10')
]

cursor.executemany("INSERT INTO users VALUES (?,?,?,?)", users)

# Insert products
products = [
    (1,'Laptop',1200),
    (2,'Phone',800),
    (3,'Headphones',150),
    (4,'Keyboard',100),
    (5,'Monitor',400)
]

cursor.executemany("INSERT INTO products VALUES (?,?,?)", products)

# Insert orders
orders = [
    (1,1,1,1,'2024-02-01'),
    (2,2,2,2,'2024-02-05'),
    (3,3,3,1,'2024-02-15'),
    (4,1,4,1,'2024-03-01'),
    (5,4,1,1,'2024-03-05'),
    (6,5,5,2,'2024-03-10'),
    (7,6,2,1,'2024-03-15'),
    (8,3,4,2,'2024-03-20'),
    (9,2,3,3,'2024-03-25')
]

cursor.executemany("INSERT INTO orders VALUES (?,?,?,?,?)", orders)

conn.commit()
conn.close()

print("Database created successfully")