import datetime
from dateutil.relativedelta import relativedelta
import sqlalchemy
from sqlalchemy import create_engine,func
from sqlalchemy.orm import Session
from sqlalchemy.ext.automap import automap_base
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from flask import Flask, jsonify



#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return the dates and precipitation observations from the last year"""
    max_date = session.query(func.max(Measurement.date))[0][0]
    last_12_month = max_date + relativedelta(months=-12)
    results = session.query(Measurement.date, Measurement.prcp).\
                               filter(Measurement.date>last_12_month).all()
    precipitation_list = []
    for precipitation in results:
        precipitation_dict = {}
        precipitation_dict["date"] = precipitation.date
        precipitation_dict["prcp"] = precipitation.prcp
        precipitation_list.append(precipitation_dict)

    return jsonify(precipitation_list)

@app.route("/api/v1.0/stations")
def stations():
    """Return all the stations"""
    results = session.query(Station.name).all()
    station_list = []
    for station in results:
        station_list.append(station.name)

    return jsonify(station_list)

@app.route("/api/v1.0/tobs")
def tobs():
    """Return the dates and temperature observations from the last year"""
    max_date = session.query(func.max(Measurement.date))[0][0]
    last_12_month = max_date + relativedelta(months=-12)
    results = session.query(Measurement.date, Measurement.tobs).\
                               filter(Measurement.date>last_12_month).all()
    tobs_list = []
    for tob in results:
        tobs_dict = {}
        tobs_dict["date"] = tob.date
        tobs_dict["tobs"] = tob.tobs
        tobs_list.append(tobs_dict)

    return jsonify(tobs_list)

@app.route("/api/v1.0/<start>")
def calc_temps(start):
    """Return a list of the minimum temperature, 
    the average temperature, and the max temperature 
    for a given start range."""
    start_date = datetime.datetime.strptime(start, '%Y-%m-%d').date() + relativedelta(months=-12)
    
    tmin,tavg,tmax = session.query(func.min(Measurement.tobs),func.avg(Measurement.tobs),func.max(Measurement.tobs)).\
                               filter(Measurement.date>=start_date).first()
  
    temps_dict = {}
    temps_dict["TMIN"] = tmin
    temps_dict["TAVG"] = tavg
    temps_dict["TMAX"] = tmax

    return jsonify(temps_dict)

@app.route("/api/v1.0/<start>/<end>")
def calc_temps_end(start,end):
    """Return a list of the minimum temperature, 
    the average temperature, and the max temperature 
    for a given start-end range."""
    start_date = datetime.datetime.strptime(start, '%Y-%m-%d').date() + relativedelta(months=-12)
    end_date = datetime.datetime.strptime(end, '%Y-%m-%d').date() + relativedelta(months=-12)
    tmin, tavg, tmax = session.query(func.min(Measurement.tobs),func.avg(Measurement.tobs),func.max(Measurement.tobs)).\
                               filter(Measurement.date>=start_date).\
                               filter(Measurement.date<=end_date).first()
    temps_dict = {}
    temps_dict["TMIN"] = tmin
    temps_dict["TAVG"] = tavg
    temps_dict["TMAX"] = tmax

    return jsonify(temps_dict)

if __name__ == '__main__':
    app.run(port=8082,debug=True)