# coding=utf-8
import unittest
import pytest
import json
import os
from .helpers.libvirt_helpers import dict_to_libvirt_obj


__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))


class MockLibvirt:
    """
    Mock libvirt client
    """
    def listAllDomains(self):
        with open(os.path.join(__location__, 'data/domains.json')) as f:
            return json.load(f, object_hook=dict_to_libvirt_obj)


@pytest.mark.usefixtures("client")
class TestDomain(unittest.TestCase):
    libvirt_client = MockLibvirt()

    def test_list_domains(self):
        response = self.client.get('/api/domain')
        self.assertEqual(response.status, '200 OK')

        data = json.loads(response.data)

        self.assertListEqual(data, [
            {'id': 0, 'isActive': 1, 'name': 'Test domain 1',
             'uuid': 'a110ff96-be94-4537-b181-87b018f3ce1b'},
            {'id': 1, 'isActive': 2, 'name': 'Test domain 2',
             'uuid': '078595d8-aa41-45de-a58a-e21f18c7f91c'},
        ])

