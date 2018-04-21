import requests
import json
import secret
import sqlite3 as sqlite


API_KEY = secret.google_places_key
# START OF CACHE-SPECIFIC FUNCTIONS

CACHE_FILENAME = 'Google.json'
CACHE = None

def save_cache_to_file():
    if CACHE is not None:
        f = open(CACHE_FILENAME, 'w')
        f.write(json.dumps(CACHE))
        f.close()
        # print('Saved cache to', CACHE_FILENAME)


def load_cache_from_file():
    global CACHE
    try:
        f = open(CACHE_FILENAME, 'r')
        CACHE = json.loads(f.read())
        f.close()
    except:
        # Cache file does not exist, initialize an empty cache
        CACHE = {}
        save_cache_to_file()


def construct_cache_key(name):
    return '+'.join(name.split())


def get_from_google(type, location):
    load_cache_from_file()
    # END OF CACHE-SPECIFIC FUNCTIONS
    name = type.lower() + " in " + location.lower()
    request_key = construct_cache_key(name)
    if request_key in CACHE:
        # The response is already present in our cache
        final_list = CACHE[request_key]
        return final_list
    else:
        baseurl = "https://maps.googleapis.com/maps/api/place/textsearch/json?"
        params = {}
        params['query'] = request_key
        params['key'] = API_KEY
        params['types'] = 'restaurant'
        print('Making new request from Google...')
        response_text = requests.get(baseurl, params=params)
        final_list = json.loads(response_text.text)['results']
        # Cache this response and save the cache to file
        CACHE[request_key] = final_list
        save_cache_to_file()
        return final_list

def insert_google_table(type, data):
    conn = sqlite.connect('final_project.sqlite')
    cur = conn.cursor()
    statement = '''
        SELECT * FROM Google;
    '''
    try:
        cur.execute(statement)
    except:
        statement = '''
            CREATE TABLE 'Google'(
                'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
                'Name' TEXT,
                'City' TEXT,
                'Type' TEXT,
                'Rating' REAL,
                'Address' TEXT,
                'Geometry' TEXT,
                'Price_level' INTEGER
                );
        '''
        cur.execute(statement)
        conn.commit()
    statement = '''
        SELECT * FROM Google;
    '''
    cur.execute(statement)
    data_in = []
    for ii in cur:
        data_in.append(ii[1])
    for ii in data:
        if ii['name'] not in data_in:
            dic = {}
            if 'name' in ii.keys():
                dic['name'] = ii['name']
            else:
                dic['name'] = None
            if 'rating' in ii.keys():
                dic['rating'] = ii['rating']
            else:
                dic['rating'] = None
            if 'formatted_address' in ii.keys():
                dic['formatted_address'] = ii['formatted_address']
                dic['city'] = ii['formatted_address'].split(',')[-3][1:]
            else:
                dic['formatted_address'] = None
            if 'price_level' in ii.keys():
                dic['price_level'] = ii['price_level']
            else:
                dic['price_level'] = None
            if 'geometry' in ii.keys():
                dic['geometry'] = '(' + str(ii['geometry']['location']['lat']) + ', ' + str(
                    ii['geometry']['location']['lng']) + ')'
            else:
                dic['geometry'] = None

            insertion = (None, dic['name'], dic['city'], type, dic['rating'], dic['formatted_address'], dic['geometry'],
                         dic['price_level'])
            statement = 'INSERT INTO "Google" '
            statement += 'VALUES (?, ?, ?, ?, ?, ?, ?, ?)'
            print('Inserting new data into Google table...')
            cur.execute(statement, insertion)
            data_in.append(ii['name'])
        conn.commit()