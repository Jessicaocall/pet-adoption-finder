#import render_template, redirect and url_for functions from flask
from flask import render_template, redirect, url_for
#import app variable from app package
from app import app
#import LoginForm class from our forms.py file
from app.forms import LoginForm

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
