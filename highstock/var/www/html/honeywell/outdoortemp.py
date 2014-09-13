#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from honeywell_db import Base, Data
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
import json
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


data = json.dumps([[(int(x.Date.strftime("%s")) * 1000) - (3600000*5), x.Temperature] for x in session.query(Data).all()])
print data
