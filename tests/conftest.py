# coding=utf-8
import pytest
from pyvirt import create_app


@pytest.fixture()
def client(mocker, request):
    mocker.patch('libvirt.openReadOnly', return_value=getattr(request.cls, 'libvirt_client'))
    app, _ = create_app('testing')

    def teardown():
        pass

    request.addfinalizer(teardown)
    request.cls.client = app.test_client()
