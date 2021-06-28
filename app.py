# Section 9.5.1
import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

# We'll set up our database engine for the Flask application.
engine = create_engine("sqlite:///hawaii.sqlite")

# Let's reflect the database into our classes.
Base = automap_base()

# Reflecting the database:
Base.prepare(engine, reflect=True)

# Saving our references to each table.
Measurement = Base.classes.measurement
Station = Base.classes.station

# Creating a session link from Python to our database.
session = Session(engine)

# To define our Flask app, add the following line of code. This will create a Flask application called "app."
app = Flask(__name__)

# Section 9.5.2 - Building our flask routes
# We can define the welcome route using the code below:
@app.route("/")

# First, create a function welcome() with a return statement.
# Next, add the precipitation, stations, tobs, and temp routes that we'll need for this module into our return statement. 
# We'll use f-strings to display them for our investors:
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

# Section 9.5.3 - The next route we'll build is for the precipitation analysis. This route will occur separately from the welcome route.
@app.route("/api/v1.0/precipitation")
def precipitation():
   prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
   precipitation = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >= prev_year).all()
   precip = {date: prcp for date, prcp in precipitation}
   return jsonify(precip)

# Section 9.5.4 - For this route we'll simply return a list of all the stations.
@app.route("/api/v1.0/stations")
def stations():
    results = session.query(Station.station).all()
    stations = list(np.ravel(results))
    return jsonify(stations=stations)

# Section 9.5.5 - For this route, the goal is to return the temperature observations for the previous year.
@app.route("/api/v1.0/tobs")
def temp_monthly():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(Measurement.tobs).\
      filter(Measurement.station == 'USC00519281').\
      filter(Measurement.date >= prev_year).all()
    temps = list(np.ravel(results))
    return jsonify(temps=temps)

# Section 9.5.6 - Our last route will be to report on the minimum, average, and maximum temperatures. 
# However, this route is different from the previous ones in that we will have to provide both a starting and ending date.
@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")
def stats(start=None, end=None):
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    if not end:
        results = session.query(*sel).\
            filter(Measurement.date >= start).\
            filter(Measurement.date <= end).all()
        temps = list(np.ravel(results))
        return jsonify(temps)

    results = session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    temps = list(np.ravel(results))
    return jsonify(temps=temps)




