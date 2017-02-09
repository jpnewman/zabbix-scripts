
# Known Issues

## Service Unavailable: Back-end server is at capacity

The Zabbix server can sometime return with error: -

~~~
urllib2.HTTPError: HTTP Error 503: Service Unavailable: Back-end server is at capacity
~~~

### Fix

Check that the server is online and the ```zabbix-server``` service is running. If not start it.
