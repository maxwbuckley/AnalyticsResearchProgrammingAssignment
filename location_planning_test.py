"""Unit tests associated with location_planning.py"""
## TODO(max): Complete
import location_planning
from location_planning import Location, LocationType, DistanceTuple
test_Location = Location(40.0, 50.0, LocationType.Plant, 100000)
test_target_location = Location(40.0, 55.0, LocationType.Port)
print test_Location.distance_to(test_target_location)
  