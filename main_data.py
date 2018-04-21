import sqlite3 as sqlite

def force_update_main_table():
    conn = sqlite.connect('final_project.sqlite')
    cur = conn.cursor()
    try:
        cur.execute('SELECT * FROM Main')
    except:
        statement = '''
                        CREATE TABLE 'Main'(
                            'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
                            'Name' TEXT,
                            'Google' INTEGER,
                            'Yelp' INTEGER,
                            'Zomato' INTEGER 
                            );
                    '''
        cur.execute(statement)
        conn.commit()
    cur.execute('SELECT Name FROM Main')
    in_list = []
    for ii in cur:
        in_list.append(ii[0])
    cur.execute('SELECT Id, Name FROM GOOGLE')
    for ii in list(cur):
        if ii[-1] not in in_list:
            in_list.append(ii[-1])
            dic = {}
            dic['name'] = ii[-1]
            dic['google'] = ii[0]
            insertion = (None, dic['name'], dic['google'], None, None)
            statement = 'INSERT INTO "Main" '
            statement += 'VALUES (?, ?, ?, ?, ?)'
            print('Inserting new data into Main table from Google...')
            cur.execute(statement, insertion)
        else:
            query = '''
                UPDATE Main 
                SET Google = ?
                WHERE Name = ?'''
            params = (ii[0], ii[-1])
            cur.execute(query, params)
    conn.commit()

    cur.execute('SELECT Id, Name FROM Yelp')
    for ii in list(cur):
        if ii[-1] not in in_list:
            in_list.append(ii[-1])
            dic = {}
            dic['name'] = ii[-1]
            dic['yelp'] = ii[0]
            insertion = (None, dic['name'], None, dic['yelp'], None)
            statement = 'INSERT INTO "Main" '
            statement += 'VALUES (?, ?, ?, ?, ?)'
            print('Inserting new data into Main table from Yelp...')
            cur.execute(statement, insertion)
        else:
            query = '''
                UPDATE Main
                SET Yelp = ?
                WHERE Name = ?'''
            params = (ii[0], ii[-1])
            cur.execute(query, params)
    conn.commit()

    cur.execute('SELECT Id, Name FROM Zomato')
    for ii in list(cur):
        if ii[-1] not in in_list:
            in_list.append(ii[-1])
            dic = {}
            dic['name'] = ii[-1]
            dic['Zomato'] = ii[0]
            insertion = (None, dic['name'], None, None, dic['Zomato'])
            statement = 'INSERT INTO "Main" '
            statement += 'VALUES (?, ?, ?, ?, ?)'
            print('Inserting new data into Main table from Zomato...')
            cur.execute(statement, insertion)
        else:
            query = '''
                UPDATE Main
                SET Zomato = ?
                WHERE Name = ?'''
            params = (ii[0], ii[-1])
            cur.execute(query, params)
    conn.commit()

def find_out_location(name_list):
    lng_list = []
    lat_list = []
    text_list = []
    conn = sqlite.connect('final_project.sqlite')
    cur = conn.cursor()
    for name in name_list:
        text_list.append(name)
        statement = '''
                SELECT * FROM Main WHERE Name = "{}";
            '''.format(name)
        cur.execute(statement)
        main_result = cur.fetchone()
        if main_result[2] != None:
            cur.execute('SELECT Geometry FROM Google WHERE Name = "{}"'.format(name))
            google_result = cur.fetchone()[0]
            lat_list.append(google_result[1:-1].split(',')[0])
            lng_list.append(google_result[1:-1].split(',')[1][1:])
        else:
            cur.execute('SELECT Geometry FROM Yelp WHERE Name = "{}"'.format(name))
            yelp_result = cur.fetchone()[0]
            lat_list.append(yelp_result[1:-1].split(',')[0])
            lng_list.append(yelp_result[1:-1].split(',')[1][1:])
    return [lat_list, lng_list, text_list]

def fetch_all(type, location):
    conn = sqlite.connect('final_project.sqlite')
    cur = conn.cursor()
    name_list = []
    cur.execute('SELECT Main.Name FROM Main JOIN Google ON Main.Google = Google.Id WHERE Google.Type = "{}" AND Google.City = "{}"'.format(type, location))
    for ii in cur:
        name_list.append(ii[0])
    cur.execute('SELECT Main.Name FROM Main JOIN Yelp ON Main.Yelp = Yelp.Id WHERE Yelp.Type = "{}" AND Yelp.City ="{}"'.format(type, location))
    for ii in cur:
        if ii[0] not in name_list:
            name_list.append(ii[0])
    return name_list

