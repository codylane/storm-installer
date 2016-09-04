import pytest
import testinfra

@pytest.mark.parametrize('name', [
    ('~/rpmbuild/RPMS/x86_64/apache-storm-1.0.2-1.el6.x86_64.rpm'),
])
def test_install_rpm(Command, Package, name):
    '''
    It should install the apache-storm RPM without errors
    '''
    # ~/rpmbuild/RPMS/x86_64/apache-storm-1.0.2-1.el6.x86_64.rpm
    yum_install = Command('yum install -y {0}'.format(name))

    pkg = Package('apache-storm')
    assert pkg.is_installed

def test_opt_apache_storm_exists(File):
    f = File('/opt/apache-storm')
    assert f.exists
    assert f.is_directory
    assert f.user == 'storm'
    assert f.group == 'storm'
    assert f.mode == 0755

def test_etc_sysconfig_strom_exists(File):
    f = File('/etc/sysconfig/storm')
    assert f.is_file
    assert f.exists
    assert f.user == 'root'
    assert f.group == 'root'
    assert f.mode  == 0644

@pytest.mark.parametrize('name', [
    'storm-nimbus',
    'storm-ui',
    'storm-supervisor',
    'storm-logviewer',
    'storm-drpc',
])
def test_etc_initd_scripts_exist(File, name):
    f = File('/etc/init.d/{0}'.format(name))
    assert f.is_file
    assert f.exists
    assert f.mode == 0755
    assert f.user == 'root'
    assert f.group == 'root'

def test_var_log_apache_storm_exists(File):
    f = File('/var/log/apache-storm')
    assert f.is_symlink
    assert f.linked_to == '/opt/apache-storm/logs'

def test_var_run_storm_exists(File):
    f = File('/var/run/storm')
    assert f.is_directory
    assert f.user == 'storm'
    assert f.group == 'storm'
    assert f.mode == 0755

@pytest.mark.parametrize('name', [
    'flight.bash',
    'storm',
    'storm.cmd',
    'storm-config.cmd',
    'storm.py',
])
def test_opt_apache_storm_bin_scripts_exists(File, name):
    f = File('/opt/apache-storm/bin/{0}'.format(name))
    assert f.is_file
    assert f.exists
    assert f.mode == 0755
    assert f.user == 'storm'
    assert f.group == 'storm'
