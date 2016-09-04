%define pkg_name     apache-storm
%define pkg_version  1.0.2
%define pkg_release  1
%define pkg_name_ver %{pkg_name}-%{pkg_version}
%define pkg_root_dir /opt/%{pkg_name}
%define _currentdir  %(pwd)

Name: %{pkg_name}
Version: %{pkg_version}
Release: %{pkg_release}%{?dist}
Summary: Storm Complex Event Processing
Group: Applications/Internet
License: Apache License Version 2.0
URL: https://storm.apache.org/
Source: http://www.apache.org/dyn/closer.cgi/storm/%{pkg_name_ver}/%{pkg_name_ver}.tar.gz
BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
Requires(pre): shadow-utils
Requires(pre): java == 1:1.7.0
%description
Storm is a distributed realtime computation system.
Similar to how Hadoop provides a set of general primitives for doing batch processing,
Storm provides a set of general primitives for doing realtime computation. Storm is simple,
can be used with any programming language, is used by many companies, and is a lot of fun to use!

The Rationale page on the wiki explains what Storm is and why it was built.
This presentation is also a good introduction to the project.

Storm has a website at storm-project.net.

%pre
getent group storm >/dev/null || groupadd -r storm
getent passwd storm >/dev/null || \
    useradd -r -g storm -d %{pkg_root_dir} -s /sbin/nologin \
    -c "Storm Service" storm
exit 0

%prep
%setup -q

# This SPEC build is Only Packaging.
%build

%install
# Copy the storm file to the right places
%{__mkdir_p} %{buildroot}%{pkg_root_dir}
%{__mkdir_p} %{buildroot}/var%{pkg_root_dir}
%{__cp} -R * %{buildroot}%{pkg_root_dir}/

# Copy the storm init files to the right places
%{__mkdir_p} %{buildroot}%{_sysconfdir}/sysconfig
%{__mkdir_p} %{buildroot}%{_initddir}/
%{__mkdir_p} %{buildroot}%{_localstatedir}/run/storm

%{__cp} %{_currentdir}/sysconfig/storm %{buildroot}%{_sysconfdir}/sysconfig/storm
%{__cp} %{_currentdir}/init.d/* %{buildroot}%{_initddir}/
%{__chmod} +x  %{buildroot}%{_initddir}/*

#update default config
echo "nimbus.host: \"localhost\"" >> %{buildroot}%{pkg_root_dir}/conf/storm.yaml
echo "" >> %{buildroot}%{pkg_root_dir}/conf/storm.yaml
echo "storm.zookeeper.servers:" >> %{buildroot}%{pkg_root_dir}/conf/storm.yaml
echo "     - \"localhost\"" >> %{buildroot}%{pkg_root_dir}/conf/storm.yaml
echo "" >> %{buildroot}%{pkg_root_dir}/conf/storm.yaml
echo "storm.local.dir: \"%{pkg_root_dir}\"" >> %{buildroot}%{pkg_root_dir}/conf/storm.yaml

#update logging config
sed -i -e 's/${logfile\.name}/${storm.id:-storm}-${logfile.name}/g' %{buildroot}%{pkg_root_dir}/log4j2/cluster.xml

# remove pesky pyc or pyo from rpm
find %{buildroot} -name '*.py?' -type f | xargs rm -f

%clean
[ "%{buildroot}" != "/" ] && %{__rm} -rf %{buildroot}
%{__rm} -rf %{buildroot}%{pkg_root_dir}

%files
%defattr(-,root,root)
%attr(0755,root,root) /etc/rc.d/init.d/storm-*
%attr(0644,root,root) %config(noreplace) /etc/sysconfig/storm
/var/run/storm
%defattr(-,storm,storm)
%{pkg_root_dir}/CHANGELOG.md
%{pkg_root_dir}/LICENSE
%{pkg_root_dir}/NOTICE
%{pkg_root_dir}/README.markdown
%{pkg_root_dir}/RELEASE
%{pkg_root_dir}/SECURITY.md
%{pkg_root_dir}/bin
%{pkg_root_dir}/conf
%{pkg_root_dir}/examples
%{pkg_root_dir}/external
%{pkg_root_dir}/lib
%{pkg_root_dir}/log4j2
%{pkg_root_dir}/public


%post
chown -R storm:storm %{pkg_root_dir}
chmod -R 755 %{pkg_root_dir}/bin/*
exit 0

%preun
if [ "$1" = "0" ]; then
    /sbin/service storm-ui stop
    /sbin/service storm-nimbus stop
    /sbin/service storm-supervisor stop
    /sbin/service storm-drpc stop
    /sbin/service storm-logviewer stop
    /sbin/chkconfig storm-ui off
    /sbin/chkconfig storm-nimbus off
    /sbin/chkconfig storm-supervisor off
    /sbin/chkconfig storm-drpc off
    /sbin/chkconfig storm-logviewer off
fi
exit 0

%postun
rmdir %{pkg_root_dir}
exit 0

%changelog
* Sat Sep 03 2016 Cody Lane
- Apache-Storm 1.0.2 Packaging

* Tue Nov 30 2014 Acroquest Technology
- Apache-Storm 0.9.3 Packaging

* Tue Jul 09 2014 Acroquest Technology
- Apache-Storm 0.9.2-incubating Packaging

* Tue Apr 08 2014 Acroquest Technology
- Apache-Storm 0.9.1-incubating Packaging

* Mon Dec 05 2013 Acroquest Technology
- Storm-0.9.0 Packaging

* Mon Dec 02 2013 Acroquest Technology
- Storm-0.9.0-rc3 Packaging

* Mon Nov 11 2013 Acroquest Technology
- Storm-0.9.0-rc2 Packaging

* Tue Mar 16 2013 spudone
- Fixed to run Storm under a non-root account
- Fixed uninstall cleanup

* Thu Feb 07 2013 Acroquest Technology
- Storm-0.8.2 Packaging

* Tue Oct 14 2012 Acroquest Technology
- Initial Packaging


