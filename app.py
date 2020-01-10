# import necessary libraries
from flask import Flask, render_template, jsonify, redirect
from flask_pymongo import PyMongo
import scrape_mars

# create instance of Flask app
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
#mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

# Define the collection and drop any existing data for this exercise
mars_db = mongo.db.mars
#mars_db.drop()

# Create route that renders index.html template
@app.route('/')
def index():
    # Find one record of data from the mongo database
    destination_data = mars_db.find_one()
    # Return template and data
    return render_template("index.html", mars=destination_data)

# Route that will trigger the scrape function
@app.route('/scrape')
def scrape():
    # Run the scrape function
    mars = scrape_mars.scrape()
    # Insert the results into the database
    mars_db.insert_one(mars)
    # The option below would update the existing record (or insert)
    #mars_db.update_one({}, mars, upsert=True)

    # Redirect back to home page
    return redirect("/")

if __name__ == '__main__':
    app.run(debug=True)
