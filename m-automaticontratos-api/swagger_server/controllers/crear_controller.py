import connexion
import requests
from flask import jsonify

from swagger_server.models import ResponseError, RequestCreateProcess
from swagger_server.models.request_archivos import RequestArchivos  # noqa: E501
from swagger_server.models.request_create_campana import RequestCreateCampana  # noqa: E501
from swagger_server.uses_cases.db_insert_methods import DB_Insert_Methods
from swagger_server.utils.transactions.transaction import TransactionId
from loguru import logger


def post_create_campanas(body=None):  # noqa: E501
    """post_create_campanas Procesos de Creacion de Campañas # noqa: E501 """
    internal = TransactionId()
    internal_transaction_id: str = internal.generate_internal_transaction_id()
    if connexion.request.is_json:
        body = RequestCreateCampana.from_dict(connexion.request.get_json())  # noqa: E501
        logger.info(f"post_upload_archivoscobros", internal=internal_transaction_id, external=body.external_transaction_id)
        try:
            if body.channel == 'automatic-contrato-web':
                db = DB_Insert_Methods()
                campana = db.insert_data_campana_create(body.campana, body.idproceso)
                campana['externalTransactionId'] = body.external_transaction_id
                campana['internalTransactionId'] = internal_transaction_id
                return jsonify(campana), campana["status"]
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




def post_create_procesos(body=None):  # noqa: E501
    """post_create_procesos Procesos de Creacion de Proceso # noqa: E501 """
    internal = TransactionId()
    internal_transaction_id: str = internal.generate_internal_transaction_id()
    if connexion.request.is_json:
        body = RequestCreateProcess.from_dict(connexion.request.get_json())  # noqa: E501
        logger.info(f"post_create_procesos", internal=internal_transaction_id, external=body.external_transaction_id)
        try:
            if body.channel == 'automatic-contrato-web':
                db = DB_Insert_Methods
                responses = db.insert_data_proceso_create(body.proceso)
                responses['externalTransactionId'] = body.external_transaction_id
                responses['internalTransactionId'] = internal_transaction_id
                return jsonify(responses), responses["status"]
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
