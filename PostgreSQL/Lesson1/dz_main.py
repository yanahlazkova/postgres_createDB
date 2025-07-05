import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
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

def create_table():
    query = '''
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        name text NOT NULL,
        age INT NOT NULL,
        gender text NOT NULL,
        nationality TEXT NOT NULL
    );
    
    CREATE TABLE IF NOT EXISTS posts (
      id SERIAL PRIMARY KEY,
      user_id INT,
      title TEXT NOT NULL,
      descreption TEXT NOT NULL
    );
   
    CREATE TABLE IF NOT EXISTS comments (
      id SERIAL PRIMARY KEY,
      user_id INT,
      post_id INT,
      text TEXT NOT NULL
    );
    
    CREATE TABLE IF NOT EXISTS emails (
      id SERIAL PRIMARY KEY,
      user_id INT,
      email TEXT NOT NULL
    );
    
    CREATE TABLE IF NOT EXISTS likes (
      id SERIAL PRIMARY KEY,
      user_id INT,
      post_id INT
    );
    '''
    cursor.execute(query)
    

create_table()