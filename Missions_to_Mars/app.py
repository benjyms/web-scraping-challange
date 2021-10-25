#createing script for flask app
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

#Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)
mars_data = mongo.db.mars_data

# or set inline
 # mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")


@app.route("/")
def home():

    # Return template
    return render_template("index.html")


# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():

    # Run the scrape function and save the results to a variable
    scraped_data = scrape_mars.scrape()

    # Update the Mongo database using update and upsert=True
    mars_data.update({}, scraped_data, upsert=True)

    # Redirect to the scraped data page
    return redirect("/data")

# Route to render data.html template using data from Mongo
@app.route("/data")
def data():

    # Find one record of data from the mongo database
    mars_info = mongo.db.mars_data.find_one()

    # Return template and data
    return render_template("data.html", info=mars_info)

if __name__ == "__main__":
    app.run(debug=True)