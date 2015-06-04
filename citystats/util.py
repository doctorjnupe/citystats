#!/usr/bin/env python

from requests.exceptions import HTTPError
import time

def get_device(client, city):
    """Return an M2X device

    Gets the device for the given city if it exists,
    if not creates the device.
    """
    print("geting device for city: " + city)

    devicename = "City Stats - " + city

    # Get device if it exists, otherwise create device
    try:
        device = client.devices(q = city)[0]
    except IndexError:
        time.sleep(5)
        device = client.create_device(name = devicename,
                                      description = "A collection of stats related to " + city,
                                      visibility = "private")

    return device

def get_stream(device, stream_name, params):
    """Return an M2X stream
    
    Gets the stream for the given device / stream_name if it exists,
    if not creates the device.
    """
    try:
        stream = device.stream(stream_name)
    except HTTPError:
        time.sleep(5)
        stream = device.create_stream(stream_name)
        time.sleep(5)
        device.update_stream(stream_name, unit=params)

    return stream
