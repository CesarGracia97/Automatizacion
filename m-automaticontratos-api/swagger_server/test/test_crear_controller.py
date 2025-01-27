# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.e_archivos400 import EArchivos400  # noqa: E501
from swagger_server.models.request_archivos import RequestArchivos  # noqa: E501
from swagger_server.models.response_archivos import ResponseArchivos  # noqa: E501
from swagger_server.test import BaseTestCase


class TestCrearController(BaseTestCase):
    """CrearController integration test stubs"""

    def test_post_create_campanas(self):
        """Test case for post_create_campanas

        
        """
        body = RequestArchivos()
        response = self.client.open(
            '/post/create/campanas',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_post_create_procesos(self):
        """Test case for post_create_procesos

        
        """
        body = RequestArchivos()
        response = self.client.open(
            '/post/create/procesos',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
