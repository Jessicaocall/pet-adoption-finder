#import os to allow for interaction with environment variables in the operating system
import os

#create class to hold config data for web service
class Config:
    #define secret key
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'P3T4D0PT10N'

    #PostgreSQL 18 connection details
    DB_HOST = 'localhost'
    DB_PORT = 5432
    DB_USER = 'postgres'
    DB_PASSWORD = 'postgres'
    #name of the database created by initialise_db.py
    DB_NAME = 'pet_adoption_finder'
