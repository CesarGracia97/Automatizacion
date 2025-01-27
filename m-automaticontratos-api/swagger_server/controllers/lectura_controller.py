import connexion
import requests
import six
from flask import jsonify

from swagger_server.models import ResponseError
from swagger_server.models.e_archivos400 import EArchivos400  # noqa: E501
from swagger_server.models.request_lectura import RequestLectura  # noqa: E501
from swagger_server.models.response_archivos import ResponseArchivos  # noqa: E501
from swagger_server import util
from swagger_server.uses_cases.db_insert_methods import DB_Insert_Methods
from swagger_server.uses_cases.db_queries_methods import DB_Queries_Methods
from swagger_server.utils.transactions.transaction import TransactionId
from loguru import logger


def get_read(body=None):  # noqa: E501
    """get_read Endpoint de Lectura de Datos # noqa: E501 """
    internal = TransactionId()
    internal_transaction_id: str = internal.generate_internal_transaction_id()

    if connexion.request.is_json:
        body = RequestLectura.from_dict(connexion.request.get_json())  # noqa: E501
        logger.info(f"post_upload_archivoscobros", internal=internal_transaction_id, external=body.external_transaction_id)
        try:
            if body.channel == 'automatic-contrato-web':
                if body.peticion == 'suplantacion':
                    db = DB_Queries_Methods()
                    date_update = db.query_last_update()
                    date_update['externalTransactionId'] = body.external_transaction_id
                    date_update['internalTransactionId'] = internal_transaction_id
                    return jsonify(date_update), date_update["status"]
                elif body.peticion == 'meses-disponibles':
                    db = DB_Queries_Methods()
                    meses = db.query_meses_disponible()
                    meses['externalTransactionId'] = body.external_transaction_id
                    meses['internalTransactionId'] = internal_transaction_id
                    return jsonify(meses), meses["status"]
                elif body.peticion == 'procesos':
                    db = DB_Queries_Methods()
                    procesos = db.query_procesos_disponibles()
                    procesos['externalTransactionId'] = body.external_transaction_id
                    procesos['internalTransactionId'] = internal_transaction_id
                    return jsonify(procesos), procesos["status"]
                else:
                    response = ResponseError(
                        error_code=-2,
                        external_transaction_id=body.external_transaction_id,
                        internal_transaction_id=internal_transaction_id,
                        message='unsupported peticion',
                    )
                    return jsonify(response), 400
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
