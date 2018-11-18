from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")


#db = client.mars_scrape
#collection = db.mars_dict


@app.route("/")
def home():

    destination_mars = mongo.db.collection.find_one()

    return render_template("index.html", mars=destination_mars)

@app.route("/scrape")
def scrape():
    mars_dict = scrape_mars.mars_scrape()
    mongo.db.collection.update({}, mars_dict, upsert = True)
    return redirect("/")

if __name__ == '__main__':
    app.run(debug=True)