import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
import random
import os
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

def create_customer_table():
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS customers (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            manager_id INTEGER REFERENCES managers(id) ON DELETE SET NULL
        );
    ''')
    
def create_manager_table():
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS managers (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL
        );
    ''')

# create_manager_table()
# create_customer_table()

def insert_manager(name):
    cursor.execute('''
        INSERT INTO managers (name) VALUE (%s) RETURNING id;
        ''', name)
    return cursor.fetchone()['id']
    
def insert_customer(name, manager_id):
    cursor.execute('''
        INSERT INTO customers (name, manager_id) VALUES (%s, %s) RETURNING id, name;
    ''', (name, manager_id))
    return cursor.fetchone()['id']

def get_managers():
    cursor.execute('SELECT * FROM managers;')
    return cursor.fetchall()

names = ['Mike', 'John', 'Alice', 'Bob', 'Charlie', 'Diana', 'Eve', 'Frank', 'Grace', 'Hank', 'Ivy']

for i in range(5):
    manager_name = random.choice(names)
    manager_id = insert_manager(manager_name)
    print(f'Inserted manager: {manager_name} with ID: {manager_id}')
    
    for j in range(3):
        customer_name = random.choice(names)
        customer_id = insert_customer(customer_name, manager_id)
        print(f'Inserted customer: {customer_name} with ID: {customer_id} under manager ID: {manager_id}')