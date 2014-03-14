#!/usr/bin/env python

from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import json
import urllib2
import urllib
import datetime
import re
import time
import math
import base64
import time
import httplib
import sys
import tty,termios
import getopt
import os
import stat

# Login information for Total Connect Comfort web site
USERNAME="your Total Connect Comfort login id"
PASSWORD="your total connect comfort password"
DEVICE_ID=#device id can be obtained by viewing source after logging in to total connect comfort page
# it should also be the last part of the URI when visiting the remote control of your thermostat online

# local database username and password
DB_USER = ''
DB_PASS = ''

# First, you'll have to make sure you have created a MySQL database called 'thermostat'
# create database thermostat;
# grant all on thermostat.* to 'DB_USER'@'localhost' identified by 'DB_PASS';
# flush privileges
# Then,
engine = create_engine('mysql://%s:%s@localhost:3306/thermostat' % (DB_USER, DB_PASS)
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
    StatSenseDispTemp = Column(Float())
    StatusCool = Column(Integer())
    StatusHeat = Column(Integer())
    SystemSwitchPosition = Column(Integer())
    TemporaryHoldUntilTime = Column(Integer())
    Humidity = Column(Integer())
    Phrase = Column(String(32))
    Temperature = Column(Integer())


    def __init__(self, data):
        self.Date = datetime.datetime.now()
        self.CoolLowerSetptLimit = data['latestData']['uiData']['CoolLowerSetptLimit']
        self.CoolNextPeriod = data['latestData']['uiData']['CoolNextPeriod']
        self.CoolSetpoint = data['latestData']['uiData']['CoolSetpoint']
        self.CoolUpperSetptLimit = data['latestData']['uiData']['CoolUpperSetptLimit']
        self.DeviceID = data['latestData']['uiData']['DeviceID']
        self.DispTemperature = data['latestData']['uiData']['DispTemperature']
        self.DisplayedUnits = data['latestData']['uiData']['DisplayedUnits']
        self.HeatLowerSetptLimit = data['latestData']['uiData']['HeatLowerSetptLimit']
        self.HeatNextPeriod = data['latestData']['uiData']['HeatNextPeriod']
        self.HeatSetpoint = data['latestData']['uiData']['HeatSetpoint']
        self.HeatUpperSetptLimit = data['latestData']['uiData']['HeatUpperSetptLimit']
        self.IsInVacationHoldMode = data['latestData']['uiData']['IsInVacationHoldMode']
        self.SchedCoolSp = data['latestData']['uiData']['SchedCoolSp']
        self.SchedHeatSp = data['latestData']['uiData']['SchedHeatSp']
        self.ScheduleCapable = data['latestData']['uiData']['ScheduleCapable']
        self.StatSenseDispTemp = data['latestData']['uiData']['StatSenseDispTemp']
        self.StatusCool = data['latestData']['uiData']['StatusCool']
        self.StatusHeat = data['latestData']['uiData']['StatusHeat']
        self.SystemSwitchPosition = data['latestData']['uiData']['SystemSwitchPosition']
        self.TemporaryHoldUntilTime = data['latestData']['uiData']['TemporaryHoldUntilTime']
        self.Humidity = data['latestData']['weather']['Humidity']
        self.Phrase = data['latestData']['weather']['Phrase']
        self.Temperature = data['latestData']['weather']['Temperature']

#Uncomment this to drop all previous data stored in DB
# Erases all old data
#Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)
session = Session()


AUTH="https://rs.alarmnet.com/TotalConnectComfort/"

def get_data():

    retries=5
    params=urllib.urlencode({"timeOffset":"240",
        "UserName":USERNAME,
        "Password":PASSWORD,
        "RememberMe":"false"})
    headers={"Content-Type":"application/x-www-form-urlencoded",
            "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Encoding":"sdch",
            "Host":"rs.alarmnet.com",
            "DNT":"1",
            "Origin":"https://rs.alarmnet.com/TotalComfort/",
            "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.95 Safari/537.36"
        }
    conn = httplib.HTTPSConnection("rs.alarmnet.com")
    conn.request("POST", "/TotalConnectComfort/",params,headers)
    r1 = conn.getresponse()
    cookie = r1.getheader("Set-Cookie")
    location = r1.getheader("Location")
    # Strip "expires" "httponly" and "path" from cookie
    newcookie=cookie
    #newcookie=re.sub("^expires=[^;]+;","",newcookie)
    #newcookie=re.sub("^expires=[^;]+$","",newcookie)
    newcookie=re.sub(";\s*expires=[^;]+","",newcookie)
    #newcookie=re.sub("^path=[^;]+;","",newcookie)
    #newcookie=re.sub(";\s*path=[^;]+;",";",newcookie)
    newcookie=re.sub(";\s*path=[^,]+,",";",newcookie)
    newcookie=re.sub("HttpOnly\s*[^;],","X;",newcookie)
    newcookie=re.sub(";\s*HttpOnly\s*,",";",newcookie)
    cookie=newcookie

    if ((location == None) or (r1.status != 302)):
        raise BaseException("Login fail" )

    # Skip second query - just go directly to our device_id, rather than letting it
    # redirect us to it.
    code=str(DEVICE_ID)
    t = datetime.datetime.now()
    utc_seconds = (time.mktime(t.timetuple()))
    utc_seconds = int(utc_seconds*1000)
    location="/TotalConnectComfort/Device/CheckDataSession/"+code+"?_="+str(utc_seconds)
    headers={
            "Accept":"*/*",
            "DNT":"1",
            #"Accept-Encoding":"gzip,deflate,sdch",
            "Accept-Encoding":"plain",
            "Cache-Control":"max-age=0",
            "Accept-Language":"en-US,en,q=0.8",
            "Connection":"keep-alive",
            "Host":"rs.alarmnet.com",
            "Referer":"https://rs.alarmnet.com/TotalConnectComfort/",
            "X-Requested-With":"XMLHttpRequest",
            "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.95 Safari/537.36",
            "Cookie":cookie
        }
    conn = httplib.HTTPSConnection("rs.alarmnet.com")
    #conn.set_debuglevel(999);
    conn.request("GET", location,None,headers)
    r3 = conn.getresponse()
    if (r3.status != 200):
            print "Bad R3 status ",r3.status, r3.reason
    #print r3.status, r3.reason
    rawdata=r3.read()
    j = json.loads(rawdata)
    #print json.dumps(j,sort_keys=True,indent=4, separators=(',', ': '))
    return j

d = Data(get_data())
session.add(d)
session.commit()
