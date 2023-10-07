import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
import numpy as np

def plot_median_resale_price(df, prediction_year):
    # plot median resale price of all towns by year
    towns = df['town'].unique()
    # add a new figure with titled window
    plt.figure()
    for town in towns:
        sub_set = df[df['town'] == town]
        sub_set = sub_set.groupby('year')['resale_price'].median()
        plt.plot(sub_set.index, sub_set.values, label=town)

    plt.xlabel('Year')
    plt.ylabel('Median Resale Price')
    plt.title('Median Resale Price of All Towns by Year')
    plt.legend()


    # plot median resale price of whole of Singapore by year
    plt.figure()
    sub_set = df.groupby('year')['resale_price'].median()
    if prediction_year != "None":
        x = np.array(sub_set.index).reshape(-1, 1)
        prediction_year = int(prediction_year)
        # last value in x is the last year in the dataset
        last_year = x[-1][0]
        #create a new array with values from last year to last year+prediction year
        y = np.array(sub_set.values).reshape(-1, 1)
        poly = PolynomialFeatures(degree=2)
        x_poly = poly.fit_transform(x)
        poly_reg_model = LinearRegression()
        poly_reg_model.fit(x_poly, y)
        # y_predicted = poly_reg_model.predict(x_poly)
        # plt.plot(x, y_predicted, color='red', label='Predicted Price')
        new_x = np.arange(x[0][0], last_year+prediction_year).reshape(-1, 1)
        # get predicted values for the new_x
        new_x_poly = poly.fit_transform(new_x)
        new_y = poly_reg_model.predict(new_x_poly)
        # plot the predicted values
        plt.plot(new_x, new_y, color='blue', label='Predicted Price', linestyle='dashed')

    plt.plot(sub_set.index, sub_set.values, label='Singapore')
    plt.xlabel('Year')
    plt.ylabel('Median Resale Price')
    plt.title('Median Resale Price of Whole of Singapore by Year')
    plt.grid()
    plt.legend()
    plt.show()

def plot_number_of_resale_flats_sold(df, prediction_year):
    # Total number of resale flats sold by each town throughout the years
    towns = df['town'].unique()
    plt.figure()
    for town in towns:
        sub_set = df[df['town'] == town]
        sub_set = sub_set.groupby('year')['resale_price'].count()
        plt.plot(sub_set.index, sub_set.values, label=town)

    plt.xlabel('Year')
    plt.ylabel('Number of Resale Flats Sold')
    plt.title('Number of Resale Flats Sold by Each Town Throughout the Years')
    plt.legend()


    # Total number of resale flats sold in whole of Singapore throughout the years
    plt.figure()
    sub_set = df.groupby('year')['resale_price'].count()
    if prediction_year != "None":
        x = np.array(sub_set.index).reshape(-1, 1)
        prediction_year = int(prediction_year)
        # last value in x is the last year in the dataset
        last_year = x[-1][0]
        #create a new array with values from last year to last year+prediction year
        y = np.array(sub_set.values).reshape(-1, 1)
        poly = PolynomialFeatures(degree=2)
        x_poly = poly.fit_transform(x)
        poly_reg_model = LinearRegression()
        poly_reg_model.fit(x_poly, y)
        # y_predicted = poly_reg_model.predict(x_poly)
        # plt.plot(x, y_predicted, color='red', label='Predicted Price')
        new_x = np.arange(x[0][0], last_year+prediction_year).reshape(-1, 1)
        # get predicted values for the new_x
        new_x_poly = poly.fit_transform(new_x)
        new_y = poly_reg_model.predict(new_x_poly)
        # plot the predicted values
        plt.plot(new_x, new_y, color='blue', label='Predicted Price', linestyle='dashed')
    plt.plot(sub_set.index, sub_set.values, label='Singapore')
    plt.xlabel('Year')
    plt.ylabel('Number of Resale Flats Sold')
    plt.title('Number of Resale Flats Sold in Whole of Singapore Throughout the Years')
    plt.grid()
    plt.legend()
    plt.show()  


def plot_top_five(df, reverse=False):
    # Top 5 towns with most expensive resale value
    plt.figure()
    sub_set = df.groupby('town')['resale_price'].median()
    sub_set = sub_set.sort_values(ascending=reverse)
    sub_set = sub_set[:5]
    plt.bar(sub_set.index, sub_set.values)
    plt.xlabel('Town')
    plt.ylabel('Median Resale Price')
    title = 'Top 5 Towns with {} Resale Value'.format('Most Expensive' if reverse == False else 'Cheapest')
    plt.title(title)
    plt.show()  


