import pytest
import testinfra

def test_uninstall_rpm(Command):
  cmd = Command('yum remove -y apache-storm')

@pytest.mark.parametrize('name', [
  'apache-storm',
])
def test_packages_should_not_be_installed(Package, name):
    p = Package(name)
    assert p.is_installed == False

def test_opt_apache_storm_does_not_exist(File):
    f = File('/opt/apache-storm')
    assert f.exists == False
    assert f.is_directory == False

def test_etc_sysconfig_storm_does_not_exists(File):
    f = File('/etc/sysconfig/storm')
    assert f.exists == False

@pytest.mark.parametrize('name', [
    'storm-nimbus',
    'storm-drpc',
    'storm-logviewer',
    'storm-supervisor',
    'storm-ui',
])
def test_etc_initd_scripts_do_not_exist(File, name):
    f = File('/etc/init.d/{0}'.format(name))
    assert f.exists == False

def test_var_run_storm_does_not_exist(File):
    f = File('/var/run/storm')
    assert f.exists == False

def test_var_log_apache_storm_does_not_exist(File):
    f = File('/var/log/apache-storm')
    assert f.exists == False

@pytest.mark.parametrize('name', [
    'storm-nimbus',
    'storm-drpc',
    'storm-logviewer',
    'storm-supervisor',
    'storm-ui',
])
def test_service_is_stopped(Service, name):
    svc = Service(name)
    assert svc.is_running == False
    assert svc.is_enabled == False
