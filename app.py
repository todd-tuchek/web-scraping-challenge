# Dependencies
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo  
from scrape_mars import scrape_info
import os

#################
# FLASK SETUP
#################
app = Flask(__name__)

# Use Flask_pymongo to set up monogo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")

# Create a route that renders the index.html template and finds documents from mongo
@app.route("/")
def home(): 
    # Find one record of data from mogno db
    mars_data = mongo.db.mars.find_one()

    # Return template and data
    return render_template("index.html", mars=mars_data)

# Route that will trigger scrape function
@app.route("/scrape")
def scrape(): 

    # Run the scrape function and save resutls to a variable
    results = scrape_info()

    # Update the Mongo Database using update and upsert=True
    mongo.db.mars.update({}, results, upsert=True)

    return redirect ("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)

