import pytest
import testinfra
import socket

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
