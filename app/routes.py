from app import app
from flask import render_template
from app.forms import LoginForm, RegistrationForm

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    form = LoginForm()
    return render_template('login.html', form=form)

@app.route('/register')
def register():
    form = RegistrationForm()
    return render_template('register.html', form=form)

'''
flask uses app routes to put logic behind urls

@app.route('whatever_url_you_want')

then build a function to do the logic, accept input, etc.

def function():

user render_template() to render html from templates folder
formatting and design can go in static

return render_template('content.html')

everything else is extra
also, recommend using a virtualenv to install necessary packages
pretty straightforward...
'''
