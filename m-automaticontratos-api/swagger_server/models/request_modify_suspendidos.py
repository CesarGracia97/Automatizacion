# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server.models.m_cliente_suspendido import MClienteSuspendido  # noqa: F401,E501
from swagger_server import util


class RequestModifySuspendidos(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    def __init__(self, external_transaction_id: str=None, channel: str=None, proceso: MClienteSuspendido=None):  # noqa: E501
        """RequestModifySuspendidos - a model defined in Swagger

        :param external_transaction_id: The external_transaction_id of this RequestModifySuspendidos.  # noqa: E501
        :type external_transaction_id: str
        :param channel: The channel of this RequestModifySuspendidos.  # noqa: E501
        :type channel: str
        :param proceso: The proceso of this RequestModifySuspendidos.  # noqa: E501
        :type proceso: MClienteSuspendido
        """
        self.swagger_types = {
            'external_transaction_id': str,
            'channel': str,
            'proceso': MClienteSuspendido
        }

        self.attribute_map = {
            'external_transaction_id': 'externalTransactionId',
            'channel': 'channel',
            'proceso': 'proceso'
        }
        self._external_transaction_id = external_transaction_id
        self._channel = channel
        self._proceso = proceso

    @classmethod
    def from_dict(cls, dikt) -> 'RequestModifySuspendidos':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The RequestModifySuspendidos of this RequestModifySuspendidos.  # noqa: E501
        :rtype: RequestModifySuspendidos
        """
        return util.deserialize_model(dikt, cls)

    @property
    def external_transaction_id(self) -> str:
        """Gets the external_transaction_id of this RequestModifySuspendidos.


        :return: The external_transaction_id of this RequestModifySuspendidos.
        :rtype: str
        """
        return self._external_transaction_id

    @external_transaction_id.setter
    def external_transaction_id(self, external_transaction_id: str):
        """Sets the external_transaction_id of this RequestModifySuspendidos.


        :param external_transaction_id: The external_transaction_id of this RequestModifySuspendidos.
        :type external_transaction_id: str
        """
        if external_transaction_id is None:
            raise ValueError("Invalid value for `external_transaction_id`, must not be `None`")  # noqa: E501

        self._external_transaction_id = external_transaction_id

    @property
    def channel(self) -> str:
        """Gets the channel of this RequestModifySuspendidos.


        :return: The channel of this RequestModifySuspendidos.
        :rtype: str
        """
        return self._channel

    @channel.setter
    def channel(self, channel: str):
        """Sets the channel of this RequestModifySuspendidos.


        :param channel: The channel of this RequestModifySuspendidos.
        :type channel: str
        """
        if channel is None:
            raise ValueError("Invalid value for `channel`, must not be `None`")  # noqa: E501

        self._channel = channel

    @property
    def proceso(self) -> MClienteSuspendido:
        """Gets the proceso of this RequestModifySuspendidos.


        :return: The proceso of this RequestModifySuspendidos.
        :rtype: MClienteSuspendido
        """
        return self._proceso

    @proceso.setter
    def proceso(self, proceso: MClienteSuspendido):
        """Sets the proceso of this RequestModifySuspendidos.


        :param proceso: The proceso of this RequestModifySuspendidos.
        :type proceso: MClienteSuspendido
        """

        self._proceso = proceso
