import pandas as pd
import geopandas as gpd
#from geopandas.tools import sjoin
import json
import matplotlib as mpl
import numpy as np


def met_stations():
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
    
    return Stat




def catch():
    #multypolygons for different Catchments, One main and several sub-catchments.
    #read data from NVE... 
    catchments = gpd.read_file('./Data/NVEData.gdb/', layer=0)
    #catchments['geometry'][1] # draw area
    #print(c['geometry'][1])
        # MULTIPOLYGON (((13.55422274200004 66.54195477900004, 13.55408583600007 66.54185024300006, 
        # 13.55405569400006 66.54175381500005, 13.55436763100005 66.54161424800003,...￼ ￼￼
    
    #Get catchments numbers
    b1 = catchments['vassdragsnummer'][:]
    b2 = pd.DataFrame(b1[:].str.split(pat="."))
    b2[['vdNR','Rest','none']] = pd.DataFrame(b2.vassdragsnummer.tolist(), index= b2.index)
    catchNR = pd.DataFrame(b2['vdNR'][:].astype(int))
    #test = catchments
    #test = pd.concat([catchments, catchNR], axis=1)
    print("Number of catchments: ",catchNR.vdNR.max()) 

    # Select rows with same catchment numbers
    for i in range(catchNR.vdNR.min(),catchNR.vdNR.max()):
        oneCatch = catchments[catchNR['vdNR'] == i]
        
        # find Geometry to largest cachment within same chatcmente area (main catchment)
        oneCatchGeo = oneCatch['geometry'][oneCatch.regineAreal_km2 == oneCatch.regineAreal_km2.max()]
    
    return oneCatchGeo #a multypoligon of main catchment 
    

        
        
def match(catch, stations): 
    #find stations inside a catchment
    
    #gdf = geopandas.GeoDataFrame(
    #df, geometry=gdp.points_from_xy(df.Longitude, df.Latitude), crs="EPSG:4326")
    
    test = gpd.GeoSeries.from_wkt(Stat["coordinates"])
    StationsInCatch = gpd.sjoin(stations, catch, how='left')
    StationsInCatch = gpd.sjoin(Stat, oneCatchGeo, how='left')
    StationsInCatch = gpd.sjoin(s['coordinates'], oneCatchGeo, how='left', op='within')
    grouped = pointInPolys.groupby('index_right')
    list(grouped)
    #    [(0.0,      geometry                               id_left  index_right id_right  
    #
    #      1  POINT (-0.58898847631242 0.17797695262484)       None      0.0        1.0 
    #      3  POINT (0.4993597951344431 -0.06017925736235585)  None      0.0        1.0
    #      5  POINT (-0.3764404609475033 -0.4750320102432779)  None      0.0        1.0 
    #      6  POINT (-0.3098591549295775 -0.6312419974391805)  None      0.0        1.0 ]
    print(grouped.groups)
    #      {0.0: [1, 3, 5, 6]}         



def met_data():
    # Insert your own client ID here
    client_id = '7ee4ddb1-336e-492f-9315-6090eb7bb44e'

    # Define endpoint and parameters
    endpoint = 'https://frost.met.no/observations/v0.jsonld'


    """
    parameters = {
        'sources': 'SN18700',
        'elements': 'max(air_temperature P1D),min(air_temperature P1D),best_estimate_sum(precipitation_amount P1D),mean(water_vapor_partial_pressure_in_air P1D)',# ,sum(duration_of_sunshine P1D),accumulated(liquid_water_content_of_surface_snow),surface_snow_thickness',
        'referencetime': '1980-01-01/2024-02-20',
        }
    """
    parameters = {
        'sources': 'SN18700,SN90450',
        'elements': 'mean(air_temperature P1D),sum(precipitation_amount P1D),mean(wind_speed P1D)',
        'referencetime': '2010-04-01/2010-04-03',
        }
    # Issue an HTTP GET request
    r = requests.get(endpoint, parameters, auth=(client_id,''))
    # Extract JSON data
    json = r.json()

    # Check if the request worked, print out any errors
    if r.status_code == 200:
        data = json['data']


    
    # This will return a Dataframe with all of the observations in a table format
    df = pd.DataFrame()
    for i in range(len(data)):
        row = pd.DataFrame(data[i]['observations'])
        row['referenceTime'] = data[i]['referenceTime']
        row['sourceId'] = data[i]['sourceId']
        df = pd.concat([df,row])
        
    df = df.reset_index()
        
    df.head()
    
    
    # These additional columns will be kept
    columns = ['sourceId','referenceTime','elementId','value','unit','timeOffset']
    df2 = df[columns].copy()
    # Convert the time value to something Python understands
    df2['referenceTime'] = pd.to_datetime(df2['referenceTime'])
    
    # Preview the result
    df2.head()

            



def runoff():
    station = 
    parameter = 
    resolution_time = 
    reference_time = 
    api_key =
    
    
    baseurl = "https://hydapi.nve.no/api/v1/Observations?StationId={station}&Parameter={parameter}&ResolutionTime={resolution_time}"
    
    url = baseurl.format(station=station, parameter=parameter,
                     resolution_time=resolution_time)
        
    if reference_time is not None:
        url = "{url}&ReferenceTime={reference_time}".format(
            url=url, reference_time=reference_time)
        
        print(url)

    request_headers = {
        "Accept": "application/json",
        "X-API-Key": api_key
        }
    
    request = Request(url, headers=request_headers)
    
    response = urlopen(request)
    content = response.read().decode('utf-8')
    
    parsed_result = json.loads(content)
    
    
    for observation in parsed_result["data"]:
        print(observation)
        
        
        
        