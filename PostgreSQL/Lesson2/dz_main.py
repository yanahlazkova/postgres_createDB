import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
import os
from datetime import date, datetime

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

def add_product(name, price, description, published_at, country='Ukrain'):
    query = '''
    INSERT INTO products (name, price, description, published_at, country)
    VALUES (%s, %s, %s, %s, %s);
    '''
    cursor.execute(query, (name, price, description, published_at, country))
    # повернемо доданий товар
    new_product_query = '''
    SELECT * FROM products
    WHERE published_at = %s;

    '''
    # ORDER BY published_at DESC
    # LIMIT 1;
    cursor.execute(new_product_query, (published_at,))
    return cursor.fetchall()

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

def menu_add():
    choice_add = int(input('1-Product\n2-Order\n3-Back'))
    match choice_add:
        case 1:
            print('Додавання товару')
            name = input('Enter name of product: ')
            price = float(input('Enter price: '))
            description = input('Enter description: ')
            published_at = datetime.now()
            new_product = add_product(name, price, description, published_at)
            print("Product added successfully.")
            print(new_product)
        case 2:
            print('Створення замовлення')
        case 3:
            print("Exiting...")
            return 
            

def main():
    create_products_tb()
    create_orders_tb()
    
    while True:
        choice = int(input("1-Add\n2-View\n3-Delete\n4-Exit\nChoose an option: "))
        match choice:
            case 1:
                menu_add()
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