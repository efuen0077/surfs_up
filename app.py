
from flask import Flask
#create a new Flask app
app = Flask(__name__)
#__name__ variable denotes the name of the
# current function. You can use the __name__
# variable to determine if your code is being
# run from the command line or if it has been
# imported into another piece of code.
# Variables with underscores before and after
# them are called magic methods in Python.

#define the starting point, aka the root
@app.route('/')

#create a function called hello_world().
# Whenever you make a route in Flask,
# you put the code you want in that
# specific route below @app.route().

@app.route('/')
def hello_world():
	return 'Hello world'

#run the following in the terminal
#set FLASK_APP=app.py
#flask run

@app.route('/name')
def my_name():
	return 'Eva'