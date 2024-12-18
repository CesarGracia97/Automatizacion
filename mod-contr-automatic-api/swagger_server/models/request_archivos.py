# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server import util


class RequestArchivos(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    def __init__(self, external_transaction_id: str=None, channel: str=None, archivo: List[str]=None):  # noqa: E501
        """RequestArchivos - a model defined in Swagger

        :param external_transaction_id: The external_transaction_id of this RequestArchivos.  # noqa: E501
        :type external_transaction_id: str
        :param channel: The channel of this RequestArchivos.  # noqa: E501
        :type channel: str
        :param archivo: The archivo of this RequestArchivos.  # noqa: E501
        :type archivo: List[str]
        """
        self.swagger_types = {
            'external_transaction_id': str,
            'channel': str,
            'archivo': List[str]
        }

        self.attribute_map = {
            'external_transaction_id': 'externalTransactionId',
            'channel': 'channel',
            'archivo': 'archivo'
        }
        self._external_transaction_id = external_transaction_id
        self._channel = channel
        self._archivo = archivo

    @classmethod
    def from_dict(cls, dikt) -> 'RequestArchivos':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The RequestArchivos of this RequestArchivos.  # noqa: E501
        :rtype: RequestArchivos
        """
        return util.deserialize_model(dikt, cls)

    @property
    def external_transaction_id(self) -> str:
        """Gets the external_transaction_id of this RequestArchivos.


        :return: The external_transaction_id of this RequestArchivos.
        :rtype: str
        """
        return self._external_transaction_id

    @external_transaction_id.setter
    def external_transaction_id(self, external_transaction_id: str):
        """Sets the external_transaction_id of this RequestArchivos.


        :param external_transaction_id: The external_transaction_id of this RequestArchivos.
        :type external_transaction_id: str
        """
        if external_transaction_id is None:
            raise ValueError("Invalid value for `external_transaction_id`, must not be `None`")  # noqa: E501

        self._external_transaction_id = external_transaction_id

    @property
    def channel(self) -> str:
        """Gets the channel of this RequestArchivos.


        :return: The channel of this RequestArchivos.
        :rtype: str
        """
        return self._channel

    @channel.setter
    def channel(self, channel: str):
        """Sets the channel of this RequestArchivos.


        :param channel: The channel of this RequestArchivos.
        :type channel: str
        """
        if channel is None:
            raise ValueError("Invalid value for `channel`, must not be `None`")  # noqa: E501

        self._channel = channel

    @property
    def archivo(self) -> List[str]:
        """Gets the archivo of this RequestArchivos.

        Archivos en formato Excel o CSV  # noqa: E501

        :return: The archivo of this RequestArchivos.
        :rtype: List[str]
        """
        return self._archivo

    @archivo.setter
    def archivo(self, archivo: List[str]):
        """Sets the archivo of this RequestArchivos.

        Archivos en formato Excel o CSV  # noqa: E501

        :param archivo: The archivo of this RequestArchivos.
        :type archivo: List[str]
        """
        if archivo is None:
            raise ValueError("Invalid value for `archivo`, must not be `None`")  # noqa: E501

        self._archivo = archivo
