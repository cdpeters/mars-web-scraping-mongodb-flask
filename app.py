from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo
import scraping

app = Flask(__name__)

# Use flask_pymongo to set up a mongo connection to the mars_app database
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)


@app.route("/")
def index():
    """Retrieve data from DB and render the html template"""
    # mongo.db.mars is a collection in the mars_app database
    mars = mongo.db.mars.find_one()
    return render_template("index.html", mars=mars)


@app.route("/scrape")
def scrape():
    """Run scraping script and update DB, redirect to index route"""
    mars = mongo.db.mars
    mars_data = scraping.scrape_all()
    mars.update_one({}, {"$set": mars_data}, upsert=True)
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run()

