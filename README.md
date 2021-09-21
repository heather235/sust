# Coding assignment - Sust Global
This project was created to transform a dataset supplied by Sust Global. 
The goals were to: 

1) Truncate data from annual to decade maximum risk values
2) Combine data into single state values

This data can be run in two methods:
1) Using the provided Dockerfile
```
$ Docker build -t [your-image-name] .
$ Docker run [your-image-name] 
```
2) Using your own python environment
```
$ python3 -m pip install -r requirements.txt
$ python3 main.py
```
`main.py` starts three seperate scripts: `data-load.py`, `data-transform.py`, and `spatial.py`. `main.py` also compresses the resulting output

Either way, this script also relies on the end-user setting up their own `config.ini` file with appropriate keys.
That file should look like:

```
[GS_CLOUD]

BUCKET_ID= 'your bucket here'
FILE_ID= 'your filepath here'

[MAPBOX]
ACCESS_TOKEN='your token here'
```
You can get a mapbox token here: https://account.mapbox.com/access-tokens/ (provided you have a mapbox account, queries of this size are free) 
The mapbox access token is used in `spatial.py` to correctly match lat/lng pairs to their correct zipcodes and states
The queries used for this data challenged were also cached to: [`spatial-cache.sqlite`](https://github.com/heather235/sust/blob/main/spatial-cache.sqlite)

Lastly, the resulting data output has been uploaded [here as well](https://github.com/heather235/sust/blob/main/final_data.tar.bz2)
