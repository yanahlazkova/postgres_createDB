import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
import os
# from datetime import date, datetime

load_dotenv()

connect = psycopg2.connect(
    host=os.environ.get("DB_HOST"),
    database=os.environ.get("DB_NAME"),
    user=os.environ.get("DB_USER"),
    password=os.environ.get("DB_PASSWORD"),
    port=os.environ.get("DB_PORT"),
)
cursor = connect.cursor(cursor_factory=RealDictCursor)
connect.autocommit = True

def create_products_tb():
    query = '''
    CREATE TABLE IF NOT EXISTS products (
        id SERIAL PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        price NUMERIC(10, 2) NOT NULL,
        description TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        published_at TIMESTAMP,
        country VARCHAR(50) NOT NULL
    );
    '''
    cursor.execute(query)

def create_orders_tb():
    query = '''
    CREATE TABLE IF NOT EXISTS orders (
        id SERIAL PRIMARY KEY,
        amount NUMERIC(10, 2) NOT NULL,
        count_products INTEGER NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    '''
    cursor.execute(query)

def add_product(name, price, description, published_at, country):
    query = '''
    INSERT INTO products (name, price, description, published_at, country)
    VALUES (%s, %s, %s, %s, %s);
    '''
    cursor.execute(query, (name, price, description, published_at, country))

def delete_product(product_id):
    cursor.execute('DELETE FROM products WHERE id = %s;', (product_id,))

def get_all_products():
    cursor.execute('SELECT * FROM products;')
    return cursor.fetchall()

def get_products_limit(limit):
    cursor.execute('SELECT * FROM products LIMIT %s;', (limit,))
    return cursor.fetchall()

def get_product_by_id(product_id):
    cursor.execute('SELECT * FROM products WHERE id = %s;', (product_id,))
    return cursor.fetchone()


def get_products_by_date(pub_date):
    cursor.execute('SELECT * FROM products WHERE DATE(published_at) = %s;', (pub_date,))
    return cursor.fetchall()

def get_products_published_today():
    cursor.execute('SELECT * FROM products WHERE DATE(published_at) = CURRENT_DATE;')
    return cursor.fetchall()

def get_products_price_greater_than(amount):
    cursor.execute('SELECT * FROM products WHERE price > %s;', (amount,))
    return cursor.fetchall()

def get_products_price_less_than(amount):
    cursor.execute('SELECT * FROM products WHERE price < %s;', (amount,))
    return cursor.fetchall()

def get_products_by_name(name):
    cursor.execute('SELECT * FROM products WHERE name ILIKE %s;', (f'%{name}%',))
    return cursor.fetchall()

def get_products_by_country(country):
    cursor.execute('SELECT * FROM products WHERE country ILIKE %s;', (country,))
    return cursor.fetchall()

def get_product_count_per_country():
    cursor.execute('''
    SELECT country, COUNT(*) AS total_products
    FROM products
    GROUP BY country;
    ''')
    return cursor.fetchall()



def add_order(amount, count_products):
    cursor.execute('''
    INSERT INTO orders (amount, count_products)
    VALUES (%s, %s);
    ''', (amount, count_products))

def delete_order(order_id):
    cursor.execute('DELETE FROM orders WHERE id = %s;', (order_id,))

def get_all_orders():
    cursor.execute('SELECT * FROM orders;')
    return cursor.fetchall()

def get_orders_limit(limit):
    cursor.execute('SELECT * FROM orders LIMIT %s;', (limit,))
    return cursor.fetchall()

def get_order_by_id(order_id):
    cursor.execute('SELECT * FROM orders WHERE id = %s;', (order_id,))
    return cursor.fetchone()



def get_max_order():
    cursor.execute('SELECT * FROM orders ORDER BY amount DESC LIMIT 1;')
    return cursor.fetchone()

def get_min_order():
    cursor.execute('SELECT * FROM orders ORDER BY amount ASC LIMIT 1;')
    return cursor.fetchone()

def get_orders_today():
    cursor.execute('SELECT * FROM orders WHERE DATE(created_at) = CURRENT_DATE;')
    return cursor.fetchall()

def get_orders_this_month():
    cursor.execute('''
    SELECT * FROM orders
    WHERE EXTRACT(MONTH FROM created_at) = EXTRACT(MONTH FROM CURRENT_DATE)
    AND EXTRACT(YEAR FROM created_at) = EXTRACT(YEAR FROM CURRENT_DATE);
    ''')
    return cursor.fetchall()

def get_total_order_sum():
    cursor.execute('SELECT SUM(amount) as total FROM orders;')
    return cursor.fetchone()

def get_avg_order_amount():
    cursor.execute('SELECT AVG(amount) as avg_amount FROM orders;')
    return cursor.fetchone()

def get_month_order_sum():
    cursor.execute('''
    SELECT SUM(amount) as month_total FROM orders
    WHERE EXTRACT(MONTH FROM created_at) = EXTRACT(MONTH FROM CURRENT_DATE)
    AND EXTRACT(YEAR FROM created_at) = EXTRACT(YEAR FROM CURRENT_DATE);
    ''')
    return cursor.fetchone()

def get_month_product_count():
    cursor.execute('''
    SELECT SUM(count_products) as products_sold FROM orders
    WHERE EXTRACT(MONTH FROM created_at) = EXTRACT(MONTH FROM CURRENT_DATE)
    AND EXTRACT(YEAR FROM created_at) = EXTRACT(YEAR FROM CURRENT_DATE);
    ''')
    return cursor.fetchone()

def main():
    create_products_tb()
    create_orders_tb()
    
    while True:
        choice = int(input("1-Add Product\n2-View Products\n3-Delete Products\n4-Exit\nChoose an option: "))
        match choice:
            case 1:
                product = input("Enter product (name, price, description, published_at, country): ")
                add_product(product)
                print("Product added successfully.")
            case 2:
                products = get_all_products()
                for product in products:
                    print(dict(product))
            case 3:
                product_id = int(input("Enter product ID to delete: "))
                delete_product(product_id)
                print("Product deleted successfully.")
            case 4:
                print("Exiting...")
                break
main()
    # 👇 Приклад вставки
    # add_product("Мило", 25.50, "Господарське мило", datetime.now(), "Україна")
    # add_order(120.00, 5)

    # 👇 Приклад виклику
    # print(get_all_products())
    # print(get_orders_today())
