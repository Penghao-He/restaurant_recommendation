import requests
import json
import secret
import sqlite3 as sqlite

API_KEY = secret.zomato_key

CACHE_FILENAME = 'Zomato.json'
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


def get_location_id_from_zomato(location):
    load_cache_from_file()
    # END OF CACHE-SPECIFIC FUNCTIONS
    request_key = construct_cache_key(location)
    if request_key in CACHE:
        # The response is already present in our cache
        final_result = CACHE[request_key]
        return final_result
    else:
        baseurl = 'https://developers.zomato.com/api/v2.1/locations'
        header = {}
        header['user-key'] = API_KEY
        params = {}
        params['query'] = location
        response_text = requests.get(url=baseurl, params=params, headers=header)
        print('Making new request from Zomato for location...')
        resp_text = json.loads(response_text.text)
        if resp_text['status'] == 'success':
            final_result = (resp_text['location_suggestions'][0]['entity_type'], resp_text['location_suggestions'][0]['entity_id'])
        else:
            print('Cannot find '+location+' in Zomato!')
            return
        # Cache this response and save the cache to file
        CACHE[request_key] = final_result
        save_cache_to_file()
        return final_result

def get_rest_id_from_zomato(name, location_tuple):
    load_cache_from_file()
    # END OF CACHE-SPECIFIC FUNCTIONS
    request_key = construct_cache_key(name+" "+location_tuple[0]+" "+str(location_tuple[1])+' id')
    if request_key in CACHE:
        # The response is already present in our cache
        final_result = CACHE[request_key]
        return final_result
    else:
        baseurl = 'https://developers.zomato.com/api/v2.1/search'
        header = {}
        header['user-key'] = API_KEY
        params = {}
        params['entity_type'] = location_tuple[0]
        params['entity_id'] = location_tuple[1]
        params['q'] = name
        response_text = requests.get(url=baseurl, params=params, headers=header)
        print('Making new request from Zomato for restuarant id...')
        resp_text = json.loads(response_text.text)
        if resp_text['results_found'] != 0:
            for ii in resp_text['restaurants']:
                if ii['restaurant']['name'].lower() == name:
                    final_result = ii['restaurant']['id']
            final_result = resp_text['restaurants'][0]['restaurant']['id']
        else:
            print('Cannot find '+name+' in Zomato!')
            return
        # Cache this response and save the cache to file
        CACHE[request_key] = final_result
        save_cache_to_file()
        return final_result

def get_review_from_zomato(name, location):
    load_cache_from_file()
    # END OF CACHE-SPECIFIC FUNCTIONS
    name = name.lower()
    location = location.lower()
    request_key = construct_cache_key(name+" "+location)
    if request_key in CACHE:
        # The response is already present in our cache
        final_result = CACHE[request_key]
        return final_result
    else:
        location_tuple = get_location_id_from_zomato(location)
        rest_id = get_rest_id_from_zomato(name, location_tuple)
        if rest_id == None:
            return
        baseurl = 'https://developers.zomato.com/api/v2.1/reviews'
        header = {}
        header['user-key'] = API_KEY
        params = {}
        params['res_id'] = rest_id
        response_text = requests.get(url=baseurl, params=params, headers=header)
        print('Making new request from Zomato for review...')
        resp_text = json.loads(response_text.text)
        if resp_text['reviews_count'] != 0:
            final_result = [ii['review']['review_text'] for ii in resp_text['user_reviews']]
        else:
            print('No review for '+name)
            return
        # Cache this response and save the cache to file
        CACHE[request_key] = final_result
        save_cache_to_file()
        return final_result

def insert_zomato_table(data):
    conn = sqlite.connect('final_project.sqlite')
    cur = conn.cursor()
    statement = '''
            SELECT * FROM Zomato;
        '''
    try:
        cur.execute(statement)
    except:
        statement = '''
                        CREATE TABLE 'Zomato'(
                            'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
                            'Name' TEXT,
                            'City' TEXT,
                            'Review1' TEXT,
                            'Review2' TEXT,
                            'Review3' TEXT
                            );
                    '''
        cur.execute(statement)
    data_in = []
    for ii in cur:
        data_in.append(ii[1])
    for ii in data:
        if ii[0] not in data_in:
            dic = {}
            dic['name'] = ii[0]
            dic['city'] = ii[1]
            if len(ii) == 2:
                dic['review1'] = None
                dic['review2'] = None
                dic['review3'] = None
            elif len(ii) == 3:
                dic['review1'] = ii[2]
                dic['review2'] = None
                dic['review3'] = None
            elif len(ii) == 4:
                dic['review1'] = ii[2]
                dic['review2'] = ii[3]
                dic['review3'] = None
            else:
                dic['review1'] = ii[2]
                dic['review2'] = ii[3]
                dic['review3'] = ii[4]

            insertion = (None, dic['name'], dic['city'], dic['review1'], dic['review2'], dic['review3'])
            statement = 'INSERT INTO "Zomato" '
            statement += 'VALUES (?, ?, ?, ?, ?, ?)'
            print('Inserting new data into Zomato table...')
            cur.execute(statement, insertion)
            data_in.append(ii[0])
        conn.commit()
