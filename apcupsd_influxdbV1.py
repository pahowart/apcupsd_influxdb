#!/usr/bin/env python3
import re
import subprocess
import datetime
import time
from influxdb import InfluxDBClient

# put your influx server ip, port number and the name of the database
server_ip = '192.168.10.10'
server_port = 8086
db_name = 'ups_stats'

# iso = datetime.datetime.now()
iso = datetime.datetime.utcnow().isoformat() + 'Z'

while True:

    # run apcaccess and capture output to stdout
    result = subprocess.run(['apcaccess'], stdout=subprocess.PIPE)
    result.stdout
    bytes2STR = result.stdout.decode('utf-8') # convert stdout to sting format

    # print(result) # uncomment to print stdout

    values = re.findall(r'(\d+\.\d+)',bytes2STR) # find values using regex, start search at 1500th chr to remove html
    names = re.findall(r'[A-Za-z-]+\w\b',bytes2STR)
    
    #print(values) # uncomment to see regex numerical output
    #print(names) # uncomment to see regex ascill output
    
    # split results we want from "values" in to individual variables
    LINEV = float(values[1])
    LOAD = float(values[2])
    BCHG = float(values[3])
    TIMELEFT = float(values[4])
    BATTV = float(values[7])
    SERVER = (names[3])
    UPSNAME = (names[8])
    STATUS = (names[24])

    # Prepare UPS variabes in JSON format for upload to Influxdb
    json_ups = [
        {
            "measurement": "apcaccess",
            "tags": {
                "status": STATUS,
                "upsname": UPSNAME,
                "server": SERVER
            },
            #"time": iso, # Comment out if influxdb is not writing data points
            "fields": {
                "LINEV": LINEV,
                "LOAD": LOAD,
                "BCHG": BCHG,
                "BATTV": BATTV,
                "TIMELEFT": TIMELEFT,
            }
        }
    ]

    # write values to influxdb
    # note that the username and password are blank, put them inside the '' if you have
    # implemented authentication
    # retries=0 is infinite retries.
    client = InfluxDBClient(server_ip, server_port, '', '', db_name, timeout=5,retries=0)
    try:
        client.create_database(db_name) # will create db if none exists
        client.write_points(json_ups)
    except ConnectionError:
        print('influxdb server not responding')
        #break
    # Wait before repeating loop
    time.sleep(5)
