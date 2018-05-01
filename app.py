from flask import Flask, render_template, jsonify, redirect
#from flask_pymongo import PyMongo
import pymongo
import scrape_mars

app = Flask(__name__)

#mongo = PyMongo(app)
conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)
db = client.mars
collection = db.mars_scrape

@app.route("/")
def index():
    mars = db.collection.find_one()
    return render_template("index.html", mars=mars)


@app.route("/scrape")
def scrape():
    mars = db.collection
    mars_data = scrape_mars.scrape()
    mars.update(
        {},
        mars_data,
        upsert=True
    )
    return redirect("http://localhost:5000/", code=302)


if __name__ == "__main__":
    app.run(debug=True)