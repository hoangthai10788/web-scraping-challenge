from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars


# Create an instance of Flask
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_info")


# Route to render index.html template using data from Mongo
@app.route("/")
def home():

    # Find one record of title and para data from the mongo database
    title_and_para_data = mongo.db.title_and_para_col.find_one()

    # Find one record of featured image data from the mongo database
    featured_image_data = mongo.db.featured_image_col.find_one()

    # Find one record of mars facts data from the mongo database
    mars_facts_data = mongo.db.mars_weather_col.find_one()

    # Image 1
    img1_data = mongo.db.mars_img1_col.find_one()

    # Image 2
    img2_data = mongo.db.mars_img2_col.find_one()

    # Image 3
    img3_data = mongo.db.mars_img3_col.find_one()

    # Image 4
    img4_data = mongo.db.mars_img4_col.find_one()



    # Return template and data
    return render_template("index.html", title_para=title_and_para_data, featured_img = featured_image_data, facts = mars_facts_data, img1 = img1_data, img2 = img2_data, img3 = img3_data, img4 = img4_data)


# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():

    # Run the scrape title and para function
    title_and_paragraph = scrape_mars.title_and_para()
    mongo.db.title_and_para_col.update({}, title_and_paragraph, upsert=True)

    # Run and scrape featured image function
    featured_image = scrape_mars.featured_image()
    mongo.db.featured_image_col.update({}, featured_image, upsert=True)

    # Run and scrape mars_weather function
    mars_facts = scrape_mars.mars_weather()
    mongo.db.mars_weather_col.update({}, mars_facts, upsert=True)

    # Run and scrape mars_hemisphere function
    mars_hemisphere_image = scrape_mars.mars_hemispheres()

    # Image 1
    mars_img1 = mars_hemisphere_image[0]
    mongo.db.mars_img1_col.update({}, mars_img1, upsert=True)

    # Image 2
    mars_img2 = mars_hemisphere_image[1]
    mongo.db.mars_img2_col.update({}, mars_img2, upsert=True)

    # Image 3
    mars_img3 = mars_hemisphere_image[2]
    mongo.db.mars_img3_col.update({}, mars_img3, upsert=True)

    # Image 4
    mars_img4 = mars_hemisphere_image[3]
    mongo.db.mars_img4_col.update({}, mars_img4, upsert=True)
    


    # Redirect back to home page
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)