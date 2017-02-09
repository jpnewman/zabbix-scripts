
# Zabbix Docker

This script uses the following docker images to create a Zabbix stack, for testing: -

- [mysql](https://hub.docker.com/_/mysql/)
- [zabbix/zabbix-server-mysql](https://hub.docker.com/r/zabbix/zabbix-server-mysql/)
- [zabbix/zabbix-web-nginx-mysql](https://hub.docker.com/r/zabbix/zabbix-web-nginx-mysql/)
- [zabbix/zabbix-agent](https://hub.docker.com/r/zabbix/zabbix-agent/)

> All images use tag ```latest```.

## Run

~~~
chmod u+x zabbiz_docker.sh

./zabbiz_docker.sh
~~~

## Script variables

|Variable|Description|Default|
|---|---|---|
|```MYSQL_ROOT_USERNAME```|MySQL Root Username|root|
|```MYSQL_ROOT_PASSWORD```|MySQL Root Password|password123|
|```GUI_TIMEZONE```|PHP GUI Timezone|UTC|
|```ZABBIX_WEB_PORT```|GUI Port|32782|
|```ZABBIX_MYSQL_PORT```|MySQL Port|32784|
|```NUMBER_OF_AGENTS```|Number of Zabbix Agents to run|2|
|```CONTAINER_NAMES```|Names to use for containers<br /><br />**The order of these names should not be changed!**|```zabbix-server```<br />```zabbix-gui```<br />```zabbix-db```<br />```zabbix-agent```|
|```CONTAINER_AGENT_PREFIX```|Agent Container prefix|```zabbix-agent```|

## Auto-registration

After about a minute the agents should be automatically registered with the Zabbix Server.

*e.g.* <http://localhost:32782/hosts.php>

## License

MIT / BSD

## Author Information

John Paul Newman
