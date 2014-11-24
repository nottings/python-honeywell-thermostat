#!/usr/bin/env python

from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import json
import urllib
import datetime
import time
import re
import time
import httplib
import requests


# Login information for Total Connect Comfort web site
USERNAME="your Total Connect Comfort login id"
PASSWORD="your total connect comfort password"
DEVICE_ID=""#device id can be obtained by viewing source after logging in to total connect comfort page
# it should also be the last part of the URI when visiting the remote control of your thermostat online

# local database username and password
DB_USER = ''
DB_PASS = ''

# First, you'll have to make sure you have created a MySQL database called 'thermostat'
# create database thermostat;
# grant all on thermostat.* to 'DB_USER'@'localhost' identified by 'DB_PASS';
# flush privileges
# Then,
engine = create_engine('mysql://%s:%s@localhost:3306/thermostat' % (DB_USER, DB_PASS))
Base = declarative_base()

class Data(Base):
    __tablename__ = 'data'

    id = Column(Integer, primary_key=True)
    Date = Column(DateTime())
    CoolLowerSetptLimit = Column(Float())
    CoolNextPeriod = Column(Float())
    CoolSetpoint = Column(Float())
    CoolUpperSetptLimit = Column(Float())
    DeviceID = Column(Integer())
    DispTemperature = Column(Float())
    DisplayedUnits = Column(String(1))
    HeatLowerSetptLimit = Column(Float())
    HeatNextPeriod = Column(Integer())
    HeatSetpoint = Column(Float())
    HeatUpperSetptLimit = Column(Float())
    IsInVacationHoldMode = Column(Boolean())
    SchedCoolSp = Column(Float())
    SchedHeatSp = Column(Float())
    ScheduleCapable = Column(Boolean())
    #StatSenseDispTemp = Column(Float())
    StatusCool = Column(Integer())
    StatusHeat = Column(Integer())
    SystemSwitchPosition = Column(Integer())
    #TemporaryHoldUntilTime = Column(Integer())
    Humidity = Column(Integer())
    Phrase = Column(String(32))
    Temperature = Column(Integer())


    def __init__(self, data):
        self.Date = datetime.datetime.now()
        self.CoolLowerSetptLimit = float(data['latestData']['uiData']['coolLowerSetpLimit'])
        self.CoolNextPeriod = float(data['latestData']['uiData']['coolNextPeriod'])
        self.CoolSetpoint = float(data['latestData']['uiData']['coolSetpoint'])
        self.CoolUpperSetptLimit = float(data['latestData']['uiData']['coolUpperSetptLimit'])
        self.DeviceID = int(data['latestData']['uiData']['deviceID'])
        self.DispTemperature = float(data['latestData']['uiData']['dispTemperature'])
        self.DisplayedUnits = data['latestData']['uiData']['displayedUnits']
        self.HeatLowerSetptLimit = float(data['latestData']['uiData']['heatLowerSetptLimit'])
        self.HeatNextPeriod = int(data['latestData']['uiData']['heatNextPeriod'])
        self.HeatSetpoint = float(data['latestData']['uiData']['heatSetpoint'])
        self.HeatUpperSetptLimit = float(data['latestData']['uiData']['heatUpperSetptLimit'])
        self.IsInVacationHoldMode = bool(data['latestData']['uiData']['isInVacationHoldMode'])
        self.SchedCoolSp = float(data['latestData']['uiData']['schedCoolSp'])
        self.SchedHeatSp = float(data['latestData']['uiData']['schedHeatSp'])
        self.ScheduleCapable = bool(data['latestData']['uiData']['scheduleCapable'])
        #self.StatSenseDispTemp = data['latestData']['uiData']['StatSenseDispTemp']
        self.StatusCool = int(data['latestData']['uiData']['statusCool'])
        self.StatusHeat = int(data['latestData']['uiData']['statusHeat'])
        self.SystemSwitchPosition = int(data['latestData']['uiData']['systemSwitchPosition'])
        #self.TemporaryHoldUntilTime = int(data['latestData']['uiData']['vacationHoldUntilTime'])
        self.Humidity = int(data['latestData']['uiData']['weatherHumidity'])
        self.Phrase = data['latestData']['uiData']['weatherPhrase']
        self.Temperature = int(data['latestData']['uiData']['weatherTemperature'])

#Uncomment this to drop all previous data stored in DB
# Erases all old data
#Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)
session = Session()


AUTH="https://rs.alarmnet.com/TotalConnectComfort/"

def get_data():

    retries=5
    auth={
        'timeOffset': 240,
        'UserName': USERNAME,
        'Password': PASSWORD,
        'RememberMe': 'false'
    }
    headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:31.0) Gecko/20100101 Firefox/31.0',
        'Host': 'rs.alarmnet.com',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Referer': 'https://rs.alarmnet.com/TotalConnectComfort'
    }
    headers2 = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:31.0) Gecko/20100101 Firefox/31.0',
        'Host': 'rs.alarmnet.com',
        'Referer': 'https://rs.alarmnet.com/TotalConnectComfort/Device/Control/'+DEVICE_ID,
        'X-Requested-With': 'XMLHttpRequest',
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.5'
    }
    s = requests.Session()
    t = datetime.datetime.now()
    utc_seconds = (time.mktime(t.timetuple()))
    utc_seconds = int(utc_seconds*1000)

    # Login
    r = s.post('https://mytotalconnectcomfort.com/portal/', params=auth, headers=headers)
    r.raise_for_status()
    data_regex = re.compile(r'Control\.Model\.set\(Control\.Model\.Property\.(.*),\ (.*)\);')
    matches = data_regex.findall(r.content.strip())
    data = {'latestData': {'uiData': {}}}
    for x in matches:
        data['latestData']['uiData'][x[0]] = x[1].strip("'")
    return data

d = Data(get_data())
session.add(d)
session.commit()
