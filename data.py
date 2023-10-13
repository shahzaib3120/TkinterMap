import pandas as pd
import numpy as np
import json
import requests

def get_cords(query):
    words = query.replace("/"," ")
    words = words.split()
    query = "+".join(words)
    print("fetching data for: ", query)
    url = "https://nominatim.openstreetmap.org/search.php?q={}&polygon_geojson=1&format=json".format(query+"+singapore")
    response = requests.get(url)
    data = response.json()
    return_dict = {}
    return_dict['coordinates'] = []
    return_dict['lat'] = None
    return_dict['lon'] = None
    if len(data) == 0:
        return return_dict
    else:
        for i in data:
            if i['class'] == 'place' and i['geojson']['type'] == 'Polygon':
                return_dict['coordinates'] = i['geojson']['coordinates'][0]
                return_dict['lat'] = i['lat']
                return_dict['lon'] = i['lon']
                return return_dict
    
# open data.csv file and read it into a pandas dataframe
df = pd.read_csv('data_modified.csv')
# get unique values of the column 'town'
towns = df['town'].unique()

towns_list = []
id = 0
for town in towns:
    town_dict = {}
    town_dict['id'] = id
    town_dict['name'] = town
    cords = get_cords(town_dict['name'].split('/')[0])
    if cords is not None:
        town_dict['coordinates'] = cords['coordinates']
        town_dict['lat'] = cords['lat']
        town_dict['lon'] = cords['lon']
    towns_list.append(town_dict)
    id += 1
    
# create a json file
with open('towns.json', 'w') as json_file:
    json.dump(towns_list, json_file, indent=4)

print("done!!")