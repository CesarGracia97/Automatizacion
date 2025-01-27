import connexion
import six

from swagger_server.models.e_archivos400 import EArchivos400  # noqa: E501
from swagger_server.models.response_archivos import ResponseArchivos  # noqa: E501
from swagger_server import util


def patch_transaccion_proveedores(external_transaction_id=None, channel=None, archivo=None):  # noqa: E501
    """patch_transaccion_proveedores

    Procesos de Modificaciones de Registro de Proveedores # noqa: E501

    :param external_transaction_id: 
    :type external_transaction_id: str
    :param channel: 
    :type channel: str
    :param archivo: 
    :type archivo: List[strstr]

    :rtype: ResponseArchivos
    """
    return 'do some magic!'
