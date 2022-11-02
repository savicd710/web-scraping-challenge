from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# Create an instance of Flask
app = Flask(__name__)

# Use PyMongo to set up mongo connection
mongo = PyMongo(app, uri='mongodb://localhost:27017/mars_app')

# Initial path
@app.route("/")
def home():
    # Find one document from our mongo db and return it
    mars_data = mongo.db.mars_data.find_one()
    # Pass the mars data to render template
    return render_template('index.html', mars_data=mars_data)

# Scrape path
@app.route("/scrape")
def data_scrape():
    # Create a mars_data database
    mars_data = mongo.db.mars_data
    # Call the scrape function from scrape_mars
    mars_dict = scrape_mars.scrape()
    # Update the database
    mars_data.update_one({}, {"$set":mars_dict}, upsert=True)
    # Return to home page
    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)