#!/usr/bin/env python3
import re
import socket
import datetime
import time
from struct import pack
from influxdb import InfluxDBClient

# put your influx server ip, port number and the name of the database
server_ip = '192.168.10.13'
server_port = 8086
db_name = 'ups_stats'

# apcupsd server ip, port number
HOST = ('192.168.10.200') 
PORT = 3551
#PORT = 3493

# iso = datetime.datetime.now()
iso = datetime.datetime.utcnow().isoformat() + 'Z'

while True:

    # Open socket with remote host
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))

    # Send command: Packet is pad byte, size byte, and command
    s.send(pack(b'xb6s', 6, b'status'))

    # Ditch the header
    s.recv(1024)
    time.sleep(.25)
    data = s.recv(4096)
    s.close()
    #print ('Received', repr(data))

    bytes2STR = data.decode('utf-8')

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