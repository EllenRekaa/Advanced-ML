import pandas as pd
import geopandas as gpd
#from geopandas.tools import sjoin
import json


print("Loading metrological stations...")
with open("Stasjoner.json",encoding="utf8") as file:
    tmp = json.load(file)
    d = tmp["data"] 
    
    stations = pd.DataFrame(d)

#'@type', 'id', 'name', 'shortName', 'country', 'countryCode',
#       'geometry', 'masl', 'validFrom', 'validTo', 'county', 'countyId',
#       'municipality', 'municipalityId', 'stationHolders', 'wmoId',
#       'externalIds', 'wigosId', 'shipCodes'

stations = stations.drop(stations[stations['country'] != 'Norge'].index)
print("Number of stations: ",len(stations))

Stat = stations.drop(['@type', 'name', 'shortName', 'country','countryCode', 'county', 'countyId',
                      'municipality', 'municipalityId', 'stationHolders', 'wmoId',
                      'externalIds', 'wigosId', 'shipCodes'], axis='columns')
#print(Stat.columns)
# ['id', 'geometry', 'validFrom', 'validTo']


# Extracting dictionary values from the 'Details' column and creating new columns
df_details = Stat['geometry'].apply(lambda x: {} if pd.isna(x) else x).apply(pd.Series)['coordinates']

# Concatenating the new columns to the original DataFrame
Stat = pd.concat([Stat, df_details], axis=1)
Stat = Stat.drop(['geometry'], axis='columns')


#co = Stat["geometry"][1]["coordinates"]
#print("Coord", co)

