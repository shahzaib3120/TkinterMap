import customtkinter
from tkintermapview import TkinterMapView
import json
import pandas as pd
import matplotlib.pyplot as plt
# polynomial regression
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from PIL import Image, ImageTk

from plots import plot_median_resale_price, plot_number_of_resale_flats_sold, plot_top_five

map_center = (1.352083, 103.809707)
default_zoom = 11

def swap_coordinates(cords):
    for i in range(len(cords)):
        cords[i] = (cords[i][1], cords[i][0])
    return cords

# read towns.json file
with open('towns.json', 'r') as json_file:
    towns_list = json.load(json_file)

# read average_price.json file
with open('average_price.json', 'r') as json_file:
    average_price_list = json.load(json_file)


df = pd.read_csv('data_modified.csv')

customtkinter.set_default_color_theme("blue")


class App(customtkinter.CTk):

    APP_NAME = "Singapore Data Analysis"
    WIDTH = 1000
    HEIGHT = 600

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title(App.APP_NAME)
        self.geometry(str(App.WIDTH) + "x" + str(App.HEIGHT))
        self.minsize(App.WIDTH, App.HEIGHT)

        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.bind("<Command-q>", self.on_closing)
        self.bind("<Command-w>", self.on_closing)
        self.createcommand('tk::mac::Quit', self.on_closing)

        self.marker_list = []

        # ============ create three CTkFrames ============

        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=0)
        self.grid_rowconfigure(0, weight=1)

        self.frame_left = customtkinter.CTkFrame(master=self, width=150, corner_radius=0, fg_color=None)
        self.frame_left.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")

        self.frame_center = customtkinter.CTkFrame(master=self, corner_radius=0)
        self.frame_center.grid(row=0, column=1, rowspan=1, pady=0, padx=0, sticky="nsew")

        self.frame_right = customtkinter.CTkFrame(master=self, width=150, corner_radius=0, fg_color=None)
        self.frame_right.grid(row=0, column=2, padx=0, pady=0, sticky="nsew")


        # ============ frame_left ============

        self.frame_left.grid_rowconfigure(4, weight=1)

        self.button_1 = customtkinter.CTkButton(master=self.frame_left,
                                                text="Resale Prices",
                                                command=self.plot_price_event)
        self.button_1.grid(pady=(20, 0), padx=(20, 20), row=0, column=0)

        self.button_2 = customtkinter.CTkButton(master=self.frame_left,
                                                text="No. of Resales",
                                                command=self.plot_resale_event)
        self.button_2.grid(pady=(20, 0), padx=(20, 20), row=1, column=0)


        self.button_3 = customtkinter.CTkButton(master=self.frame_left,
                                                text="Top 5",
                                                command=self.plot_top_five_event)
        self.button_3.grid(pady=(20, 0), padx=(20, 20), row=2, column=0)

        self.button_4 = customtkinter.CTkButton(master=self.frame_left,
                                                text="Bottom 5",
                                                command=self.plot_bottom_five_event)
        self.button_4.grid(pady=(20, 0), padx=(20, 20), row=3, column=0)

        self.prediction_label = customtkinter.CTkLabel(self.frame_left, text="Prediction:", anchor="w")
        self.prediction_label.grid(row=5, column=0, padx=(20, 20), pady=(20, 0))
        self.prediction_menu = customtkinter.CTkOptionMenu(self.frame_left, values=["None", "1", "2", "3", "4", "5"],
                                                                       command=self.change_prediction_year)
        self.prediction_menu.grid(row=6, column=0, padx=(20, 20), pady=(10, 0))

        self.flat_label = customtkinter.CTkLabel(self.frame_left, text="Flat Type:", anchor="w")
        self.flat_label.grid(row=7, column=0, padx=(20, 20), pady=(20, 0))
        self.flat_type_menu = customtkinter.CTkOptionMenu(self.frame_left, values=["All", "1 ROOM", "2 ROOM", "3 ROOM", "4 ROOM", "5 ROOM", "EXECUTIVE", "MULTI-GENERATION"],
                                                                       command=self.change_flat_type)
        self.flat_type_menu.grid(row=8, column=0, padx=(20, 20), pady=(10, 0))


        self.map_label = customtkinter.CTkLabel(self.frame_left, text="Tile Server:", anchor="w")
        self.map_label.grid(row=9, column=0, padx=(20, 20), pady=(20, 0))
        self.map_option_menu = customtkinter.CTkOptionMenu(self.frame_left, values=["OpenStreetMap", "Google normal", "Google satellite", "Blank"],
                                                                       command=self.change_map)
        self.map_option_menu.grid(row=10, column=0, padx=(20, 20), pady=(10, 0))

        self.appearance_mode_label = customtkinter.CTkLabel(self.frame_left, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=11, column=0, padx=(20, 20), pady=(20, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.frame_left, values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode)
        self.appearance_mode_optionemenu.grid(row=12, column=0, padx=(20, 20), pady=(10, 20))

        # ============ frame_center ============

        self.frame_center.grid_rowconfigure(1, weight=1)
        self.frame_center.grid_rowconfigure(0, weight=0)
        self.frame_center.grid_columnconfigure(0, weight=1)
        self.frame_center.grid_columnconfigure(1, weight=0)
        self.frame_center.grid_columnconfigure(2, weight=1)

        self.flat_type = "All"
        self.prediction_year = "None"

        def plot(polygon):
            sub_set = df[df['town'] == polygon.name]
            if self.flat_type != "All":
                sub_set = sub_set[sub_set['flat_type'] == self.flat_type]
            sub_set = sub_set.groupby('year')['resale_price'].median()
            plt.figure()
            if self.prediction_year != "None":
                x = np.array(sub_set.index).reshape(-1, 1)
                prediction_year = int(self.prediction_year)
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
            plt.grid()
            plt.plot(sub_set.index, sub_set.values, label=polygon.name)
            plt.xlabel('Year')
            plt.ylabel('Median Resale Price')
            plt.title('Median Resale Price of {1} flats in {0} by Year'.format(polygon.name, self.flat_type))
            plt.show()


        self.map_widget = TkinterMapView(self.frame_center, corner_radius=0)
        self.map_widget.grid(row=1, rowspan=1, column=0, columnspan=3, sticky="nswe", padx=(0, 0), pady=(0, 0))
        self.map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)
        self.map_widget.set_position(map_center[0], map_center[1])
        self.map_widget.set_zoom(default_zoom)

        # load "Blank.webp" image using PIL
        img = Image.open("Blank.webp")
        #resize the image
        img = img.resize((1, 1), Image.Resampling.LANCZOS)
        img_tk = ImageTk.PhotoImage(img)


        for town in average_price_list:
            if town['name'] == "Singapore" or town['coordinates'] == None:
                continue
            cords = swap_coordinates(town['coordinates'])
            # if resale price is greater than average price, fill the polygon with red color
            # if town['average_price'] > average_price_list[-1]['average_price']:
            if town["rank"] < 0.2*len(towns_list):
                color= "red"
            elif town["rank"] < 0.5*len(towns_list):
                color = "yellow"
            else:
                color = "green"
            self.map_widget.set_polygon(cords,
                                    fill_color=color,
                                    outline_color="grey",
                                    border_width=1,
                                    command=plot,
                                    name=town['name'])
            # get mean value of cords
            mean_lat = sum([cord[0] for cord in cords])/len(cords)
            mean_lon = sum([cord[1] for cord in cords])/len(cords)

            self.map_widget.set_marker(float(town['lat']), float(town['lon']), text_color="black", text=town['name'], icon=img_tk, font=("Helvetica", 5))
            # self.map_widget.set_marker(float(mean_lat), float(mean_lon), text_color="black", text=town['name'], icon=img_tk, font=("Helvetica", 5))

        self.title_label = customtkinter.CTkLabel(master=self.frame_center,
                                                        text="Singapore Real Estate Data Analysis",
                                                        anchor="center",
                                                        font=("Helvetica", 20)
                                                        )
        self.title_label.grid(row=0, column=1, sticky="w", padx=(12, 0), pady=12)

        # Set default values
        self.map_option_menu.set("Google normal")
        self.appearance_mode_optionemenu.set("Dark")


        # ============ frame_right ============
        self.frame_right.grid_rowconfigure(0, weight=0)
        self.frame_right.grid_rowconfigure(1, weight=1)
        self.frame_right.grid_rowconfigure(2, weight=1)
        self.frame_right.grid_columnconfigure(0, weight=0)
        # add padding to the right of the frame
        self.frame_right.grid_columnconfigure(1, weight=1)

        self.frame_right_label = customtkinter.CTkLabel(master=self.frame_right,
                                                        text="Resale Price Map",
                                                        anchor="center")
        self.frame_right_label.grid(row=0, column=0, padx=(20, 20), pady=(20, 0))

        # create a legend for the map
        self.legend = customtkinter.CTkFrame(master=self.frame_right, corner_radius=0, fg_color=None)
        self.legend.grid(row=1, column=0, padx=(20, 20), pady=(20, 0), sticky="nsew")
        self.legend.grid_columnconfigure(0, weight=1)
        self.legend.grid_columnconfigure(1, weight=1)

        self.legend.grid_rowconfigure(0, weight=0)
        self.legend.grid_rowconfigure(1, weight=0)
        self.legend.grid_rowconfigure(2, weight=0)
        
        
        self.legend_label_1 = customtkinter.CTkLabel(master=self.legend, text="Top 20%")
        self.legend_label_1.grid(row=0, column=0, padx=(0, 0), pady=(0, 0), sticky="nsew")

        # create a red square using create_rectangle method
        self.green_block = customtkinter.CTkFrame(master=self.legend, corner_radius=0, fg_color="red", height=20, width=20)
        self.green_block.grid(row=0, column=1, padx=(0, 0), pady=(5, 5), sticky="nsew")

        self.legend_label_2 = customtkinter.CTkLabel(master=self.legend, text="20% - 50%")
        self.legend_label_2.grid(row=1, column=0, padx=(0, 0), pady=(0, 0), sticky="nsew")

        self.red_block = customtkinter.CTkFrame(master=self.legend, corner_radius=0, fg_color="yellow", height=20, width=20)
        self.red_block.grid(row=1, column=1, padx=(0, 0), pady=(5, 5), sticky="nsew")

        self.legend_label_3 = customtkinter.CTkLabel(master=self.legend, text="Bottom 50%")
        self.legend_label_3.grid(row=2, column=0, padx=(0, 0), pady=(0, 0), sticky="nsew")

        self.red_block = customtkinter.CTkFrame(master=self.legend, corner_radius=0, fg_color="green", height=20, width=20)
        self.red_block.grid(row=2, column=1, padx=(0, 0), pady=(5, 5), sticky="nsew")
        

    def search_event(self, event=None):
        self.map_widget.set_address(self.entry.get())

    def plot_price_event(self):
        plot_median_resale_price(df, self.prediction_year)
    
    def plot_resale_event(self):
        plot_number_of_resale_flats_sold(df, self.prediction_year)

    def plot_top_five_event(self):
        plot_top_five(df, reverse=False)
    
    def plot_bottom_five_event(self):
        plot_top_five(df, reverse=True)

    def change_prediction_year(self, new_prediction_year: str):
        self.prediction_year = new_prediction_year

    def change_appearance_mode(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_map(self, new_map: str):
        if new_map == "OpenStreetMap":
            self.map_widget.set_tile_server("https://a.tile.openstreetmap.org/{z}/{x}/{y}.png")
        elif new_map == "Google normal":
            self.map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)
        elif new_map == "Google satellite":
            self.map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=s&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)
        elif new_map == "Blank":
            self.map_widget.set_tile_server("https://wmts.geo.admin.ch/1.0.0/ch.swisstopo.pixelkarte-farbe/default/current/3857/{z}/{x}/{y}.jpeg")

    def change_flat_type(self, new_flat_type: str):
        self.flat_type = new_flat_type

    def on_closing(self, event=0):
        self.destroy()

    def start(self):
        self.mainloop()


if __name__ == "__main__":
    app = App()
    app.start()
