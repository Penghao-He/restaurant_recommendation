from google_data import *
from y_data import *
from zomato_data import *
from main_data import *
from plot import *

class Rest():
    def __init__(self, name, city, type, rating, price, address, review):
        self.name = name
        self.city = city
        self.type = type
        self.rating = rating
        self.price = price
        self.address = address
        self.review = review

def make_new_search(name, location):
    d1 = get_from_google(name, location)
    d2 = get_from_yelp(name, location)
    name_list = []
    for ii in d1:
        name_list.append(ii['name'])
    for ii in d2:
        if ii['name'] not in name_list:
            name_list.append(ii['name'])
    d3 = []
    for ii in name_list:
        result = get_review_from_zomato(ii, location)
        if result != None:
            d3.append([ii, location] + result)
        else:
            d3.append([ii, location])
    insert_google_table(name, d1)
    insert_yelp_table(name, d2)
    insert_zomato_table(d3)
    force_update_main_table()
    return name_list

def create_obj(type, location):
    obj_list = []
    name_list = fetch_all(type, location)
    for ii in name_list:
        name = ii
        info = fetch_one_info(name)
        city = info['City']
        type = info['Type']
        rating = info['Rating']
        addr = info['Addr']
        price = info['Price']
        review = info['Review']
        obj = Rest(name, city, type, rating, price, addr, review)
        obj_list.append(obj)
    return obj_list


def make_title(name, location):
    return "{} Restaurant in {}".format(name, location)


if __name__ == "__main__":
    # print(make_new_search('Chinese', 'Ann Arbor'))
    # type = 'Chinese'
    # location = "Ann Arbor"
    # obj_list = create_obj(type, location)

    # name_list = fetch_all('Chinese', 'San Mateo')
    # print(name_list)
    # name_list = fetch_top_rate('Chinese', 'San Mateo', '1-2')
    # print(name_list)
    # location = find_out_location(name_list)
    # plot_location(location[0], location[1], location[2], "Italian Restaurant in Ann Arbor")

    # rate = fetch_all_rate('Chinese', 'Ann Arbor', None)
    # print(rate)
    # plot_rate(rate, "Chinese Restaurant in Ann Arbor")

    # price = fetch_all_price('Chinese', 'San Mateo', None)
    # print(price)
    # plot_price(price, 'Chinese Restaurant in Ann Arbor')
    pass
