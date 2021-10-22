#createing script for flask app
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

#Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

# or set inline
 # mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")

@app.route("/")
def index():
    # pick up here when ready