#!/usr/bin/env python3
import tarfile

# 1) Download data from GCS, save to data.csv
exec(open("./load-data.py").read())

# 2) Transform data - truncate columns by decade, etc
exec(open("./data-transform.py").read())

# 3) Geocode data lat/lon, update to full zipcode
#	  create spatial datafile
exec(open("./spatial.py").read())

with tarfile.open("final_data.tar.bz2", "w:bz2") as f:
	for name in ["data/final.csv"]:
		f.add(name)
