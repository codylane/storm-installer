#!/bin/bash

STORM_VERSION="${STORM_VERSION:-1.0.2}"
STORM_RPMBUILD_REPO="https://github.com/codylane/storm-installer.git"
STORM_TARGZ_FILE="apache-storm-${STORM_VERSION}.tar.gz"
STORM_TARGZ_URL="http://mirrors.advancedhosters.com/apache/storm/apache-storm-${STORM_VERSION}/apache-storm-${STORM_VERSION}.tar.gz"

CONTAINER_NAME="storm-rpmbuild"

# Allows you to override what version you want to build via the commandline
[ -f env.sh ] && . env.sh "$1"

echo "STORM_VERSION=$STORM_VERSION"
echo "STORM_RPMBUILD_REPO=$STORM_RPMBUILD_REPO"
echo "STORM_TARGZ_FILE=$STORM_TARGZ_FILE"
echo "STORM_TARGZ_URL=$STORM_TARGZ_URL"

[ ! -d storm-installer ] && git clone $STORM_RPMBUILD_REPO storm-installer

[ -e $STORM_TARGZ_FILE ] || curl "$STORM_TARGZ_URL" -o $STORM_TARGZ_FILE

# always pull the latest version
pushd storm-installer
git fetch --all
git checkout storm-${STORM_VERSION}
git pull
popd

BUILD_DIR="apache-storm-build"

mkdir -p ${BUILD_DIR}
rsync -av --delete storm-installer $BUILD_DIR/
rsync -av --delete $STORM_TARGZ_FILE $BUILD_DIR/

tar czvf $BUILD_DIR.tar.gz $BUILD_DIR

mkdir -p builds
mv $BUILD_DIR.tar.gz builds

docker build -t $CONTAINER_NAME .
