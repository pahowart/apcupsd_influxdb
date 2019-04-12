# apcupsd_influxdb
Python script to capture apcupsd stats and put them into influxdb. 

This script can be used to replace APCUPSD's cgi webmon page.
While running, this script will connect to apcupsd NIS using sockets and pull status information. It will then apply regex to extract key values and dump them into an influx db. 

You can then use Grafana with the influxdb plugin to display the UPS information. 

I have included my Grafana dashboard "UPS Stats.json" to get you started.

apcupsd_influxdbV2 is the final version. 
apcupsd_influxdbv1 uses a different method to get the stats but may be of interest to folks that don't want to use sockets.
