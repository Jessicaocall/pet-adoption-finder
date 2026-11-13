#import web elements from WTF
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Length

#create a class for the web elements needed for a Login Form
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

#create a class for the web elements needed for an Adoption Enquiry Form
class EnquiryForm(FlaskForm):
    email = StringField('Your registered email', validators=[DataRequired()])
    #the list of animals is filled in from the database in routes.py
    animal = SelectField('Animal', coerce=int, validators=[DataRequired()])
    message = TextAreaField('Message to the shelter', validators=[DataRequired(), Length(max=500)])
    submit = SubmitField('Send Enquiry')
