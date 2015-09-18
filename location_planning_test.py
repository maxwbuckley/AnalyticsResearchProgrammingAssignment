#! /usr/bin/python
"""Unit tests associated with location_planning.py"""

import unittest
from mock import Mock
import location_planning
from math import sqrt
from location_planning import Location, LocationType, DistanceTuple

class TestLocation(unittest.TestCase):
  """Unit tests associated with the Location Class"""
  def test_init(self):
    test_location = Location(10.0, 30.0, LocationType.Plant, 100000)
    self.assertEqual(test_location.longitude, 10)
    self.assertEqual(test_location.latitude, 30)
    self.assertEqual(test_location.production, 100000)
    self.assertEqual(test_location.type, LocationType.Plant)

  def test_init_fail_wrong_location_category(self):
    with self.assertRaises(ValueError):
      Location(100, 100, 'House')

  def test_to_str(self):
    test_location = Location(50.0, 50.0, LocationType.Plant, 100000)
    self.assertEqual(str(test_location), 'Plant Lon:50.0 Lat:50.0')

  def test_distance_to(self):
    test_location = Location(50.0, 50.0, LocationType.Plant, 100000)
    test_target_location1 = Location(50.0, 55.0, LocationType.Port)
    test_target_location2 = Location(55.0, 50.0, LocationType.Port)
    test_target_location3 = Location(49.0, 51.0, LocationType.Port)
    self.assertEqual(test_location.distance_to(test_target_location1), 5)
    self.assertEqual(test_location.distance_to(test_target_location2), 5)
    self.assertEqual(test_location.distance_to(test_target_location3),
                     sqrt(2))

  def test_distance_to_fail(self):
    test_location = Location(50.0, 50.0, LocationType.Plant, 100000)
    with self.assertRaises(TypeError):
      test_location.distance_to(1)

class TestLocationPlanningFunctions(unittest.TestCase):
  """Unit tests associated with the functions in location_planning.py"""
  def test_get_plants(self):
    mock = Mock()
    cursor = mock.connection.cursor.return_value
    cursor.execute.return_value = [(1.0, 1.0, 1000)]
    self.assertEquals(location_planning._get_plants(cursor), [
        Location(1.0, 1.0, LocationType.Plant, 1000)])

  def test_get_ports(self):
    mock = Mock()
    cursor = mock.connection.cursor.return_value
    cursor.execute.return_value = [(5.0, 5.0)]
    self.assertEquals(location_planning._get_ports(cursor), [
        Location(5.0, 5.0, LocationType.Port)])

  def test_rank_pairs(self):
    plant_list = [Location(0.0, 0.0, LocationType.Plant, 1000)]
    port_list = [Location(5.0, 5.0, LocationType.Port),
                 Location(10.0, 10.0, LocationType.Port),
                 Location(15.0, 15.0, LocationType.Port)]
    expected_return_value = [
        DistanceTuple(Plant='Plant Lon:0.0 Lat:0.0', Port='Port Lon:5.0 Lat:5.0'
        , Distance=sqrt(50)), DistanceTuple(Plant='Plant Lon:0.0 Lat:0.0',
        Port='Port Lon:10.0 Lat:10.0', Distance=sqrt(200)), DistanceTuple(Plant=
        'Plant Lon:0.0 Lat:0.0', Port='Port Lon:15.0 Lat:15.0', Distance=sqrt(
        450))]
    returned_ranks = location_planning.rank_pairs(plant_list, port_list)
    self.assertEqual(expected_return_value, returned_ranks)
    # Make sure the returned values are in ascending order.
    for i, elem in enumerate(returned_ranks):
      if i > 0:
        self.assertGreaterEqual(elem.Distance, returned_ranks[i-1].Distance)

if __name__ == '__main__':
  unittest.main()
