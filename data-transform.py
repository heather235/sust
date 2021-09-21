#!/usr/bin/env python3
import pandas as pd
import regex as re
import uuid

data = pd.read_csv('data/raw_data.csv',sep=',')
data['uuid']= [uuid.uuid4() for x in range(len(data))]

# clean/check values before truncating into decades
# filter out lat/lng, zip & the year 2100 (for now)
values = data.drop(labels=['lat','lng','zip_code','2100'],axis=1)

#saving spatial data slice for later
spatial = data.filter(['lat','lng','zip_code','uuid'],axis=1)
spatial.to_csv('data/spatial.csv')

# now truncate into decades
grouped = values.groupby(lambda col: col[:-1], axis=1)
max_risk = grouped.max()

#update column names
col_names = max_risk.columns.values.tolist()
new_col_names = []
for col in col_names:
	substitute = re.sub(r'\d{3}',r'\g<0>0-\g<0>9',col)
	new_col_names.append(substitute)

max_risk.set_axis(new_col_names, axis=1, inplace=True)
max_risk.rename(columns={'uui':'uuid'}, inplace=True,)
max_risk.to_csv('data/max_risk.csv')