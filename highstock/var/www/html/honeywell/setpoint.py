#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from honeywell_db import Base, Data
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import json
import cgi
import cgitb
cgitb.enable()

print 'Content-Type: text/plain;charset=utf-8'
print

DB_USER = "YOUR DB USER"
DB_PASS = "YOUR DB PASS"

engine = create_engine('mysql://%s:%s@localhost:3306/thermostat' % (DB_USER, DB_PASS))
Base.metadata.bind = engine
DBSession = sessionmaker()
DBSession.bind = engine
session = DBSession()

db_data = []
for x in session.query(Data).all():
    if x.SystemSwitchPosition == 1:
        db_data.append([(int(x.Date.strftime("%s")) * 1000) - (3600000*5), x.HeatSetpoint])
    elif x.SystemSwitchPosition == 3:
        db_data.append([(int(x.Date.strftime("%s")) * 1000) - (3600000*5), x.CoolSetpoint])
    else:
        db_data.append([(int(x.Date.strftime("%s")) * 1000) - (3600000*5), 0])

data = json.dumps(db_data)
print data

