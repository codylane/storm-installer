import pytest
import testinfra
import socket
import os

backend = testinfra.get_backend('local://', connection='local')

@pytest.fixture()
def get_host_ipaddress(request):
    '''
    Get ipaddress from fqdn
    '''
    def getip(fqdn):
        return socket.gethostbyname(fqdn)
    return getip

@pytest.fixture(scope='module')
def TestinfraBackend(request):
    return backend

def service_status(name):
    return os.system('/sbin/service {0} status'.format(name))

@pytest.fixture()
def Start_Service(request):
    def run(args):
        status_rc = service_status(args)
        if status_rc != 0:
            return os.system('/sbin/service {0} start'.format(args))
        return status_rc
    return run

@pytest.fixture()
def Stop_Service(request):
    def run(args):
        status_rc = service_status(args)
        if status_rc == 0:
            return os.system('/sbin/service {0} stop'.format(args))
        return status_rc
    return run