def fetch_top_rate(type, location, price_range=None):
    if price_range != None:
        min_price = int(price_range.split('-')[0])
        max_price = int(price_range.split('-')[1])
    conn = sqlite.connect('final_project.sqlite')
    cur = conn.cursor()
    dic = {}
    name_list = []
    statement = '''
                    SELECT Name, Rating, Price_level FROM Google WHERE Type = "{}" AND City = "{}"
                '''.format(type, location)
    cur.execute(statement)
    for ii in cur:
        if price_range != None:
            if ii[2] != None:
                if ii[2] >= min_price and ii[2] <= max_price:
                    dic[ii[0]] = ii[1]
        else:
            dic[ii[0]] = ii[1]
    statement = '''
                    SELECT Name, Rating, Price_level FROM Yelp WHERE Type = "{}" AND City = "{}"
                '''.format(type, location)
    cur.execute(statement)
    for ii in cur:
        if price_range != None:
            if ii[2] != None:
                if ii[2] >= min_price and ii[2] <= max_price:
                    if ii[0] in dic:
                        dic[ii[0]] += ii[1]
                        dic[ii[0]] /= 2
                    else:
                        dic[ii[0]] = ii[1]
        else:
            if ii[0] in dic:
                dic[ii[0]] += ii[1]
                dic[ii[0]] /= 2
            else:
                dic[ii[0]] = ii[1]
    result = sorted(dic, key=lambda x:x[1], reverse=True)
    for ii in result[0:5]:
        name_list.append(ii)
    return name_list

def fetch_all_rate(type, location, price_range=None):
    if price_range != None:
        min_price = int(price_range.split('-')[0])
        max_price = int(price_range.split('-')[1])
    conn = sqlite.connect('final_project.sqlite')
    cur = conn.cursor()
    dic = {}
    statement = '''
                        SELECT Name, Rating, Price_level FROM Google WHERE Type = "{}" AND City = "{}"
                    '''.format(type, location)
    cur.execute(statement)
    for ii in cur:
        if price_range != None:
            if ii[2] != None:
                if ii[2] >= min_price and ii[2] <= max_price:
                    dic[ii[0]] = ii[1]
        else:
            dic[ii[0]] = ii[1]
    statement = '''
                        SELECT Name, Rating, Price_level FROM Yelp WHERE Type = "{}" AND City = "{}"
                    '''.format(type, location)
    cur.execute(statement)
    for ii in cur:
        if price_range != None:
            if ii[2] != None:
                if ii[2] >= min_price and ii[2] <= max_price:
                    if ii[0] in dic:
                        dic[ii[0]] += ii[1]
                        dic[ii[0]] /= 2
                    else:
                        dic[ii[0]] = ii[1]
        else:
            if ii[0] in dic:
                dic[ii[0]] += ii[1]
                dic[ii[0]] /= 2
            else:
                dic[ii[0]] = ii[1]
    return dic

def fetch_all_price(type, location, rate_range=None):
    if rate_range != None:
        min_rate = int(rate_range.split('-')[0])
        max_rate = int(rate_range.split('-')[1])
    conn = sqlite.connect('final_project.sqlite')
    cur = conn.cursor()
    dic = {}
    statement = '''
                            SELECT Name, Price_level, Rating FROM Google WHERE Type = "{}" AND City = "{}"
                        '''.format(type, location)
    cur.execute(statement)
    for ii in cur:
        if rate_range != None:
            if ii[2] >= min_rate and ii[2] <= max_rate:
                if ii[1] != None:
                    dic[ii[0]] = ii[1]
        elif ii[1] != None:
            dic[ii[0]] = ii[1]
    statement = '''
                            SELECT Name, Price_level, Rating FROM Yelp WHERE Type = "{}" AND City = "{}"
                        '''.format(type, location)
    cur.execute(statement)
    for ii in cur:
        if rate_range != None:
            if ii[2] >= min_rate and ii[2] <= max_rate:
                if ii[1] != None:
                    if ii[0] in dic:
                        dic[ii[0]] += ii[1]
                        dic[ii[0]] /= 2
                    else:
                        dic[ii[0]] = ii[1]
        elif ii[1] != None:
            if ii[0] in dic:
                dic[ii[0]] += ii[1]
                dic[ii[0]] /= 2
            else:
                dic[ii[0]] = ii[1]
    return dic

def fetch_one_info(name):
    conn = sqlite.connect('final_project.sqlite')
    cur = conn.cursor()
    dic = {'City':None, 'Type':None, 'Rating':None, 'Addr':None, 'Price':None, 'Review': []}
    cur.execute('SELECT City, Type, Rating, Address, Price_level FROM Google WHERE Name = "{}"'.format(name))
    google_result = cur.fetchone()
    if google_result != None:
        dic['City'] = google_result[0]
        dic['Type'] = google_result[1]
        dic['Rating'] = google_result[2]
        dic['Addr'] = google_result[3]
        if google_result[4] != None:
            dic['Price'] = google_result[4]
    cur.execute('SELECT City, Type, Rating, Address, Price_level FROM Yelp WHERE Name = "{}"'.format(name))
    yelp_result = cur.fetchone()
    if yelp_result != None:
        if dic['City'] == None:
            dic['City'] = yelp_result[0]
        if dic['Type'] == None:
            dic['Type'] = yelp_result[1]
        if dic['Rating'] == None:
            dic['Rating'] = yelp_result[2]
        else:
            dic['Rating'] += yelp_result[2]
            dic['Rating'] /= 2
        if dic['Addr'] == None:
            dic['Addr'] = yelp_result[3]
        if yelp_result[4] != None:
            if dic['Price'] == None:
                dic['Price'] = yelp_result[4]
            else:
                dic['Price'] += yelp_result[4]
                dic['Price'] /= 2
    cur.execute('SELECT Review1, Review2, Review3 FROM Zomato WHERE Name = "{}"'.format(name))
    zomato_result = cur.fetchone()
    for ii in zomato_result:
        dic['Review'].append(ii)
    return dic
