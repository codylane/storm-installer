#!/bin/bash

[ -n "$1" ] && STORM_VERSION="$1"

STORM_VERSION="${STORM_VERSION:-1.0.2}"

STORM_RPMBUILD_REPO="https://github.com/codylane/storm-installer.git"

STORM_TARGZ_URL="http://mirrors.advancedhosters.com/apache/storm/apache-storm-${STORM_VERSION}/apache-storm-${STORM_VERSION}.tar.gz"

STORM_TARGZ_FILE="apache-storm-${STORM_VERSION}.tar.gz"

CONTAINER_EXPOSED_PORT="8080"

CONTAINER_PUBLISHED_PORT="$CONTAINER_EXPOSED_PORT/tcp"

CONTAINER_NAME="storm-rpmbuild"
