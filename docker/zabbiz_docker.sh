#!/usr/bin/env bash

MYSQL_ROOT_USERNAME=root
MYSQL_ROOT_PASSWORD=password123
GUI_TIMEZONE=UTC

ZABBIX_WEB_PORT=32782
ZABBIX_MYSQL_PORT=32784 # For connecting to the database from host.

NUMBER_OF_AGENTS=2

# DO NOT: Change the order as they are subscripted in function 'create_containers'. Otherwise update subscript indexes.
CONTAINER_NAMES=('zabbix-server' 'zabbix-gui' 'zabbix-db')
CONTAINER_AGENT_PREFIX='zabbix-agent'

###############################################################################
# Functions
###############################################################################
kill_all_containers() {
  kill_containers "${CONTAINER_NAMES[@]}"
  for i in $(seq -f "%02g" 1 $NUMBER_OF_AGENTS); do
    kill_containers "$CONTAINER_AGENT_PREFIX-$i"
  done
}

kill_containers() {
  for c in "$@"; do
    echo $c
    RUNNING=$(docker inspect --format='{{ .State.Running }}' $c 2> /dev/null)
    if [ "$RUNNING" == "true" ]; then
      docker stop $c
      docker rm $c
    fi
  done
}

get_ip_addr() {
   echo "$(docker inspect --format='{{ .NetworkSettings.IPAddress }}' $1)"
}

create_containers() {
  # Zabbix MySQL
  # https://hub.docker.com/r/library/mysql/
  MYSQL_CID=$(docker run -p $ZABBIX_MYSQL_PORT:3306 --name "${CONTAINER_NAMES[2]}" -e MYSQL_ROOT_PASSWORD=$MYSQL_ROOT_PASSWORD -d mysql:latest)
  MYSQL_IP=$(get_ip_addr "$MYSQL_CID")
  echo "MySQL (${CONTAINER_NAMES[2]}) IP Address: $MYSQL_IP"
  sleep 30

  # Zabbix Server
  # https://hub.docker.com/r/zabbix/zabbix-server-mysql/
  ZABBIX_SERVER_CID=$(docker run --name "${CONTAINER_NAMES[0]}" -e DB_SERVER_HOST="$MYSQL_IP" -e MYSQL_USER="$MYSQL_ROOT_USERNAME" -e MYSQL_PASSWORD="$MYSQL_ROOT_PASSWORD" -d zabbix/zabbix-server-mysql:latest)
  ZABBIX_SERVER_CID_IP=$(get_ip_addr "$ZABBIX_SERVER_CID")
  echo "Zabbix Server (${CONTAINER_NAMES[0]}) IP Address: $ZABBIX_SERVER_CID_IP"
  sleep 60

  # Zabbiz GUI
  # https://hub.docker.com/r/zabbix/zabbix-web-nginx-mysql/
  ZABBIX_WEB_CID=$(docker run -p $ZABBIX_WEB_PORT:80 --name "${CONTAINER_NAMES[1]}" -e DB_SERVER_HOST="$MYSQL_IP" -e MYSQL_USER="$MYSQL_ROOT_USERNAME" -e MYSQL_PASSWORD="$MYSQL_ROOT_PASSWORD" -e ZBX_SERVER_HOST="$ZABBIX_SERVER_CID_IP" -e TZ="$GUI_TIMEZONE" -d zabbix/zabbix-web-nginx-mysql:latest)
  ZABBIX_WEB_CID_IP=$(get_ip_addr "$ZABBIX_WEB_CID")
  echo "Zabbix Web Server (${CONTAINER_NAMES[1]}) IP Address: $ZABBIX_WEB_CID_IP (http://localhost:$ZABBIX_WEB_PORT)"
  sleep 30

  python ../sync-zabbix-config/sync-zabbix-config.py import http://localhost:$ZABBIX_WEB_PORT/ --data-path ./_zabbix_data -o action user

  # Zabbix Agent
  # https://hub.docker.com/r/zabbix/zabbix-agent/
  for i in $(seq -f "%02g" 1 $NUMBER_OF_AGENTS); do
    cmd="docker run --link ${CONTAINER_NAMES[0]} --name '$CONTAINER_AGENT_PREFIX-$i' --privileged -e ZBX_HOSTNAME='zabbix-agent-$i' -e ZBX_SERVER_HOST='$ZABBIX_SERVER_CID_IP' -e ZBX_METADATA='Linux' -d zabbix/zabbix-agent:latest"
    echo $cmd
    ZABBIX_AGENT_CID=$(eval $cmd)
    ZABBIX_AGENT_CID_IP=$(get_ip_addr "$ZABBIX_AGENT_CID")
    echo "Zabbix Agent ($CONTAINER_AGENT_PREFIX) IP Address: $ZABBIX_AGENT_CID_IP"
  done
}

###############################################################################
# Main
###############################################################################
main() {
  echo '------------------------------------------------------------------------------'
  echo 'Killing Containers'
  echo '------------------------------------------------------------------------------'
  kill_all_containers

  echo '------------------------------------------------------------------------------'
  echo 'Creating Containers'
  echo '------------------------------------------------------------------------------'
  create_containers

  echo '------------------------------------------------------------------------------'
  echo 'Listing Containers'
  echo '------------------------------------------------------------------------------'
  docker ps
}

main
