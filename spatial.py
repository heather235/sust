#!/usr/bin/env python3
import configparser
from mapbox import Geocoder
import pandas as pd
import requests
import requests_cache
import json
import regex as re

config = configparser.ConfigParser()
config.read('config.ini')

# Many zip codes appear shortened by 
# removing any leading zeros, they have
# 3-4 digits instead of the expected 5.
# Furthermore -- there are > 40,000 zipcodes
# in the US and many cross state lines, it
# makes sense to query API rather than try to match on zip code

# This script will produce a state 
# and a full zip code from lat/long

# requires a [mapbox access token](https://account.mapbox.com/)

data = pd.read_csv('data/spatial.csv',index_col='uuid')
MAPBOX_ACCESS_TOKEN=config['MAPBOX']['ACCESS_TOKEN']

# Query returns are computationally expensive - make sure to cache
places = []
requests_cache.install_cache('spatial-cache')

max_attempts = 10
attempts = 0

while attempts < max_attempts:
	for index, row in data.iterrows():
		lon=row[2]
		lat=row[1]
		uuid=index
		r = requests.get('https://api.mapbox.com/geocoding/v5/mapbox.places/{},{}.json?types=country,region,postcode&access_token={}'.format(lon,lat,MAPBOX_ACCESS_TOKEN))
		response = r.json()
		# If response empty
		if response['features'] == []:
			place_name='Null'
		# If response not empty
		if response['features'] != []:
			place_name=response['features'][0]['place_name']
			print(lat,lon,place_name)
			places.append((lat,lon,place_name,uuid))
	# If not rate limited, break out of while loop and continue
	if r.status_code != 429:
		break
	# If rate limited, wait and try again
	time.sleep((2 ** attempts) + random.random())
	attempts = attempts + 1


cols=['lat','lng','place_name','uuid']
query_result = pd.DataFrame(places,columns=cols)

# Change place name string to postcode & state
query_result['postcode'] = query_result['place_name'].str.extract(r'(\d{5})') # postcodes
query_result['state'] = query_result['place_name'].str.extract(r"\,?\s?(\w+\s?\w+?)\s\d{5}") #captures state values

# merge in state lookup table (taken from: https://en.wikipedia.org/wiki/ISO_3166-2:US)
state_lookup = pd.read_csv('state-lookup.csv',delimiter='\t')
state_lookup['state']=state_lookup['state'].str.strip()
merged = pd.merge(query_result,state_lookup,how='left',on='state')
add_states = merged.filter(items=['lat','lng','abbrev','uuid'],axis=1)

## Bring back in data and merge on index
max_risk = pd.read_csv('data/max_risk.csv')
max_by_state=pd.merge(max_risk,add_states, how='left', on='uuid')
grouped = max_by_state.groupby('abbrev')
group_by_state=grouped.max()
group_by_state.rename(columns={'abbrev':'state'}, inplace=True)
group_by_state.drop(labels=['Unnamed: 0','uuid','lat','lng'],axis=1, inplace=True)

# last-minute clean-up
filter_col = [col for col in group_by_state if col.startswith('1') or col.startswith('2')]
filtered=pd.DataFrame(group_by_state,columns=filter_col)
x = filtered[(filtered > 100).any(1)]
y = filtered[(filtered < 0).any(1)]
n = filtered[(filtered.isna()).any(1)]

#delete unusual values from main dataframe (data) using id
for df in [x,y,n]:
	if len(df) > 0:
		group_by_state.drop(df.index, axis=0, inplace=True)
		print("OK - dropping {} row".format(len(df)))


#Print to main
group_by_state.to_csv('data/final.csv')
