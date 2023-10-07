import pandas as pd
import json

if __name__ == "__main__":
    # open data.csv file and read it into a pandas dataframe
    df = pd.read_csv('data.csv')
    total_average_price = df['resale_price'].mean()

    # read json file
    with open('towns.json', 'r') as json_file:
        towns_list = json.load(json_file)

    # get average price of each town
    towns = df['town'].unique()
    for town in towns_list:
        sub_set = df[df['town'] == town['name']]
        average_price = sub_set['resale_price'].mean()
        town['average_price'] = average_price

    # arrange the list in descending order
    towns_list.sort(key=lambda x: x['average_price'], reverse=True)

    # add rank to each town
    rank = 1
    for town in towns_list:
        town['rank'] = rank
        rank += 1
    towns_list.append({'name': 'Singapore', 'average_price': total_average_price})

    # create a json file
    with open('average_price.json', 'w') as json_file:
        json.dump(towns_list, json_file, indent=4)





