#! /usr/bin/python
"""This script is for the UCD MSc. Business Analytics, specifically the
   Analytics Research modules programming assignment. It opens a database
   connection and reads the data out of it into relevant data structures. It
   then checks the distance between all possible pairs of Plant and Port,
   returning the results in order of proximity to help a company choose the
   optimal set up geographically."""

from collections import namedtuple
from enum import Enum
import math
import pandas as pd
import sqlite3

class LocationType(Enum):
  """The Enum of valid location types"""
  Plant = 1
  Port = 2


class Location(object):
  """Our location class.
  
     Stores both geographic and production information related to a given site.
  
      Attributes:
          longitude: a float representing the longitudinal coordinates of the
              location.
          latitude: a float representing the latitudinal coordinates of the
              location.
          type: an enum represting the type of the location.
          production: The production capacity of the given location
  """
  def __init__(self, longitude, latitude, type, production=None):
    self.longitude = longitude  
    self.latitude = latitude
    self.production = production
    if type in LocationType:
      self.type = type
    else: raise ValueError

  def __str__(self):
    string_name = (
      str(self.type) + ' Lon:' + str(self.longitude) + ' Lat:' +
      str(self.latitude)).replace('LocationType.','')
    return string_name

  def __eq__(self, other):
    """Tests Locations objects for equivalence"""
    return (isinstance(other, Location) and self.longitude == other.longitude
            and self.latitude == other.latitude and self.type == other.type and
            self.production == other.production)

  def distance_to(self, target_location):
    """Returns the euclidean distance from this location to another target
       location
       Args:
           self,
           location: a location object
        Returns:
           A float representing the euclidean distance from this location to
           the target location.
       Raises:
           TypeError: The location passed was not of type Location
       
       """
    if type(target_location) != Location:
      raise TypeError
    return math.sqrt((self.longitude - target_location.longitude)**2 +
                     (self.latitude - target_location.latitude)**2) 


DistanceTuple = namedtuple('DistanceTuple', ['Plant', 'Port', 'Distance'])

def _get_plants(cursor):
  """Takes a database connection with a 'location' table in the database.
        cursor: a database cursor
     
      Returns:
          A list of Location objects representing Plants."""
  plantlist = []
  plants = cursor.execute('SELECT long, lat, production FROM location;')
  for longitude, latitude, production in plants:
    plant = Location(longitude, latitude, LocationType.Plant, production)
    plantlist.append(plant)
  return plantlist


def _get_ports(cursor):
  """Takes a database connection with a 'ports' table in the database.
        cursor: a database cursor
      
       Returns:
        A list of Location objects representing Ports."""
  portlist = []
  ports = cursor.execute('SELECT long, lat FROM ports;')
  for longitude, latitude in ports:
    port = Location(longitude, latitude, LocationType.Port)
    portlist.append(port)
  return portlist


def get_data(database_name):
  """Gets our data and returns two lists of Location Objects. One list of Ports
     and one of Plants"""  
  conn = sqlite3.connect(database_name)
  cursor = conn.cursor()
  plants = _get_plants(cursor)
  ports = _get_ports(cursor)
  conn.close()
  return plants, ports
  

def rank_pairs(plant_list, port_list):
  """Takes a list of potential plant locations and a list of port locations and
     returns a list of DistanceTuple's with the pair of locations order by
     euclidean distance from the closest pair to the farthest away pair.
     
     Args:
       plant_list: A list of Locations of type LocationType.Plant
       port_list: A list of Locations of type LocationType.Port
     Returns:
       A list of named tuples sorted by distance.
  """
  distance_list = []
  for plant in plant_list:
    for port in port_list:
      distance = plant.distance_to(port)
      distance_list.append(
          DistanceTuple(str(plant), str(port), distance))
  distance_list.sort(key=lambda x: x.Distance)
  return distance_list


def main():
  """Reads in our database, ranks the different pairs of locations and prints
     out the ordered list and writes it to a csv file for sharing with business
     stakeholders."""
  plants, ports = get_data('renewable.db')  
  ordered_list = rank_pairs(plants, ports)
  data_frame = pd.DataFrame(ordered_list, columns=DistanceTuple._fields)
  print data_frame
  data_frame.to_csv('output.csv', index=False)

if __name__ == "__main__":
    main()
