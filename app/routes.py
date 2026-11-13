#import render_template, redirect, url_for and request functions from flask
from flask import render_template, redirect, url_for, request
#import app variable from app package
from app import app
#import LoginForm class from our forms.py file
from app.forms import LoginForm
#import the query function from our db.py file
from app.db import query

#create an association for the URL /
@app.route('/')
#create an association for the URL /index
@app.route('/index')

#create the index page to display the animals waiting for a home
def index():
    #create a list of dictionaries to hold the animal information
    animals = [
        {
            'name': 'Bella',
            'emoji': '🐕',
            'breed': 'Labrador cross',
            'age': '2 years',
            'location': 'Ballincollig'
        },
        {
            'name': 'Oscar',
            'emoji': '🐈',
            'breed': 'Domestic shorthair',
            'age': '4 years',
            'location': 'Cork City'
        },
        {
            'name': 'Murphy',
            'emoji': '🐕',
            'breed': 'Collie',
            'age': '8 months',
            'location': 'Mallow'
        },
        {
            'name': 'Clover',
            'emoji': '🐇',
            'breed': 'Lionhead rabbit',
            'age': '1 year',
            'location': 'Midleton'
        }
    ]

    return render_template('index.html', title='Home', animals=animals)

#create an association for the URL /about
@app.route('/about')

#create the about page
def about():
    return render_template('about.html', title='About Us')

#create an association for the URL /login
@app.route('/login', methods=['GET', 'POST'])

#create the login page to display web form for user
def login():
    #create an instance of a loginform obj and store in a variable called form
    form = LoginForm()

    if form.validate_on_submit():
        return redirect(url_for('index'))

    return render_template('login.html', title='Sign In', form=form)

#create an association for the URL /animals
@app.route('/animals')

#create the browse page to display animals from the database with filters
def animals():
    #read the filter choices from the URL e.g. /animals?species=dog&size=small
    species = request.args.get('species', '')
    size = request.args.get('size', '')

    #build the SQL query - only show animals that are not adopted yet
    sql = ("SELECT a.name, a.species, a.breed, a.age_months, a.sex, a.size, "
           "a.good_with_kids, a.image_url, a.status, s.name AS shelter, s.town "
           "FROM animals a JOIN shelters s ON a.shelter_id = s.shelter_id "
           "WHERE a.status <> 'adopted'")
    params = []

    #add a filter for species if the user picked one
    if species:
        sql += " AND a.species = %s"
        params.append(species)

    #add a filter for size if the user picked one
    if size:
        sql += " AND a.size = %s"
        params.append(size)

    sql += " ORDER BY a.date_listed DESC, a.name"

    #run the query against the PostgreSQL database
    results = query(sql, params)

    return render_template('animals.html', title='Browse Pets', animals=results,
                           species=species, size=size)
