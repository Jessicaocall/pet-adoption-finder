#import psycopg2 to connect Python to PostgreSQL
import psycopg2
#import RealDictCursor so each row comes back as a dictionary e.g. row['name']
from psycopg2.extras import RealDictCursor
#import config settings
from config import Config

#create a connection to the pet_adoption_finder database
def get_connection():
    return psycopg2.connect(
        host=Config.DB_HOST,
        port=Config.DB_PORT,
        user=Config.DB_USER,
        password=Config.DB_PASSWORD,
        dbname=Config.DB_NAME
    )

#run a SELECT query and return all rows as a list of dictionaries
def query(sql, params=None):
    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute(sql, params)
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows

#run an INSERT, UPDATE or DELETE query and save the change
def execute(sql, params=None):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(sql, params)
    conn.commit()
    cur.close()
    conn.close()
