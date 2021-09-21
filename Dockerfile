# grab latest python
FROM python:latest
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY main.py load-data.py data-transform.py spatial.py config.ini sust-dev-01-3ba63a5afe5a.json spatial-cache.sqlite state-lookup.csv /
COPY data/ ./data/
CMD [ "python", "./main.py" ]
