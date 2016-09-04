import pytest
import testinfra

@pytest.mark.parametrize('name', [
    'storm-nimbus',
    'storm-drpc',
    'storm-logviewer',
    'storm-supervisor',
    'storm-ui',
])
def test_service_starts_up(LocalCommand, Service, name):
    svc = Service(name)
    assert svc.is_running
