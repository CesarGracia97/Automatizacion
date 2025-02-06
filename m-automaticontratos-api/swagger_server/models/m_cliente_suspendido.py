# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server import util


class MClienteSuspendido(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    def __init__(self, contrato: float=None, isvalid: str=None):  # noqa: E501
        """MClienteSuspendido - a model defined in Swagger

        :param contrato: The contrato of this MClienteSuspendido.  # noqa: E501
        :type contrato: float
        :param isvalid: The isvalid of this MClienteSuspendido.  # noqa: E501
        :type isvalid: str
        """
        self.swagger_types = {
            'contrato': float,
            'isvalid': str
        }

        self.attribute_map = {
            'contrato': 'contrato',
            'isvalid': 'isvalid'
        }
        self._contrato = contrato
        self._isvalid = isvalid

    @classmethod
    def from_dict(cls, dikt) -> 'MClienteSuspendido':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The M_Cliente_Suspendido of this MClienteSuspendido.  # noqa: E501
        :rtype: MClienteSuspendido
        """
        return util.deserialize_model(dikt, cls)

    @property
    def contrato(self) -> float:
        """Gets the contrato of this MClienteSuspendido.


        :return: The contrato of this MClienteSuspendido.
        :rtype: float
        """
        return self._contrato

    @contrato.setter
    def contrato(self, contrato: float):
        """Sets the contrato of this MClienteSuspendido.


        :param contrato: The contrato of this MClienteSuspendido.
        :type contrato: float
        """
        if contrato is None:
            raise ValueError("Invalid value for `contrato`, must not be `None`")  # noqa: E501

        self._contrato = contrato

    @property
    def isvalid(self) -> str:
        """Gets the isvalid of this MClienteSuspendido.


        :return: The isvalid of this MClienteSuspendido.
        :rtype: str
        """
        return self._isvalid

    @isvalid.setter
    def isvalid(self, isvalid: str):
        """Sets the isvalid of this MClienteSuspendido.


        :param isvalid: The isvalid of this MClienteSuspendido.
        :type isvalid: str
        """
        if isvalid is None:
            raise ValueError("Invalid value for `isvalid`, must not be `None`")  # noqa: E501

        self._isvalid = isvalid
