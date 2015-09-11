#! /usr/bin/python
"""This script is for the UCD MSc. in Business Analytics, specifically the
   Analytics Research modules programming assignment. It opens a database
   connection and reads the data out of it into relevant data structures. It
   then checks the distance between all possible pairs of Plant and Port,
   returning the results in order of proximity to help a company choose the
   optimal set up geographically."""

from collections import namedtuple
from enum import Enum
import math
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
    else: raise AttributeError
    self.unique_name = (
      str(type) + ' Lon:' + str(longitude) + ' Lat:' + str(latitude))
    
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


def get_data(database_name):
  """Gets our data and returns two lists of Location Objects. One list of Ports
     and one of Plants"""   
  def get_plants(cursor):
    """Takes a database connection with a ports table
          cursor: a database cursor
        
        Returns:
            A list of Location objects representing Plants."""
    plantlist = []
    plants = cursor.execute('select long, lat, production from location')
    for longitude, latitude, production in plants:
      plant = Location(longitude, latitude, LocationType.Plant, production)
      plantlist.append(plant)
    return plantlist
    
  def get_ports(cursor):
    """Takes a database connection with a ports table
          cursor: a database cursor
        
        Returns:
          A list of Location objects representing Ports."""
    portlist = []
    ports = cursor.execute('select long, lat from ports')
    for longitude, latitude in ports:
      port = Location(longitude, latitude, LocationType.Port)
      portlist.append(port)
    return portlist

    
  conn = sqlite3.connect(database_name)
  cursor = conn.cursor()
  plants = get_plants(cursor)
  ports = get_ports(cursor)
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
          DistanceTuple(plant.unique_name, port.unique_name, distance))
  distance_list.sort(key=lambda x: x.Distance)
  return distance_list


def main():
  plants, ports = get_data('renewable.db')  
  ordered_list = rank_pairs(plants, ports)
  print ordered_list


if __name__ == "__main__":
    main()