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

    # Find one record of data from the mongo database
    mars_data = mongo.db.mars_data.find_one()

    #make auto generated table a bootstrap style table
    mars_data["mars_fact_table"]=mars_data["mars_fact_table"].replace('<table border="1" class="dataframe">',"<table class='table table-sm'>")

    return render_template("index.html", mission_mars=mars_data)


# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():

    # Run the scrape function and save the results to a variable
    scraped_data = scrape_mars.scrape()

    # Update the Mongo database using update and upsert=True
    mars_data.update({}, scraped_data, upsert=True)

    # Redirect to the scraped data page
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)