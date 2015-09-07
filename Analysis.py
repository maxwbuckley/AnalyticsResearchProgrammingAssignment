#! /usr/bin/python
""" Docstring"""
import sqlite3
import math


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
  def distance_From_Port(self, port):
      return math.sqrt((self.longitude - port.longitude)**2 +
                       (self.latitude - port.latitude)**2) 

## Two tables; location and ports
def get_Ports(conn):
  """Takes a database connection with a ports table
      conn = a database connection
      
      returns a list of Port objects."""
  portlist = []
  ports = c.execute('select long, lat from ports')
  for longitude, latitude in ports:
    port = Port(longitude, latitude)
    portlist.append(port)
  return portlist


ports = get_Ports(conn)
test_Location = Location(40.0, 50.0, 100000)

for port in ports:
  print test_Location.distance_From_Port(port)

##ports = c.execute('select long, lat, production from location')
  
