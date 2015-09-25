# Analytics Research Programming Assignment
## Python Programming, Databases, and Version Control Assignment
For this assignment we are required to demonstrate the use of Python, databases
and Git for version control.

The request is that we are to

> Suppose you have been hired by a renewable fuels company, who want to locate a
> processing plant somewhere in Ireland. They already have several raw materials
> locations in Ireland, where they cut down trees. They have decided that the
> new plant will be at one of those locations. The idea is that wood from all 
> locations will be transported by road to the processing plant, and then the
> product will be transported by road to some port. You have been asked to
> choose the location for the processing plant and the choice of port, so as to
> minimize the total road transportation costs.


For this we have been provided a database with two tables 'ports' and 'location'
. We have to read the data out of them, store them in appropriate Python data
structures. Then use a brute force (try all combinations) algorithm, which will
perform the necessary calculations and provide the output for our business
stakeholders.

My approach is well commented in the respective scripts themselves. But
effectively location_planning.py is a script which reads the databases into 
'Location' objects with sensibly named parameters. These Location objects are of
two types 'Port' and 'Plant' which are then stored in their own respective lists
. These lists are then compared by the rank_pairs function which does the brute
force comparison of every 'Port' and every 'Plant'. It stores its output as a
list of named tuples. These amed tuples have a name I constructed for the plant
and port from their type and coordinates as they lacked a true unique identifier
column. The value it stores is the euclidean distance in the same units as the
coordinates. This list is then sorted by ascending distance and converted to a
pandas dataframe. This dataframe is printed to the terminal. However as I know
most business stakeholders prefer using csv. I also write out to a csv
'output.csv' for ease of communication. This script also has associated unit
tests in 'location_planning_test.py' These tests allow us to make sure all the
code is working as intended. This will also make it easier to extend or further
develop this code without introducing new bugs.

# Launching the scripts:
Launching location_planning.py is done as follows and should return something
similar to this below.
```shell
python location_planning.py
                       Plant                     Port  Distance
0   Plant Lon:52.34 Lat:6.48  Port Lon:52.27 Lat:6.39  0.114018
1   Plant Lon:52.86 Lat:8.99   Port Lon:52.7 Lat:8.63  0.393954
2   Plant Lon:53.22 Lat:6.68  Port Lon:53.33 Lat:6.25  0.443847
3   Plant Lon:53.66 Lat:6.69  Port Lon:53.33 Lat:6.25  0.550000
4    Plant Lon:53.18 Lat:6.8  Port Lon:53.33 Lat:6.25  0.570088
5   Plant Lon:52.84 Lat:6.92  Port Lon:52.27 Lat:6.39  0.778332
```

The tests location_planning_test.py can be run as follows and should return
similar

```shell
python location_planning_test.py
........
----------------------------------------------------------------------
Ran 8 tests in 0.001s
```


# Package Dependencies:
sqlite3
pandas
enum
unittest
mock
