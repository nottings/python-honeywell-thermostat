python-honeywell-thermostat
===========================

Data collector for internet connected Honeywell Thermostats

- **honeywell**_db.py Adds data collected from Total Connect Comfort site to a local 
MySQL database 

- **honeywell_plot.py** Simple PyPlot of temperature data from database

Be sure to review the code before running. You will need to enter in some user 
and device information.

- **highstock** is javascript code from http://www.highcharts.com/products/highstock 
with modifications to support pulling data from the database populated by 
honeywell_db.py  I'm not sure about the legality of posting the highstock code 
within this repo, so you'll need to download a copy on your own and combine it 
with the customizations of this repo.

This is an initial commit with basic working functionality. Still **LOTS** to do
especially with code cleanup.


[[highstock.png]]
[[pyplot.png]]
