#!/bin/bash

CONTAINER_NAME='storm-rpmbuild'
CONTAINER_EXPOSED_PORT="8080"
CONTAINER_PUBLISHED_PORT="$CONTAINER_EXPOSED_PORT/tcp"

[ -f env.sh ] && . env.sh

CID=$(docker ps -f name=$CONTAINER_NAME -q)

if [ -z "$CID" ]; then
  CID=$(docker ps -f name=$CONTAINER_NAME -f status=exited -q)

  [ -z $CID ] && docker run -dP --name $CONTAINER_NAME $CONTAINER_NAME || docker start $CONTAINER_NAME
fi

PUBLISHED_PORT=$(docker inspect -f "{{(index (index .NetworkSettings.Ports \"$CONTAINER_PUBLISHED_PORT\") 0).HostPort }}" $CONTAINER_NAME)

HOST_INFO=
if [ -n "$DOCKER_HOST" ]; then
  HOST_INFO="${DOCKER_HOST#tcp://}"
  HOST_INFO="${HOST_INFO%:*}"
else
  HOST_INFO='127.0.0.1'
fi

cat > apache-storm.repo <<EOF
[apache-storm-el6]
name='apache-storm-el6 repo'
baseurl=http://${HOST_INFO}:$PUBLISHED_PORT/RedHat/6/x86_64/
enabled=1
gpgcheck=0
EOF

echo "http://${HOST_INFO}:${PUBLISHED_PORT}/RedHat/6/x86_64/"
