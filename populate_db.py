#populate_db.py
#Automates populating the pet_adoption_finder tables with the data in the data folder.
#Run with: python populate_db.py  (run initialise_db.py first)

#import csv to read the data files
import csv
#import psycopg2 to connect Python to PostgreSQL
import psycopg2
#import generate_password_hash so passwords are never stored as plain text
from werkzeug.security import generate_password_hash
#import the database settings from config.py
from config import Config

#function to read a csv file from the data folder into a list of dictionaries
def read_csv(filename):
    with open('data/' + filename, 'r', encoding='utf-8') as file:
        return list(csv.DictReader(file))

#function to turn an empty csv value into None (NULL in the database)
def blank_to_none(value):
    if value == '':
        return None
    return value

#connect to the pet_adoption_finder database
conn = psycopg2.connect(
    host=Config.DB_HOST,
    port=Config.DB_PORT,
    user=Config.DB_USER,
    password=Config.DB_PASSWORD,
    dbname=Config.DB_NAME
)
cur = conn.cursor()

#empty all tables first so the script can be run more than once
#RESTART IDENTITY sets the ID numbers back to 1
cur.execute('TRUNCATE enquiries, favourites, animals, users, shelters RESTART IDENTITY CASCADE;')

#insert shelters
shelters = read_csv('shelters.csv')
for s in shelters:
    cur.execute(
        'INSERT INTO shelters (name, address, town, county, latitude, longitude, phone, email) '
        'VALUES (%s, %s, %s, %s, %s, %s, %s, %s);',
        (s['name'], s['address'], s['town'], s['county'],
         s['latitude'], s['longitude'], s['phone'], s['email'])
    )
print('Inserted ' + str(len(shelters)) + ' shelters')

#insert users - each password is hashed before it is saved
users = read_csv('users.csv')
for u in users:
    cur.execute(
        'INSERT INTO users (first_name, last_name, email, password_hash, role, shelter_id) '
        'VALUES (%s, %s, %s, %s, %s, %s);',
        (u['first_name'], u['last_name'], u['email'],
         generate_password_hash(u['password']), u['role'], blank_to_none(u['shelter_id']))
    )
print('Inserted ' + str(len(users)) + ' users')

#insert animals
animals = read_csv('animals.csv')
for a in animals:
    cur.execute(
        'INSERT INTO animals (shelter_id, name, species, breed, age_months, sex, size, '
        'good_with_kids, description, image_url, status) '
        'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);',
        (a['shelter_id'], a['name'], a['species'], a['breed'], a['age_months'], a['sex'],
         a['size'], a['good_with_kids'] == 'true', a['description'], a['image_url'], a['status'])
    )
print('Inserted ' + str(len(animals)) + ' animals')

#insert favourites
favourites = read_csv('favourites.csv')
for f in favourites:
    cur.execute(
        'INSERT INTO favourites (user_id, animal_id) VALUES (%s, %s);',
        (f['user_id'], f['animal_id'])
    )
print('Inserted ' + str(len(favourites)) + ' favourites')

#insert enquiries
enquiries = read_csv('enquiries.csv')
for e in enquiries:
    cur.execute(
        'INSERT INTO enquiries (user_id, animal_id, message, status) VALUES (%s, %s, %s, %s);',
        (e['user_id'], e['animal_id'], e['message'], e['status'])
    )
print('Inserted ' + str(len(enquiries)) + ' enquiries')

#save all the changes
conn.commit()
cur.close()
conn.close()
print('Database populated successfully.')
