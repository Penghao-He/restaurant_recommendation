import requests
import json
import secret
import sqlite3 as sqlite

API_KEY = secret.yelp_key
# START OF CACHE-SPECIFIC FUNCTIONS

CACHE_FILENAME = 'Yelp.json'
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


def get_from_yelp(type, location):
    load_cache_from_file()
    # END OF CACHE-SPECIFIC FUNCTIONS
    name = type.lower() + " in " + location.lower()
    request_key = construct_cache_key(name)
    if request_key in CACHE:
        # The response is already present in our cache
        final_list = CACHE[request_key]
        return final_list
    else:
        baseurl = 'https://api.yelp.com/v3/businesses/search'
        params = {}
        params['term'] = type
        params['location'] = location
        params['limit'] = 50
        headers = {'Authorization': 'bearer %s' % API_KEY}
        print('Making new request from Yelp...')
        response_text = requests.get(url=baseurl, params=params, headers=headers)
        final_list = json.loads(response_text.text)['businesses']
        # Cache this response and save the cache to file
        CACHE[request_key] = final_list
        save_cache_to_file()
        return final_list

def insert_yelp_table(type, data):
    conn = sqlite.connect('final_project.sqlite')
    cur = conn.cursor()
    statement = '''
            SELECT * FROM Yelp;
        '''
    try:
        cur.execute(statement)
    except:
        statement = '''
                CREATE TABLE 'Yelp'(
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
            SELECT * FROM Yelp;
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
            if 'location' in ii.keys():
                dic['display_address'] = " ".join(ii['location']['display_address'])
            else:
                dic['display_address'] = None
            if 'location' in ii.keys():
                dic['city'] = ii['location']['city']
            else:
                dic['city'] = None
            if 'price' in ii.keys():
                dic['price'] = len(ii['price'])
            else:
                dic['price'] = None
            if 'coordinates' in ii.keys():
                dic['coordinates'] = '(' + str(ii['coordinates']['latitude']) + ', ' + str(
                    ii['coordinates']['longitude']) + ')'
            else:
                dic['coordinates'] = None

            insertion = (
            None, dic['name'], dic['city'], type, dic['rating'], dic['display_address'], dic['coordinates'],
            dic['price'])
            statement = 'INSERT INTO "Yelp" '
            statement += 'VALUES (?, ?, ?, ?, ?, ?, ?, ?)'
            print('Inserting new data into Yelp table...')
            cur.execute(statement, insertion)
            data_in.append(ii['name'])
        conn.commit()