import main

GUESTBOOK_ENTRIES_FILE = "entries.json"
entries = []
title = ""

def init():
    global entries
    global title
    global PRICERANGE
    PRICERANGE = None
    title = ""
    entries = []

def get_entries():
    global entries
    return entries

def get_title():
    global title
    return title

def get_price_range():
    global PRICERANGE
    return PRICERANGE

def get_reviews(name):
    global entries
    for ii in entries:
        if name == ii.name:
            return ii.review

def get_top_rate(price_range):
    global TYPE, CITY
    return main.fetch_top_rate(TYPE, CITY, price_range)

def add_entry(type, city):
    global entries, title, TYPE, CITY, Location
    TYPE = type
    CITY = city
    entries = main.create_obj(type, city)
    if len(entries) == 0:
        raise(NameError)
    title = main.make_title(type, city)
    name_list = []
    for ii in entries:
        name_list.append(ii.name)
    Location = main.find_out_location(name_list)

def add_pricerange(price):
    global PRICERANGE
    PRICERANGE = price

def set_location(location):
    global Location
    Location = location

def get_location():
    global Location
    return Location

def get_all_rate():
    global TYPE, CITY
    return main.fetch_all_rate(TYPE, CITY, None)

def get_all_price():
    global TYPE, CITY
    return main.fetch_all_price(TYPE, CITY, None)

def destroy():
    global entries, title, PRICERANGE, TYPE, CITY, Location
    entries = []
    title = ""
    PRICERANGE = None
    TYPE = ""
    CITY = ""
    Location = []