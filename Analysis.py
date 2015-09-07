#! /usr/bin/python
""" Docstring"""
import sqlite3


conn = sqlite3.connect('renewable.db')
c = conn.cursor()

class Port:
  def __init__(self, longitude, latitude):
    self.longitude = longitude  
    self.latitude = latitude

class Location:
  def __init__(self, longitude, latitude, production):
    self.longitude = longitude  
    self.latitude = latitude
    self.production = production

## Two tables; location and ports
ports = c.execute('select long, lat from ports')

portlist = []
for long, lat in ports:
  portlist.append(Port(long, lat))

print portlist[1].longitude



ports = c.execute('select long, lat, production from location')
  
