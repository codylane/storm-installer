FROM centos:6

RUN yum install -y \
    epel-release \
    https://archive.cloudera.com/cdh5/one-click-install/redhat/6/x86_64/cloudera-cdh-5-0.x86_64.rpm

RUN yum install -y \
      curl \
      rpm-build \
      rpmdevtools \
      git \
      autoconf \
      automake \
      make \
      gcc-c++ \
      libuuid-devel \
      glib2-devel \
      xmlto \
      asciidoc \
      python \
      python-devel \
      openssl-devel \
      libffi-devel \
      python-pip \
      python-virtualenvwrapper \
      python-virtualenv \
      readline-devel \
      bzip2-devel \
      sqlite-devel \
      createrepo

RUN mkdir -p /builds && \
    rpmdev-setuptree

# /start-web.sh
RUN echo '#!/bin/bash' > /start-web.sh && \
    echo >> /start-web.sh && \
    echo 'cd /RPMS; python -m SimpleHTTPServer 8080' >> /start-web.sh && \
    chmod 755 /start-web.sh

COPY builds /builds

RUN tar zxvf /builds/apache-storm-build.tar.gz -C /builds && \
    cp /builds/apache-storm-build/apache-storm-*.tar.gz ~/rpmbuild/SOURCES/ && \
    chown $(whoami) -R /builds

# build the RPM
RUN cd /builds/apache-storm-build/storm-installer && \
    rpmbuild -ba apache-storm.spec

RUN cd ~/rpmbuild && \
    mkdir -p /RPMS/RedHat/6 && \
    rsync -av RPMS/ /RPMS/RedHat/6/ && \
    rsync -av SRPMS /RPMS/RedHat/6/ && \
    createrepo /RPMS/RedHat/6/x86_64 && \
    createrepo /RPMS/RedHat/6/SRPMS && \
    echo '[storm-rpm]' > /etc/yum.repos.d/storm-rpm.repo && \
    echo 'name=storm-rpm repo' >> /etc/yum.repos.d/storm-rpm.repo && \
    echo 'baseurl=file:///RPMS/RedHat/6/x86_64' >> /etc/yum.repos.d/storm-rpm.repo && \
    echo 'enabled=1' >> /etc/yum.repos.d/storm-rpm.repo && \
    echo 'gpgcheck=0' >> /etc/yum.repos.d/storm-rpm.repo

# setup a virtualenv that will be used for installing testing utilities
RUN echo '. /usr/bin/virtualenvwrapper.sh' > /etc/profile.d/virtualenvwrapper.sh
RUN . /etc/profile.d/virtualenvwrapper.sh && \
    mkvirtualenv rpmbuild && \
    cd /builds/apache-storm-build/storm-installer && \
    setvirtualenvproject && \
    pip install --upgrade pip
RUN . /etc/profile.d/virtualenvwrapper.sh && \
    workon rpmbuild && \
    pip install argparse \
        paramiko \
        testinfra

# Run our integration tests to make sure the RPM works
RUN . /etc/profile.d/virtualenvwrapper.sh && \
    workon rpmbuild && \
    yum clean expire-cache && \
    testinfra -vs tests/test_install.py && \
    testinfra -vs tests/test_service.py && \
    testinfra -vs tests/test_uninstall.py

EXPOSE 8080

CMD ["/bin/bash", "-c", "/start-web.sh"]
