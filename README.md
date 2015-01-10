crimeviz
========

Crime Vizualization


Visual Design
-------------

The web interface should permit users to explore variations in crime rates by breaking down counts of crime incidents by:

* Area
** 2-d space, on a map
** City and COmmunity
* Time
** Hour of day
** Day of week
** Week of year.
* Type of Crime
** Major group: Violent, Property, Quality of Life
** Specific: 
*** Residential Vs Commercial Property crime
*** Sex crimes
*** DUI


Crime categories:
* Violent
* Property
* Commercial Property
* Residential Property
* Quality of Life
* Sex crimes ( Prostitution )
* DUI

There are a few different pages:
* Crime counts/density by community, paramterized on crime type as a bar chart
* Crime counts/density by crime type, parameterized by community, as a bar chart
* Temporal heatmaps by community, parameterized on crime type
* Temporal heatmaps by crime type, parameterized on community
* Geographic Heatmap page Parameterized on crimetype and one time dimension. 

Maybe there is a profile for the community/city that has 
* Parameterized on crime type
* each of the three temporal maps
* Each of the three bar charts. 

There are four vizualizations that can be displayed on the heatmap page:
* Geographic heatmap
* Temporal heatmap
* Line chart
* Community bar-chart

The Temporal Heat map also have line charts on each axis. The user can click, or move the mouse on the line charts to set one of the time dimensions. Moving the mouse in 

The Geographic heatmap displays

Data Format
-----------

Create two file for each of the crime categories / communities pairs

The file has incidents groups by hour of year, with each record categorized on:
* Hour of year
* Hour of Day
* Day of week
* Week of year
* geo point


Then, one more set of files for the whole region ( all cities / communities ) that has points grouped by:
* Hour of year
* Hour of Day
* Day of week
* Week of year
* Community




Notes
-----

Use http://www.patrick-wied.at/static/heatmapjs/ for a dynamic heatmap.



