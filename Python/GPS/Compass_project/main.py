import os
import sys
import time
import requests
import xml.dom.minidom
import pandas as pd


# https://developer.translink.ca/
def get_api_token(token_path):
    f = open(token_path, 'r')
    api_token = f.read()
    f.close()
    return api_token


def load_compass_data(data_folder_path):
    transit_data = {}
    bus_stops_list = []
    sky_train_station_list = []

    for csv_sheet in os.listdir(data_folder_path):
        if "card" in csv_sheet.lower():
            year = csv_sheet.split(' to')[0].split('-')[-1]
            data = pd.read_csv(data_folder_path + os.sep + csv_sheet)
            df = pd.concat([data["DateTime"].iloc[::-1], data["Transaction"].iloc[::-1]], axis=1)

            transit_data[year] = {}
            for index, row in df.iterrows():
                month = row["DateTime"].split("-")[0]
                day = row["DateTime"].split("-")[1]
                time = row["DateTime"].split(year)[-1].strip()
                if month not in transit_data[year].keys():
                    transit_data[year][month] = {}
                if day not in transit_data[year][month].keys():
                    transit_data[year][month][day] = []
                if "Missing" not in row["Transaction"]:
                    transit_data[year][month][day].append((time, row["Transaction"]))

            for item in data["Transaction"].iloc[::-1].tolist():
                if "Missing" not in item and "Bus" not in item and item.split(" at ")[-1] not in sky_train_station_list:
                    if '#' not in item.split(" at ")[-1]:
                        sky_train_station_list.append(item.split(" at ")[-1])
                elif "Bus Stop" in item and item.split("Bus Stop ")[-1] not in bus_stops_list:
                    if len(item.split("Bus Stop ")[-1]) == 5:
                        bus_stops_list.append(item.split("Bus Stop ")[-1])

    bus_stops_list.sort()
    sky_train_station_list.sort()

    return transit_data, bus_stops_list, sky_train_station_list


def get_bus_info(api, bus_stops):
    stop_info = []
    url = r'https://api.translink.ca/rttiapi/v1/stops/[STOP]?apikey=[KEY]'
    url = url.replace("[KEY]", api)
    for stop in bus_stops:
        response = requests.get(url.replace("[STOP]", stop))
        response_text = response.text
        xml_pretty_str = xml.dom.minidom.parseString(response_text).toprettyxml()
        if "<Code>1001</Code>" not in xml_pretty_str:
            stop_no = xml_pretty_str[xml_pretty_str.find("StopNo>") + len("StopNo>"):xml_pretty_str.find("</StopNo")]
            name = xml_pretty_str[xml_pretty_str.find("Name>") + len("Name>"):xml_pretty_str.find("</Name")]
            city = xml_pretty_str[xml_pretty_str.find("City>") + len("City>"):xml_pretty_str.find("</City")]
            bay_no = xml_pretty_str[xml_pretty_str.find("BayNo>") + len("BayNo>"):xml_pretty_str.find("</BayNo")]
            on_street = xml_pretty_str[xml_pretty_str.find("OnStreet>") + len("OnStreet>"):xml_pretty_str.find("</OnStreet")]
            at_street = xml_pretty_str[xml_pretty_str.find("AtStreet>") + len("AtStreet>"):xml_pretty_str.find("</AtStreet")]
            latitude = xml_pretty_str[xml_pretty_str.find("Latitude>") + len("Latitude>"):xml_pretty_str.find("</Latitude")]
            longitude = xml_pretty_str[xml_pretty_str.find("Longitude>") + len("Longitude>"):xml_pretty_str.find("</Longitude")]
            routes = xml_pretty_str[xml_pretty_str.find("Routes>") + len("Routes>"):xml_pretty_str.find("</Routes")]
            if "xmlns" in routes:
                routes = ""
            else:
                routes = routes.replace(',', ';').replace(' ', '')
            stop_info.append([stop_no, name, city, bay_no, on_street, at_street, latitude, longitude, routes, url.replace("[STOP]", stop)])
            print("Complete Getting Stop Info for: ", stop_no)

    return stop_info


def write_bus_info(stop_info):
    header = "stop_no,name,city,bay_no,on_street,at_street,latitude,longitude,routes,api_url\n"
    f = open("bus_info.csv", "a+")
    f.truncate(0)
    f.write(header)
    f.flush()
    for item in stop_info:
        f.write(",".join(item) + '\n')
        f.flush()
    f.close()


if __name__ == "__main__":
    api_token = get_api_token(os.getcwd() + os.sep + "api.token")
    data, bus_stops, sky_stops = load_compass_data("E:\Files\Stuff\Compass")

    if not os.path.isfile(os.getcwd() + os.sep + "bus_info.csv"):
        stop_info = get_bus_info(api_token, bus_stops)
        write_bus_info(stop_info)
