# Storm-Installer

This package is a package group for ease of setting up a storm cluster.

## Environment

* OS: CentOS 6.X
* CPU Arch: x64
* Middleware: Needs JDK6 or after（Oracle JDK or Open JDK）

## Building the apache-storm RPM

Before you build the apache-storm RPM you will need to make sure that you have Docker installed and you have the docker client installed on your workstation.  Please consult `https://www.docker.com/products/overview` to install docker.

Once you have docker installed and your workstation can communicate with your docker host then all you need to do is the following in the directory where you cloned this repo.

### Builing the apache-storm RPM.
```
cd docker
./build.sh
```

or you can also pass a specific build version to `./build.sh 1.0.1` which would build `apache-storm-1.0.1*.rpm`


The above will fire up centos 6 docker container and build the apache-storm RPM.  Note that after the RPM is built this repo will also make sure that the RPM can pass a few integration tests.  If all goes well, you will have a valid apache-storm RPM that you can downloa which will be discussed in the next step.

### Retrieving the apache-storm RPM

This assumes you completed the previous step [Builing the apache-storm RPM]

First confirm that you have a container named `storm-rpmbuild`
```
docker images storm-rpmbuild
REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
storm-rpmbuild      latest              11e0d66946dc        2 days ago          2.393 GB
```

If you get this instead, then the build stage must have failed.  You can use `docker logs <container_id>` to see what went wrong.  You can also run `./build.sh` again to see what went wrong.
```
docker images storm-rpmbuild
REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
```

If you have the `storm-rpmbuild` container image in your inventory then you can run `./run.sh` and you'll be presented with a url that you can copy into your browser to download the RPM.  Also this script will also create a `apache-storm.repo` in your current directory that you can use as a yum repo.

## Before you install storm package

Before you install Storm Package on a cluster,
there are some important steps you need to do to prepare your system.

1.Storm needs zookeeper cluster.
  For zookeeper cluster installation, you find install step on cdh.
  http://www.cloudera.com/content/cloudera/en/documentation/core/latest/topics/installation_installation.html
  http://archive-primary.cloudera.com/cdh5/redhat/6/x86_64/cdh/5.3.2/RPMS/x86_64/

  or below url(in Japanese)
  http://d.hatena.ne.jp/acro-engineer/20111123/1322059295


## Installing storm package

1. Add the apache-storm RPM to your yum repo either external or internal.  Or you can download the RPM to the machine you    want to install storm on and then run `yum localinstall /path/to/apache-storm-1.0.2-1.el6.x86_64.rpm`

2.Install the Storm RPM:
```
# su -
# rpm -ivh apache-storm-1.0.2-1.el6.x86_64.rpm
```

3.Set the zookeeper host and nimbus host to below property.
  (Reference: http://nathanmarz.github.com/storm/doc/backtype/storm/Config.html )
* storm.zookeeper.servers (STORM_ZOOKEEPER_SERVERS)
* nimbus.host             (NIMBUS_HOST)

```
vi /opt/apache-storm/conf/storm.yaml
```

Setting Example:
```
########### These MUST be filled in for a storm configuration
storm.zookeeper.servers:
    - "192.168.100.101"         ## zookeeper host

nimbus.host: "192.168.100.101"  ## nimbus host
```

4.Start or stop storm cluster by following commands:

Start
```
# service storm-nimbus start
# service storm-ui start
# service storm-drpc start
# service storm-logviewer start
# service storm-supervisor start
```

Stop
```
# service storm-supervisor stop
# service storm-logviewer stop
# service storm-drpc stop
# service storm-ui stop
# service storm-nimbus stop
```


## Caution
In case this installer uses, worker's log name becomes below format.
```
[TopologyID]-worker-[port].log
```

So, Storm-UI Component summary screen's port link is disabled.
If you want to use port link, execute below command and modify log setting.
```
# vi /opt/apache-storm/logback/cluster.xml
```

storm-installer initial:
```
<configuration scan="true" scanPeriod="60 seconds">
 <appender name="A1" class="ch.qos.logback.core.rolling.RollingFileAppender">
    <file>${storm.log.dir}/${storm.id:-storm}-${logfile.name}</file>
    <rollingPolicy class="ch.qos.logback.core.rolling.FixedWindowRollingPolicy">
      <fileNamePattern>${storm.log.dir}/${storm.id:-storm}-${logfile.name}.%i</fileNamePattern>
      <minIndex>1</minIndex>
      <maxIndex>9</maxIndex>
    </rollingPolicy>
```

modify after:
```
<configuration scan="true" scanPeriod="60 seconds">
 <appender name="A1" class="ch.qos.logback.core.rolling.RollingFileAppender">
    <file>${storm.log.dir}/${logfile.name}</file>
    <rollingPolicy class="ch.qos.logback.core.rolling.FixedWindowRollingPolicy">
      <fileNamePattern>${storm.log.dir}/${logfile.name}.%i</fileNamePattern>
      <minIndex>1</minIndex>
      <maxIndex>9</maxIndex>
    </rollingPolicy>
```


## Dependency libraries

Project    : Aache-Storm
Version    : 1.0.2
Lisence    : Apache License Version 2.0
Source URL : https://storm.apache.org/


## License
This software is released under the MIT License, see LICENSE.txt.

