#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import forecastio
import json
import cgitb

cgitb.enable()
print 'Content-Type: text/plain;charset=utf-8'
print

# Get your free API key from http://developer.forecast.io
api_key = ""

# Set your latitude and longitude for desired temperature forecast here
lat = 41.943036
lng = -87.683696

forecast = forecastio.load_forecast(api_key, lat, lng)

# TODO: adjust math to use GMT offset from forecast data instead of hard-coded "5"
data = json.dumps([[(int(x['time']) * 1000) - (3600000*5), x['temperature']] for x in forecast.__dict__['json']['hourly']['data']])

print data
