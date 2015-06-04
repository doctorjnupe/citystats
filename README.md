# Citystats

![citystats-logo](http://cl.ly/image/1q351H2I0F3B/citystats.png)

## Introduction

This application runs on [Heroku](https://www.heroku.com/), collects data pertaining to various cities and reports the data to [AT&T's M2X](https://m2x.att.com/) time-series data service.

Check out the data which I've made publicly available via my account on M2X @ [M2X Public Device Catalog](https://m2x.att.com/catalog?q=City+Stats)

## Pre-Requisites

### You will need to have an account on the following services:

1. [M2X](https://m2x.att.com/signup): M2X is an IoT time-series data storage service. The M2X developer tier account is free for up to 10 devices @ 100,000 max data points written per device/month.  This application creates one M2X device per city listed in [/data/cities.txt](/data/cities.txt), as long as there are 10 or fewer cities listed in that file you will be able to utilize this application with a developer tier account. The current build of the application pushes less than 10,000 datapoints per device, well under the developer tier limit. Should you desire more capacity you'll need to [upgrade your M2X Account](https://m2x.att.com/pricing).
2. [Heroku](https://www.heroku.com/): Heroku is a PaaS that enables developers to build and run applications entirely in the cloud. Because this example application uses only one Heroku dyno, it should be free for you to use, no matter how many other Heroku applications you have.
3. [Forecast.io](https://developer.forecast.io/): Forecast.io is a global weather service with an open API for accessing weather data. The Forecast.io developer account is free and allows for up to 1000 API calls per month. This application utilizes Forecast.io to retrieve weather data for the cities listed in [/data/cities.txt](/data/cities.txt).

### API Keys
Obtain your Forecast.io API Key from their [developer portal](https://developer.forecast.io/)

## Installation

### Deploying your application

Click the Heroku button to deploy your application to Heroku:

[![Deploy](https://www.herokucdn.com/deploy/button.png)](https://heroku.com/deploy)

### Setup Config Variables in Heroku

#### Via Heroku CLI
(requires [Heroku Toolbelt](https://toolbelt.heroku.com/))

Forecast.io API Key:
```
heroku config:set FORECAST_API_KEY={YOUR-FORECAST.IO-API-KEY}
```

#### Via Heroku Dashboard

You can also [edit config vars](https://devcenter.heroku.com/articles/config-vars#setting-up-config-vars-for-a-deployed-application) on your app’s settings tab on your Heroku Dashboard.

### Adjust `/data/cities.txt` (optional)

Adjust the list of cities in [`/data/cities.txt`](/data/cities.txt) if desired. This is a newline separated list of Cities that will be tracked by this app. Forecast data from Forecast.io is retrieved for the cities listed in `/data/cities.txt`.

### Scaling Your Application

Scale the number of clock workers to 1, once this is done the `clock.py` script will start and is set up to run every 2 days.  *Why 2 days?* Hourly forecast data from Forecast.io returns data for the past 48 hours, so the script is set up to run every 2 days.

#### Via Heroku CLI

```
heroku ps:scale clock=1
```

#### Via Heroku Dashboard

Go to the Resources tab on your application's dashboard on Heroku and scale the `python clock.py` process so that it uses one dyno.

## Issues

Feel free to report any issues you encounter with this app via GitHub

## Thanks to...
* [M2X](https://m2x.att.com): time-series data store
* [Heroku](https://www.heroku.com): cloud application hosting
* [ZeevG/python-forecast.io](https://github.com/ZeevG/python-forecast.io): python wrapper library for interacting with Forecast.io
* [geopy](https://github.com/geopy/geopy): geolocation library for python

## LICENSE

This sample application is released under the MIT license. See [`LICENSE`](LICENSE) for the terms.
