#import pandas as pd
#import geopandas as gpd
#from geopandas.tools import sjoin
#import json
#import matplotlib as mpl
#import numpy as np

import library as l


"""(ok)"""
#Load met stations 
stations = l.met_stations()


"""(ok)"""
#Get catchments data from NVE 

catchment = l.catch()


#loop through catchments
for i in range(1,2):
    i = 12

    """(close)"""    
    #Find stations within a catchment
    l.match(catchment, stations)
    
    """(ok)"""
    #Get Met data for relevant stations
    
    """(  )"""
    #Get Runoff data for relevant catchment from NVE

    """(  )"""
    #Calculate average met data within that catchment

    """(  )"""
    #run LSTM model for catchment

