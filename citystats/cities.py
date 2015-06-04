#coding: utf-8
#!/usr/bin/env python

import json
import time
import os.path
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut

class Cities:

    def __init__(self):
        self.cities = Cities.load_cities()

    @staticmethod
    def load_cities():
        """
        Return cities and their respective latitude & longitude coordinates
        as JSON object.

        If /data/cities.json backup file does not exist coordinates for
        cities in /data/cities.txt are looked up using geopy lib.

        Otherwise, if /data/cities.json backup file exists, data from
        /data/cities.json is returned.

        """
        cities_list = open("data/cities.txt").read().split("\n")
        cities_json_file_exists = os.path.isfile("data/cities.json") 
        
        if(not(cities_json_file_exists)):
            print("Downloading city coords...")
            coords_dict = { "lat": "", "lng": "" }
            cities_dict = { x: coords_dict for x in cities_list }
            cities_json = json.loads(json.dumps(cities_dict))
            for city in cities_list:
                attempts = 0
                success = False
                coords = Cities.get_coords(city)
                if(len(coords) < 2):
                    # if coords not found, delete city
                    del cities_json[city]
                else:
                    # else add coords to city
                    latitude = coords[0]
                    longitude = coords[1]
                    cities_json[city]["lat"] = latitude
                    cities_json[city]["lng"] = longitude
            cities_json_file = open("data/cities.json", "w")
            json.dump(cities_json, cities_json_file)
        else:
            print("Getting cities from file...")
            cities_json_file = open("data/cities.json", "r")
            cities_json = json.loads(cities_json_file.read())
        
        cities_json_file.close()
        return cities_json

    @staticmethod
    def get_coords(city):
        """
        Looks up the given city's latitude and longitude coordinates using geopy.
        
        Returns a comma separated string of the cities coordinates: 'latitude,longitude'
        """
        geolocator = Nominatim()
        coords = []
        attempts = 0
        success = False
        
        while(not(success) and attempts < 10):
            try:
                location = geolocator.geocode(city)
                attempts += 1
                time.sleep(3)
                coords = [location.latitude, location.longitude]
                success = True
            except GeocoderTimedOut as e:
                if attempts == 5: print("Failed on final attempt for " + city)

        return coords
