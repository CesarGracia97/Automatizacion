# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.e_archivos400 import EArchivos400  # noqa: E501
from swagger_server.models.response_archivos import ResponseArchivos  # noqa: E501
from swagger_server.test import BaseTestCase


class TestArchivosController(BaseTestCase):
    """ArchivosController integration test stubs"""

    def test_get_archivos_carga(self):
        """Test case for get_archivos_carga

        
        """
        data = dict(external_transaction_id='external_transaction_id_example',
                    channel='channel_example',
                    archivo='archivo_example')
        response = self.client.open(
            '/get/archivos/carga',
            method='POST',
            data=data,
            content_type='multipart/form-data')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
