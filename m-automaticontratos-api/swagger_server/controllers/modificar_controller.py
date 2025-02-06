import connexion
import requests
import six
from flask import jsonify

from swagger_server.models import ResponseError
from swagger_server.models.e_archivos400 import EArchivos400  # noqa: E501
from swagger_server.models.request_modify_suspendidos import RequestModifySuspendidos  # noqa: E501
from swagger_server.models.response_archivos import ResponseArchivos  # noqa: E501
from swagger_server.uses_cases.db_insert_methods import DB_Insert_Methods
from swagger_server.uses_cases.db_update_methods import DB_Update_Method
from swagger_server.utils.transactions.transaction import TransactionId
from loguru import logger


def put_suspendidos(body=None):  # noqa: E501
    """ put_suspendidos Procesos de Modificaciones de Registro de Proveedores # noqa: E501 """
    internal = TransactionId()
    internal_transaction_id: str = internal.generate_internal_transaction_id()
    if connexion.request.is_json:
        body = RequestModifySuspendidos.from_dict(connexion.request.get_json())  # noqa: E501
        logger.info(f"put_suspendidos", internal=internal_transaction_id, external=body.external_transaction_id)
        try:
            if body.channel == 'automatic-contrato-web':
                db = DB_Update_Method()
                update = db.update_data_suspendidos(body.proceso)
                update['externalTransactionId'] = body.external_transaction_id
                update['internalTransactionId'] = internal_transaction_id
                return jsonify(update), update["status"]

            else:
                response = ResponseError(
                    error_code=-1,
                    external_transaction_id=body.external_transaction_id,
                    internal_transaction_id=internal_transaction_id,
                    message='unsupported channel',
                )
                return jsonify(response), 400
        except requests.exceptions.HTTPError as http_err:
            response = ResponseError(
                error_code=http_err.response.status_code,
                message=http_err.response.text,
                external_transaction_id=internal_transaction_id,
                internal_transaction_id=internal_transaction_id
            )
            return jsonify(response), 400

    return 'do some magic!'
