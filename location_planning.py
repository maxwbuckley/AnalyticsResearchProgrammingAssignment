#! /usr/bin/python
"""This script is for the UCD MSc. Business Analytics, specifically the
   Analytics Research modules programming assignment. It opens a database
   connection and reads the data out of it into relevant data structures. It
   then checks the distance between all possible pairs of Plant and Port,
   returning the results in order of proximity to help a company choose the
   optimal set up geographically."""

from collections import namedtuple
from enum import Enum
from math import sqrt
import os
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
    """Tests Location objects for equivalence"""
    return (isinstance(other, Location) and self.longitude == other.longitude
            and self.latitude == other.latitude and self.type == other.type and
            self.production == other.production)

  def distance_to(self, target_location):
    """Returns the euclidean distance from this location to another Location.

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
    return sqrt((self.longitude - target_location.longitude)**2 +
                     (self.latitude - target_location.latitude)**2) 


DistanceTuple = namedtuple('DistanceTuple', ['Plant', 'Port', 'Distance',
                                             'Production'])

def _get_plants(cursor):
  """Takes a database connection with a 'location' table in the database.
     
     Args:
         cursor: a database cursor.
     
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
     
     Args:      
         cursor: a database cursor.
     
     Returns:
         A list of Location objects representing Ports."""
  portlist = []
  ports = cursor.execute('SELECT long, lat FROM ports;')
  for longitude, latitude in ports:
    port = Location(longitude, latitude, LocationType.Port)
    portlist.append(port)
  return portlist


def get_data(database_name):
  """Takes a database with 'ports' and 'location' tables and returns the data in
     two lists of relevant objects. Both lists are of Location objects. One list
     is of Plants and one is of Ports.

     Args:
         database_name: a string name of a databse file in the folder.

     Returns:
         Two lists of Location objects, one of Ports and one of Plants.

     Raises:
         A sqlite3 error if the specified database does not exist.""" 
  if os.path.isfile(database_name):
    conn = sqlite3.connect(database_name)
    cursor = conn.cursor()
    plants = _get_plants(cursor)
    ports = _get_ports(cursor)
    conn.close()
    return plants, ports
  else:
    # Database does not exist.
    print "The specified database %s does not exist." % database_name
    raise sqlite3.Error
  

def rank_pairs(plant_list, port_list):
  """Takes a list of potential plant locations and a list of port locations and
     returns a list of DistanceTuple's with the pair of locations order by
     euclidean distance from the closest pair to the farthest away pair. The
     potential production volumes are also included as the business need may
     vary. 
     
     Args:
         plant_list: A list of Locations of type LocationType.Plant
         port_list: A list of Locations of type LocationType.Port
     Returns:
         A list of 'DistanceTuple' named tuples sorted by distance.
  """
  distance_list = []
  for plant in plant_list:
    for port in port_list:
      distance = plant.distance_to(port)
      distance_list.append(
          DistanceTuple(str(plant), str(port), distance, plant.production))
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
