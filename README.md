# **Planet Mars Web Scraping App**

## **Overview of Project**
This project's focus is on the creation a simple web app that has web scraping functionality and can store the results in a MongoDB database. The context for the app is information about the planet Mars. The app is split into four main sections as follows:

1. News: An article title and summary for the current day
1. Featured Image: A featured image for the current day
1. Facts Table: A facts comparison table between Mars and Earth
1. Hemispheres: Images of the different hemispheres of mars

### **Web Scraping Prototype**
The notebook *[Mission_to_Mars_Challenge.ipynb](/Mission_to_Mars_Challenge.ipynb)* contains the prototyping of the web scraping functionality. Here, tools such as the webdriver Splinter, html parsing Beautiful Soup and pandas are used to scrape four different URLs containing various information about Mars.

### **Convert Prototype to Module for use in App**
The notebook is then exported as a python script and refactored to work as a supporting module for the web app (see *[scraping.py](/scraping.py)*). Here four functions (`mars_news()`, `featured_image()`, `mars_facts()`, and `hemisphere_images()`) were created from the prototype code to collect data for the four sections of the app. The final function `scrape_all()` contains all the logic for running the scraping process and is used in the app's script *[app.py](/app.py)* for the scraping route.

### **Constructing the App**
The app is constructed using the Flask framework and connects to MongoDB via the `flask_pymongo` library. Two routes are established, one for rendering the html template along with any data stored in the database, and one for running the web scraping function `scrape_all()` via a button on the web page. The second route also stores the results that are retrieved during the scraping process in the database.

### **Basic Styling and Two Additional Component Styles**
As far as styling the app, components from Bootstrap 5.1.3 are used to shape and organize the page. CSS inline styling was also employed to improve the spacing between elements and add a background image to the header section.

Past the basic styling, two further Bootstrap components were used to enhance the page. The first was the enhancement made to the Mars facts table using the `table-dark`, and `table-striped` utility classes. These classes were passed as the `classes` argument to the pandas `read_html()` function since this is where the html for the table is created. The second enhancement was the addition of an image carousel that allows for cycling through the different Mars hemisphere images that are retrieved in the scraping process. This component was added directly to the *[index.html](/templates/index.html)* file.

## **Future Work**
Currently the URLs scraped in this project hold placeholder articles that I would like to replace with current articles related to Mars from the websites these URLs are inspired by. An additional goal will be to host this project online as this would be an excellent exercise in how to deploy a web project.
