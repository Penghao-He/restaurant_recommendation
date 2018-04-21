import plotly
import plotly.plotly as py
from plotly.graph_objs import *
from secret import *


def plot_location(lat_list, lng_list, text_list, title):
    data = Data([
        Scattermapbox(
            lat=lat_list,
            lon=lng_list,
            mode='markers',
            marker=Marker(
                size=9
            ),
            text=text_list,
        )
    ])
    min_lat = 10000
    max_lat = -10000
    min_lon = 10000
    max_lon = -10000
    for str_v in lat_list:
        v = float(str_v)
        if v < min_lat:
            min_lat = v
        if v > max_lat:
            max_lat = v
    for str_v in lng_list:
        v = float(str_v)
        if v < min_lon:
            min_lon = v
        if v > max_lon:
            max_lon = v
    center_lat = (max_lat + min_lat) / 2
    center_lon = (max_lon + min_lon) / 2
    layout = Layout(
        title=title,
        autosize=True,
        hovermode='closest',
        mapbox=dict(
            accesstoken=mapbox_access_token,
            bearing=0,
            center=dict(
                lat=center_lat,
                lon=center_lon
            ),
            pitch=0,
            zoom=10
        ),
    )
    fig = dict(data=data, layout=layout)
    # plotly.offline.plot(fig, filename=title)
    py.plot(fig, filename=title)

def plot_rate(rate, title):
    values = list(rate.values())
    dic = {}
    for ii in values:
        if str(ii) not in dic:
            dic[str(ii)] = 1
        else:
            dic[str(ii)] += 1
    data = [Bar(
        x=list(dic.keys()),
        y=list(dic.values())
    )]
    py.plot(data, filename=title)

def plot_price(price, title):
    temp = list(price.values())
    dic = {}
    for ii in temp:
        if str(float(ii)) not in dic:
            dic[str(float(ii))] = 1
        else:
            dic[str(float(ii))] += 1
    labels = list(dic.keys())
    values = list(dic.values())
    trace = Pie(labels=labels, values=values)
    py.plot([trace], filename=title)