import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt
from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///./Resources/hawaii.sqlite")

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


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end> "

    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    query_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    
    date_prcp = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >= query_date).\
    order_by(Measurement.date).all()
    
    session.close()

    # Convert list of tuples into normal list
    all_prcp = []
    for date, prcp in date_prcp:
        prcp_date = {}
        prcp_date["date"] = date
        prcp_date["prcp"] = prcp
        all_prcp.append(prcp_date)
    
    # all_names = list(np.ravel(results)) - will help on next route

    return jsonify(all_prcp)


if __name__ == '__main__':
    app.run(debug=True)
