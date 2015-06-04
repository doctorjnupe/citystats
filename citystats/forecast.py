#coding: utf-8
#!/usr/bin/env python

import os
import time
import forecastio
import util
from m2x.utils import to_iso
from datetime import datetime

FORECAST_API_KEY = os.environ['FORECAST_API_KEY']
STREAMS = { "Temperature": { "label": "degree", "symbol": "°" },
            "Humidity": { "label": "percentage", "symbol": "%" },
            "Pressure": { "label": "millibar", "symbol": "mbar" },
            "Ozone": { "label": "dobson unit" },
            "Precipitation": { "label": "in/hr" } 
          }

def post_forecast(client, cities):
    """
    Posts the hourly forecast values for the given set of cities.

    The hourly forecast from Forecast.io includes the hourly forecast stats
    for the past 48-hours.
    """
    print("post_forecast")
    for city in cities:
        hourly_forecast = forecastio.load_forecast(FORECAST_API_KEY, cities[city]["lat"], cities[city]["lng"]).hourly()
        post_stream_updates(client, city, hourly_forecast)    

def post_stream_updates(client, city, hourly_forecast):
    """
    Posts hourly forecast updates to the given cities streams.
    """
    print("posting stream_updates...")
    try:
        device = util.get_device(client, city)
        
        timestamps = get_timestamps(hourly_forecast)
        temperature_values = get_temperature_values(hourly_forecast, timestamps)
        humidity_values = get_humidity_values(hourly_forecast, timestamps)
        pressure_values = get_pressure_values(hourly_forecast, timestamps)
        ozone_values = get_ozone_values(hourly_forecast, timestamps)
        precip_values = get_precip_values(hourly_forecast, timestamps)

        for stream_name in STREAMS:
            stream = util.get_stream(device, stream_name, STREAMS[stream_name])

            time.sleep(5)
            try:
                if stream_name == "Temperature":
                    print("posting temperature values:")
                    print(temperature_values)
                    stream.post_values(temperature_values)
                elif stream_name == "Humidity":
                    print("posting humidity values:")
                    print(humidity_values)
                    stream.post_values(humidity_values)
                elif stream_name == "Pressure":
                    print("posting pressure values:")
                    print(pressure_values)
                    stream.post_values(pressure_values)
                elif stream_name == "Ozone":
                    print("posting ozone values:")
                    print(ozone_values)
                    stream.post_values(ozone_values)
                elif stream_name == "Precipitation":
                    print("posting precipitation values:")
                    print(precip_values)
                    stream.post_values(precip_values)
            except Exception as e:
                print("Exception occurred while posting " + stream_name + " values to " + city + ":\n" + str(e))
    except Exception as e:
        print("Exception occurred while getting device for " + city + ":\n" + str(e))

def get_temperature_values(hourly_forecast, timestamps):
    """
    Returns the hourly forecast temperature values as a JSON object formatted for M2X.
    """
    temperature_values = []
    for datum in hourly_forecast.data:
        try:
            temperature_values.append(datum.temperature)
        except:
            print "Error with hourly_forecast temperature.  Appending 0"
            temperature_values.append(0)

    values = []
    for index in range(len(timestamps)):
        values.append({ "timestamp": timestamps[index], "value": str(temperature_values[index]) })

    return values

def get_humidity_values(hourly_forecast, timestamps):
    """
    Returns the hourly forecast humidity values as a JSON object formatted for M2X.
    """
    humidity_values = []
    for datum in hourly_forecast.data:
        try:
            humidity_values.append(datum.humidity)
        except:
            print "Error with hourly_forecast humidity.  Appending 0"
            humidity_values.append(0)

    values = []
    for index in range(len(timestamps)):
        values.append({ "timestamp": timestamps[index], "value": str(humidity_values[index]) })

    return values

def get_pressure_values(hourly_forecast, timestamps):
    """
    Returns the hourly forecast pressure values as a JSON object formatted for M2X.
    """
    pressure_values = []
    for datum in hourly_forecast.data:
        try:
            pressure_values.append(datum.pressure)
        except:
            print "Error with hourly_forecast pressure.  Appending 0"
            pressure_values.append(0)

    values = []
    for index in range(len(timestamps)):
        values.append({ "timestamp": timestamps[index], "value": str(pressure_values[index]) })

    return values

def get_ozone_values(hourly_forecast, timestamps):
    """
    Returns the hourly forecast ozone values as a JSON object formatted for M2X.
    """
    ozone_values = []
    for datum in hourly_forecast.data:
        try:
            ozone_values.append(datum.ozone)
        except:
            print "Error with hourly_forecast ozone.  Appending 0"
            ozone_values.append(0)

    values = []
    for index in range(len(timestamps)):
        values.append({ "timestamp": timestamps[index], "value": str(ozone_values[index]) })

    return values

def get_precip_values(hourly_forecast, timestamps):
    """
    Returns the hourly forecast precipitation values as a JSON object formatted for M2X.
    """
    precip_values = []
    for datum in hourly_forecast.data:
        try:
            precip_values.append(datum.precipIntensity)
        except:
            print "Error with hourly_forecast precipIntensity.  Appending 0"
            precip_values.append(0)

    values = []
    for index in range(len(timestamps)):
        values.append({ "timestamp": timestamps[index], "value": str(precip_values[index]) })

    return values

def get_timestamps(hourly_forecast):
    """
    Returns the timestamps for each hourly forecast as an array of ISO formatted 
    datetime strings.
    """
    timestamps = []
    for datum in hourly_forecast.data:
        try:
            timestamps.append(to_iso(datum.time))
        except:
            print "Error with hourly_forecast timestamp"

    return timestamps
