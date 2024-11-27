# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server import util


class ResponseArchivos(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    def __init__(self, status: int=None, file_name: str=None, mesage: str=None, internal_transaction_id: str=None, external_transaction_id: str=None):  # noqa: E501
        """ResponseArchivos - a model defined in Swagger

        :param status: The status of this ResponseArchivos.  # noqa: E501
        :type status: int
        :param file_name: The file_name of this ResponseArchivos.  # noqa: E501
        :type file_name: str
        :param mesage: The mesage of this ResponseArchivos.  # noqa: E501
        :type mesage: str
        :param internal_transaction_id: The internal_transaction_id of this ResponseArchivos.  # noqa: E501
        :type internal_transaction_id: str
        :param external_transaction_id: The external_transaction_id of this ResponseArchivos.  # noqa: E501
        :type external_transaction_id: str
        """
        self.swagger_types = {
            'status': int,
            'file_name': str,
            'mesage': str,
            'internal_transaction_id': str,
            'external_transaction_id': str
        }

        self.attribute_map = {
            'status': 'status',
            'file_name': 'file_name',
            'mesage': 'mesage',
            'internal_transaction_id': 'internalTransactionId',
            'external_transaction_id': 'externalTransactionId'
        }
        self._status = status
        self._file_name = file_name
        self._mesage = mesage
        self._internal_transaction_id = internal_transaction_id
        self._external_transaction_id = external_transaction_id

    @classmethod
    def from_dict(cls, dikt) -> 'ResponseArchivos':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The Response_Archivos of this ResponseArchivos.  # noqa: E501
        :rtype: ResponseArchivos
        """
        return util.deserialize_model(dikt, cls)

    @property
    def status(self) -> int:
        """Gets the status of this ResponseArchivos.


        :return: The status of this ResponseArchivos.
        :rtype: int
        """
        return self._status

    @status.setter
    def status(self, status: int):
        """Sets the status of this ResponseArchivos.


        :param status: The status of this ResponseArchivos.
        :type status: int
        """
        allowed_values = ["200", "400"]  # noqa: E501
        if status not in allowed_values:
            raise ValueError(
                "Invalid value for `status` ({0}), must be one of {1}"
                .format(status, allowed_values)
            )

        self._status = status

    @property
    def file_name(self) -> str:
        """Gets the file_name of this ResponseArchivos.


        :return: The file_name of this ResponseArchivos.
        :rtype: str
        """
        return self._file_name

    @file_name.setter
    def file_name(self, file_name: str):
        """Sets the file_name of this ResponseArchivos.


        :param file_name: The file_name of this ResponseArchivos.
        :type file_name: str
        """

        self._file_name = file_name

    @property
    def mesage(self) -> str:
        """Gets the mesage of this ResponseArchivos.


        :return: The mesage of this ResponseArchivos.
        :rtype: str
        """
        return self._mesage

    @mesage.setter
    def mesage(self, mesage: str):
        """Sets the mesage of this ResponseArchivos.


        :param mesage: The mesage of this ResponseArchivos.
        :type mesage: str
        """

        self._mesage = mesage

    @property
    def internal_transaction_id(self) -> str:
        """Gets the internal_transaction_id of this ResponseArchivos.


        :return: The internal_transaction_id of this ResponseArchivos.
        :rtype: str
        """
        return self._internal_transaction_id

    @internal_transaction_id.setter
    def internal_transaction_id(self, internal_transaction_id: str):
        """Sets the internal_transaction_id of this ResponseArchivos.


        :param internal_transaction_id: The internal_transaction_id of this ResponseArchivos.
        :type internal_transaction_id: str
        """

        self._internal_transaction_id = internal_transaction_id

    @property
    def external_transaction_id(self) -> str:
        """Gets the external_transaction_id of this ResponseArchivos.


        :return: The external_transaction_id of this ResponseArchivos.
        :rtype: str
        """
        return self._external_transaction_id

    @external_transaction_id.setter
    def external_transaction_id(self, external_transaction_id: str):
        """Sets the external_transaction_id of this ResponseArchivos.


        :param external_transaction_id: The external_transaction_id of this ResponseArchivos.
        :type external_transaction_id: str
        """

        self._external_transaction_id = external_transaction_id
