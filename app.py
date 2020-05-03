import numpy as np 
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///resources/hawaii.sqlite")
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement

Station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

last_year = dt.datetime(2017, 8, 23) - dt.timedelta(days=365)
#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"<h1>Hawaii Data</h1><br>"
        f"<h2>Choose from the Available Routes:</h2><br/> "
        f"Precipitation returns a list of precipitation values the year ranging 2016-08-23 to 2017-08-23.<br /> <br />"
        f"<li>/api/v1.0/precipitation</li><br/><br />"
        f"Stations returns a list of all the stations and information about that station. <br /><br />"
        f"<li>/api/v1.0/stations</li><br /> <br />"
        f"Returns temperature observations for the year ranging 2016-08-23 to 2017-08-23."
        f"<li>/api/v1.0/tobs</li><br /><br />"
        f"Type in a date in the format YYYY-MM-DD between 2016-08-23 to 2017-08-23<br />"
        f"to find the Max, Min, and Average Temperature on that day."
        f"<li>/api/v1.0/<start></li><br /><br />"
        f"Type in a start date and end date in the format YYYY-MM-DD between 2016-08-23 to 2017-08-23<br>"
        f"to find the Max, Min, and Average Temperatures for days in that range."
        f"<li>/api/v1.0/<start>/<end></li><br />"

    )
@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all precipitation values"""
    # Query all passengers
    results = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date > last_year).order_by(Measurement.date).all()
    # create a list for the results
    
    prcp_info = []
    for prcp in results:
        prcp_data = {}
        prcp_data["Date"] = prcp.date
        prcp_data["Temp"] = prcp.prcp
        prcp_info.append(prcp_data)

    return jsonify(prcp_info)


@app.route("/api/v1.0/station")
def station():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all stations """

    results_2 = session.query(Station).all()
    
    station_info = []

    for station in results_2:
        station_data = {}
        station_data["Name"] = station.station
        station_data["Latitude"] = station.latitude
        station_data["Longitude"] = station.longitude
        station_data["Elevation"] = station.elevation
        station_info.append(station_data)

    return jsonify(station_info)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all tobs values"""
   
    results_3 = session.query(Measurement.station, Measurement.date, Measurement.tobs).\
        group_by(Measurement.date).filter(Measurement.date > last_year).order_by(Measurement.station).all()
    
    tobs_results = []

    for tobs in results_3:
        tobs_data = {}
        tobs_data["Station"] = tobs.station
        tobs_data["Date"] = tobs.date
        tobs_data["TOBS"] = tobs.tobs
        tobs_results.append(tobs_data)

    return jsonify(tobs_results)

@app.route("/api/v1.0/<start>")
def start_date(start=None):

    # Create our session (link) from Python to the DB
    session = Session(engine)

    results_4 = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
        filter(Measurement.date >= start).all()
    temp_stats = []

    for Tmin, Tmax, Tavg in results_4: 
       temp_data = {}
       temp_data["Minum Temp"] = Tmin
       temp_data["Maximum Temp"] = Tmax
       temp_data["Average Temp"] = Tavg
       
       temp_stats.append(temp_data)
       
       return jsonify(temp_stats)

@app.route("/api/v1.0/<start>/<end>")
def start_end_date(start=None, end=None):

    # Create our session (link) from Python to the DB
    session = Session(engine)

    results_5 = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
        filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    temp_stats = []

    for Tmin, Tmax, Tavg in results_5: 
       temp_data = {}
       temp_data["Minum Temp"] = Tmin
       temp_data["Maximum Temp"] = Tmax
       temp_data["Average Temp"] = Tavg
       
       temp_stats.append(temp_data)
       
       return jsonify(temp_stats)
    



if __name__ == '__main__':
    app.run(debug=True)
