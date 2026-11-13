#initialise_db.py
#Automates creating the pet_adoption_finder database and its tables.
#Run with: python initialise_db.py

#import psycopg2 to connect Python to PostgreSQL
import psycopg2
#import the database settings from config.py
from config import Config

#connect to the default 'postgres' database first, because a database
#cannot be created while you are connected to it
conn = psycopg2.connect(
    host=Config.DB_HOST,
    port=Config.DB_PORT,
    user=Config.DB_USER,
    password=Config.DB_PASSWORD,
    dbname='postgres'
)
#CREATE DATABASE cannot run inside a transaction, so turn on autocommit
conn.autocommit = True
cur = conn.cursor()

#delete the database if it already exists so we always start fresh
print('Dropping database ' + Config.DB_NAME + ' if it exists...')
cur.execute('DROP DATABASE IF EXISTS ' + Config.DB_NAME + ' WITH (FORCE);')

#create the database
print('Creating database ' + Config.DB_NAME + '...')
cur.execute('CREATE DATABASE ' + Config.DB_NAME + ';')

cur.close()
conn.close()

#connect to the new database
conn = psycopg2.connect(
    host=Config.DB_HOST,
    port=Config.DB_PORT,
    user=Config.DB_USER,
    password=Config.DB_PASSWORD,
    dbname=Config.DB_NAME
)
cur = conn.cursor()

#read the SQL from schema.sql and run it to create the tables and relationships
print('Creating tables from schema.sql...')
with open('schema.sql', 'r', encoding='utf-8') as file:
    cur.execute(file.read())

#save the changes
conn.commit()

#list the tables that were created
cur.execute("SELECT table_name FROM information_schema.tables "
            "WHERE table_schema = 'public' ORDER BY table_name;")
for row in cur.fetchall():
    print('  created table: ' + row[0])

cur.close()
conn.close()
print('Database initialised successfully.')
