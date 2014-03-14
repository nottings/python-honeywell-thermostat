#!/usr/bin/env python

from honeywell_db import Base, Data
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import matplotlib.pyplot as plt

engine = create_engine('mysql://%s:%s@localhost:3306/thermostat' % (DB_USER, DB_PASS))
Base.metadata.bind = engine
DBSession = sessionmaker()
DBSession.bind = engine
session = DBSession()
date = [ x.Date for x in session.query(Data).all() ]
indoorTemp = [ s.DispTemperature for s in session.query(Data).all() ]
heatSetPoint = [ s.HeatSetpoint for s in session.query(Data).all() ]
outdoorTemp = [ s.Temperature for s in session.query(Data).all() ]
onOff = [ s.StatusHeat for s in session.query(Data).all() ]

plt.plot(date,indoorTemp,'g.-',date,heatSetPoint,'r.-',date,outdoorTemp,'b.-', date, onOff, 'k--')
plt.xlabel('Time')
xp, labels = plt.xticks()
plt.setp(labels, rotation=45)
plt.ylabel('Temperature')
plt.title('Home Temperature Monitor')
plt.grid(True)
plt.legend(['Indoor', 'Set Point', 'Outdoor', 'On/Off'], loc='upper left')
plt.ylim(0,100)
plt.show()

