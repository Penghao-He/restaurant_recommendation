# restaurant-recommend-app
[App introduction]<br>
This app is used to get some info (e.g., location on map, rating, price level, reviews sample) about a type of restaurant (e.g., Chinese) in a specific area (e.g., Ann Arbor). <br>
<br>
N
[Data source and secret.py format] <br>
The data sources are <br>
<ul>
<li>Google Place API: https://developers.google.com/places/web-service/details </li>
<li>Yelp: https://www.yelp.com/developers/documentation/v3/business_search </li>
<li>Zomato: https://developers.zomato.com/api </li>
</ul>
All the API keys could be easily applied by registrating an account.<br><br>
Note that before using the app, users need to create a file named "secret.py" (not secrets.py) and the format should be looked like this:<br>
<br>
google_places_key = '****'<br>
yelp_key = '****'<br>
zomato_key = '****'<br>
mapbox_access_token = '****'<br>
<br>
[Prerequisite]<br>
Before running the app, users need to create a virtual environment and install the necessary package like this:<br>
<br>
$ pip install -r requirements.txt
<br>
And the required packages are listed in "requirements.txt" <br>
<strong>Users are required to log in a poorly account before using the app<./strong><br>
<br>
[How to run the app]<br>
After installing the app, users can run the app like this:<br>
$ python app.py
<br>
And just follow the instruction and you can enjoy it (do not try to use invalid input since I have not set up a system to correct the invalid input thanks).<br>

[Code structure]<br>
The code contains several parts:
<ul>
<li>app.py: the flask pages definition file responsible for connecting with the html pages in templates</li>
<li>model.py: the basic model of the flask app</li>
<li>google_data.py: retrieve data through Google API and store the data in cache as well as database</li>
<li>y_data.py: retrieve data through Yelp API and store the data in cache as well as database</li>
<li>zomato_data.py: retrieve data through Zomato API and store the data in cache as well as database</li>
<li>main_data.py: create and insert and retrieve data from database</li>
<li>plot.py: some plot function to plot location map using plotly</li>
<li>main.py: some other function to get new data and create instances</li>
<li>test.py: unittest</li>
</ul>
Note that each restaurant info will be store temporarily as an instance and the main functions are like:
<ul>
<li>make_new_search: make a new search on given "type" and "location", and get the info through API and store them into cache and database</li>
<li>fetch_all: fetch relavent data from database on given "type" and "location"</li>
<li>create_obj: given specific "type" and "location" and using the data retrieved by "fetch_all" to create instances</li>
</ul>
