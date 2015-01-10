""" Aggregate crime data for use in a web application """

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sdipylib.url import download_ambry_db # install: pip install 'git+https://github.com/sdrdl/sdipylib.git'
from lib import plot_rhythm
import csv
import re


download_ambry_db('http://s3.sandiegodata.org/library/clarinova.com/crime-incidents-casnd-linked-0.1.2/crimes.db')
download_ambry_db('http://s3.sandiegodata.org/library/clarinova.com/places-casnd-0.1.7/areastats.db')

import sqlite3
conn = sqlite3.connect('crimes.db')

 
def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d
    
conn.row_factory = dict_factory
 
cur = conn.cursor()
 
cur.execute("attach 'areastats.db' as placestats")

q = """
SELECT crimes.*, 
    CAST(strftime('%W', datetime) AS INTEGER) AS woy ,
    CAST(strftime('%j', datetime) AS INTEGER) AS doy,

    city_stats.code as city_code,
    city_stats.pop as city_pop, city_stats.land as city_area, 
    CAST(city_stats.pop AS REAL)/ CAST(city_stats.land AS REAL) as city_density,
    
    community_stats.pop as community_pop, community_stats.land as community_area, community_stats.name as community_name, 
    CAST(community_stats.pop AS REAL)/ CAST(community_stats.land AS REAL)*1000000 as community_density 
FROM crimes
LEFT JOIN placestats.areastats AS city_stats ON city_stats.type = 'city' AND city_stats.code = crimes.city
LEFT JOIN placestats.areastats AS community_stats ON community_stats.type = 'community' AND community_stats.code = crimes.community
"""

by_area = {}

print "Loading records"

for i, row in enumerate(cur.execute(q)):

    area = row['community'] if row['community'] != '-' else row['city_name']

    if area == 'Unincorporated':
        continue

    if not area in by_area:
        by_area[area] = {}

    if not row['legend'] in by_area[area]:
        by_area[area][row['legend']] = []

    by_area[area][row['legend']].append([row['hour'], row['dow'], row['woy'],row['doy']])
    
    if i % 50000 == 0:
        print "Loaded {} records".format(i)
    
 

rep = re.compile('[\W_]+')
 
for area, area_rows in by_area.items():
    for legend, legend_rows in area_rows.items():
        legend_file_name = rep.sub('',legend.lower())
        area_file_name =  rep.sub('',area.lower())
        fn = 'incidents-{}-{}.csv'.format(area_file_name, legend_file_name)
        print "Writing file", fn
        with open(fn,'w') as f:
           w = csv.writer(f)
           w.writerow('hour dow woy doy'.split())
           w.writerows(legend_rows)
    
   

   
        
    