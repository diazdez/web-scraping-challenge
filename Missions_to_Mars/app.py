# Dependencies
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# Create an instance of Flask
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")

# "root route" to render HTML template using data from mongo
@app.route("/")
def index():

    # Find one rcd of data from the mongo database
    mars_rcd = mongo.db.mars_collection.find_one()

    # Return template and data
    return render_template("index.html", mars = mars_rcd)

# create scrape route 
# this route that will trigger the scrape function
@app.route("/scrape")
def scrape():
    mars_collection = mongo.db.mars_collection
    # run the scrape function for "scrape_mars.py"
    mars_scraped_data = scrape_mars.scrape()

    # insert the mars_scraped_data in to the collection
    mars_collection.update({}, mars_scraped_data, upsert=True)

    # go back to the home/main page
    return redirect("/")

# run the app
if __name__ == "__main__":
    app.run(debug=True)
