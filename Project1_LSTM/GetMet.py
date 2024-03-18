# Libraries needed (pandas is not standard and must be installed in Python)
import requests
import pandas as pd

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
    print('Data retrieved from frost.met.no!')
else:
    print('Error! Returned status code %s' % r.status_code)
    print('Message: %s' % json['error']['message'])
    print('Reason: %s' % json['error']['reason'])
    
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