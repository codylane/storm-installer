import pytest
import testinfra
import socket

backend = testinfra.get_backend('local://')

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

@pytest.fixture()
def run_local_command():
    Command = backend.get_module('Command')
    return Command

@pytest.fixture()
def package():
    pkg = backend.get_module('Package')
    return pkg

@pytest.fixture()
def File():
    f = backend.get_module('File')
    return f
