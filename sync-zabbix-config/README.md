
# Sync Zabbix Configuration

Sync Zabbix Configuration

> - Tested with Zabbix version 3.2.1.
> - Items will not be deleted by this script.

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
|---|---|---|
|```-u```<br />```--user```|Zabbix Username|Admin|
|```-p```<br />```--password```|Zabbix Password|zabbix|
|```-o```<br />```--objects```|Sync specific Zabbix Objects|Defined in script variable ```ZABBIX_OBJECTS``` keys|
|```-a```<br />```--data-path```|```_data'```|
|```-e```<br />```--exclude-empty-objects```|Exclude Empty Objects|False|
|```-l```<br />```--log-level```|Log Level|INFO|
|```-s```<br />```--skip-errors```|Skip Errors|False|
|```--debug```|Debug|False|
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

### Skip Errors

~~~
./sync-zabbix-config.py export http://localhost:32782/ --skip-errors
~~~

### Dry-Run

~~~
./sync-zabbix-config.py export http://localhost:32782/ --dry-run
~~~

## HTML Output

### Install dependencies

> Mac OS X

~~~
brew tap homebrew/dupes/expect
brew install homebrew/dupes/expect

pip install ansi2html
~~~

### Run

~~~
unbuffer ./sync-zabbix-config.py export http://localhost:32782/ | tee >(ansi2html > sync-zabbix-config.html)
~~~

## License

MIT / BSD

## Author Information

John Paul Newman
