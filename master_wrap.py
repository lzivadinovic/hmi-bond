#!/usr/bin/env python
# coding: utf-8

from enhance import enhance
import sunpy.map
# Load noaa2harp module
from noaa2harp import noaa2harp
import requests
import glob
import os
# Process needs more testing
from process import process_continuum

# initialize object and get harpnum
a = noaa2harp()
a.update_dataset()
HARPNUM = a.noaa2harp("11950")
print(HARPNUM)

# create query and fetch data
MY_MAIL='lazar.zivadinovic.994@gmail.com'
import os
# Lets make jsoc query 
from sunpy.net import jsoc
from sunpy.net import attrs as a
from sunpy.time import parse_time
#initialize client
client = jsoc.JSOCClient()

data_root='./data'
#DOWNLOAD_PATH_FOR_RAW_DATA
download_path=os.path.join(data_root,str(HARPNUM),'raw')

###### THIS IS THE REAL QUERY, LETS MAKE SOMETHING SMALLER FOR TESTING ########
# Create query
resjsoc = client.search(a.jsoc.PrimeKey('HARPNUM', HARPNUM),
                        a.jsoc.Series('hmi.sharp_cea_720s'),
                        a.jsoc.Segment('Bp') & a.jsoc.Segment('Bt') & 
                        a.jsoc.Segment('Br') & a.jsoc.Segment('continuum'))#,
                        a.jsoc.Notify(MY_MAIL))

#Lets fetch few images for testing
#Note that client.jsoc does not support slice, so we need new query
#This is a way around it
# Small samplesize lets test on 4 imgs
#T1 = resjsoc.table['T_REC'][0]
#T2 = resjsoc.table['T_REC'][3]
#resjsoc = client.search(a.jsoc.PrimeKey('HARPNUM', HARPNUM),
#                        a.Time(T1,T2),
#                        a.jsoc.Series('hmi.sharp_cea_720s'),
#                        a.jsoc.Segment('Bp') & a.jsoc.Segment('Bt') & 
#                        a.jsoc.Segment('Br') & a.jsoc.Segment('continuum'),
#                        a.jsoc.Notify(MY_MAIL))
#
result = client.fetch(resjsoc, path=download_path, progress=True, wait=True)

if result.errors:
    print("We had some errors, here is log")
    print(result.errors)
    print("Lets fetch them via requests library")
    for reserr in result.errors:
        r = requests.get(reserr.url)
        if r.ok:
            print("Content fetched, saving...")
        path_for_new_img = os.path.join(download_path,reserr.url.split('/')[-1])
        with open(path_for_new_img, 'wb') as f:
            f.write(r.content)
            print("File saved to {}".format(path_for_new_img))
    #we should have all results now, lets update results list
    result = glob.glob(os.path.join(download_path,'*'))


print(result)


# Ok, lets sort continuum images and process them
cont = sorted([ res for res in result if 'continuum' in res])
print(cont)

process_continuum(cont)

