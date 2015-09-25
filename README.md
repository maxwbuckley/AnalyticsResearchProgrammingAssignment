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

