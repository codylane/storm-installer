import pytest
import testinfra
import time

def assert_service_starts(Start_Service, Stop_Service, Service, name):
    rc = Start_Service(name)
    assert rc == 0

    print('sleeping to make sure service has a chance to startup')
    time.sleep(5)

    svc = Service(name)
    assert svc.is_running


    rc = Stop_Service(name)
    assert rc == 0

    svc = Service(name)
    assert svc.is_running == False

@pytest.mark.parametrize('name', [
    'storm-nimbus',
    'storm-drpc',
    'storm-logviewer',
    'storm-supervisor',
    'storm-ui',
])
def test_service_starts_up(Start_Service, Stop_Service, Service, name):
    assert_service_starts(Start_Service, Stop_Service, Service, name)
