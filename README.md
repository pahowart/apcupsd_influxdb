# apcupsd_influxdb
Python script to capture apcupsd stats and put them into influxdb. 

This script can be used to replace APCUPSD's cgi webmon page.
In order to operate it must to be installed on the apsupsd host. 
While running, this script will call "apcaccess" and apply regex to extract key values and dump them into an influx db. 

You can then use Grafana with the influxdb plugin to display the UPS information. 

I have included my Grafana dashboard you can use to get started.
