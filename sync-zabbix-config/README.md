
# Sync Zabbix Configuration

Sync Zabbix Configuration

> Items will not be deleted by this script.

## Install python requirements

~~~bash
pip install -r requirements.txt
~~~

## Run

### Required Arguments

|Argument Position|Description|Options
|---|---|---|
|*FIRST*|Action|Export / Import|
|*SECOND*|Zabbix Server||

### Optional Arguments

|Argument|Description|Default|
|---|---|---|---|
|```-u```<br />```--user```|Zabbix Username|Admin|
|```-p```<br />```--password```|Zabbix Password|zabbix|
|```-o```<br />```--objects```|Sync specific Zabbix Objects|Defined in script variable ```ZABBIX_OBJECTS``` keys|
|```-a```<br />```--data-path```|```_data'```|
|```-e```<br />```--exclude-empty-objects```|Exclude Empty Objects|False|
|```-l```<br />```--log-level```|Log Level|INFO|
|```-d```<br />```--dry-run```|Dry-run. No action taken|False|

### Export

~~~
./sync-zabbix-config.py export http://localhost:32782/

./sync-zabbix-config.py export http://localhost:32782/ -u Admin -p zabbix
~~~

#### Export specific objects

~~~
./sync-zabbix-config.py export http://localhost:32782/ -o action
~~~

### Import

~~~
./sync-zabbix-config.py import http://localhost:32782/
~~~

#### Import specific objects

~~~
./sync-zabbix-config.py import http://localhost:32782/ -o action
~~~

### Dry-Run

~~~
./sync-zabbix-config.py export http://localhost:32782/ --dry-run
~~~

## License

MIT / BSD

## Author Information

John Paul Newman
