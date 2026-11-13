#import render_template, redirect, url_for and flash functions from flask
from flask import render_template, redirect, url_for, flash
#import app variable from app package
from app import app
#import LoginForm and EnquiryForm classes from our forms.py file
from app.forms import LoginForm, EnquiryForm
#import the query and execute functions from our db.py file
from app.db import query, execute

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

#create an association for the URL /enquiry
@app.route('/enquiry', methods=['GET', 'POST'])

#create the enquiry page - saves adoption enquiries to the database
def enquiry():
    #create an instance of an enquiryform obj and store in a variable called form
    form = EnquiryForm()

    #fill the animal drop-down with available animals from the database
    available = query("SELECT animal_id, name, breed FROM animals "
                      "WHERE status = 'available' ORDER BY name")
    form.animal.choices = [(a['animal_id'], a['name'] + ' (' + a['breed'] + ')') for a in available]

    if form.validate_on_submit():
        #check the email belongs to a registered user
        users = query("SELECT user_id, first_name FROM users WHERE email = %s",
                      (form.email.data.strip().lower(),))

        if not users:
            form.email.errors.append('No account found with that email.')
        else:
            #save the enquiry to the enquiries table
            execute("INSERT INTO enquiries (user_id, animal_id, message) VALUES (%s, %s, %s)",
                    (users[0]['user_id'], form.animal.data, form.message.data))
            flash('Thanks ' + users[0]['first_name'] + ', your enquiry has been sent to the shelter!')
            return redirect(url_for('enquiry'))

    #show the 10 most recent enquiries from the database
    recent = query("SELECT u.first_name, a.name AS animal, e.status, "
                   "TO_CHAR(e.submitted_at, 'DD Mon YYYY') AS submitted "
                   "FROM enquiries e "
                   "JOIN users u ON e.user_id = u.user_id "
                   "JOIN animals a ON e.animal_id = a.animal_id "
                   "ORDER BY e.submitted_at DESC, e.enquiry_id DESC LIMIT 10")

    return render_template('enquiry.html', title='Adoption Enquiry', form=form, recent=recent)
