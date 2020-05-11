
#-----------9.4---------------
#from flask import Flask
#create a new Flask app
#app = Flask(__name__)
#__name__ variable denotes the name of the
# current function. You can use the __name__
# variable to determine if your code is being
# run from the command line or if it has been
# imported into another piece of code.
# Variables with underscores before and after
# them are called magic methods in Python.

#define the starting point, aka the root
#@app.route('/')

#create a function called hello_world().
# Whenever you make a route in Flask,
# you put the code you want in that
# specific route below @app.route().

#@app.route('/')
#def hello_world():
#	return 'Hello world'

#run the following in the terminal
#set FLASK_APP=app.py
#flask run

#@app.route('/name')
#def my_name():
	#return 'Eva'

#----------9.5.1-----------------
#import dependencies
import datetime as dt
import numpy as np
import pandas as pd 
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

engine = create_engine("sqlite:///hawaii.sqlite")

#reflect the database into our classes
Base = automap_base()
Base.prepare(engine, reflect=True)


#Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

#create a session link from Python to the database

session = Session(engine)

#----Set up Flask----
app = Flask(__name__)


#---------9.5.2-------------
#if we wanted to run example.py, then we would set __name__ to example
@app.route("/")

def welcome():
	return(
	'''
    Welcome to the Climate Analysis API!
	Available Routes:
	/api/v1.0/precipitation
    /api/v1.0/stations
    /api/v1.0/tobs
    /api/v1.0/temp/start/end
    ''')

##flask run


#-------9.5.3-------------
@app.route("/api/v1.0/precipitation")

def precipitation():
   prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
   precipitation = session.query(Measurement.date, Measurement.prcp).\
	   filter(Measurement.date >= prev_year).all()
   precip = {date: prcp for date, prcp in precipitation}
   return jsonify(precip)

##http://127.0.0.1:5000/

#You will need to navigate to the precipitation route in order
#to see the output of your code. You can do this by adding
#api/v1.0/precipitation to the end of the web address.

#--------9.5.4----------
@app.route("/api/v1.0/stations")

def stations():
	results = session.query(Station.station).all()
	stations = list(np.ravel(results))
	return jsonify(stations)

#the stations route is ready to be tested! To test it, run
#the code in the command line and then check if the result
#is correct in the web browser (http://localhost:5000/).
#Don’t forget to add the remainder of the route to see the
#output of your code


#---------9.5.5------------
@app.route("/api/v1.0/tobs")

def temp_monthly():
	prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)

	results = session.query(Measurement.tobs).\
		filter(Measurement.station == 'USC00519281').\
		filter(Measurement.date >= prev_year).all()
	temps = list(np.ravel(results))
	return jsonify(temps)

#type this in terminal 
#python app.py
#(http://localhost:5000/ (Links to an external site.))


#----------9.5.6------------
@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")

def stats(start=None, end=None):
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]
    if not end:
        results = session.query(*sel).filter(Measurement.date <= start).all()
        temps = list(np.ravel(results))
        return jsonify(temps)
    results = session.query(*sel).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    temps = list(np.ravel(results))
    return jsonify(temps)


#/api/v1.0/temp/start/endroute
#output: [null,null,null]
#This code tells us that we
# have not specified a start and end date for our range

# let’s say we want to find the minimum, maximum,
# and average temperatures for June 2017
#/api/v1.0/temp/2017-06-01/2017-06-30
#output: [71.0,77.21989528795811,83.0]
