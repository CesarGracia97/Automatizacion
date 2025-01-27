import connexion
import requests
import six
from flask import jsonify

from swagger_server.models import RequestArchivos, ResponseError
from swagger_server.models.e_archivos400 import EArchivos400  # noqa: E501
from swagger_server.models.response_archivos import ResponseArchivos  # noqa: E501
from swagger_server import util
from swagger_server.uses_cases.db_insert_methods import DB_Insert_Methods
from swagger_server.uses_cases.format_validation_methods import FormatValidationMethods
from swagger_server.utils.transactions.transaction import TransactionId
from loguru import logger


def post_upload_archivoscobros(body = None):  # noqa: E501
    """post_upload_archivoscobros"""
    ext_validas = [".xlsx", ".xls", ".csv"]
    mime_validos = ["application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", "application/vnd.ms-excel", "text/csv" ]
    internal = TransactionId()
    body = RequestArchivos.from_dict(connexion.request.form)
    files = connexion.request.files.getlist("archivo")
    internal_transaction_id: str = internal.generate_internal_transaction_id()
    logger.info(f"post_upload_archivoscobros", internal=internal_transaction_id, external=body.external_transaction_id)
    n_files = []
    try:
        if body.channel == 'automatic-contrato-web':
            for file in files:
                if any(file.filename.endswith(ext) for ext in ext_validas):
                    if file.content_type in mime_validos:
                        n_files.append(file.filename)
                    else:
                        response = ResponseArchivos(
                            status=400,
                            external_transaction_id=body.external_transaction_id,
                            internal_transaction_id=internal_transaction_id,
                            mesage=f'Tipo MIME inválido. Solo se permiten tipos {mime_validos}'
                        )
                        return jsonify(response), 400
                else:
                    response = ResponseArchivos(
                        status=400,
                        external_transaction_id=body.external_transaction_id,
                        internal_transaction_id=internal_transaction_id,
                        mesage=f'Archivo con Extension no valida, solo se permiten {ext_validas}'
                    )
                    return jsonify(response), 400
            formatte_header = FormatValidationMethods.valid_formatte_header_cobranzas(files)
            if formatte_header is True:
                db_execution = DB_Insert_Methods()
                insert_data =  db_execution.insert_data_cobros_create(files)
                insert_data['external_transaction_id'] = body.external_transaction_id
                insert_data['internal_transaction_id'] = internal_transaction_id
                return jsonify(insert_data), insert_data['status']
            else:
                formatte_header['external_transaction_id'] = body.external_transaction_id
                formatte_header['internal_transaction_id'] = internal_transaction_id
                return jsonify(formatte_header), formatte_header["status"]
        else:
            response = ResponseError(
                error_code=-1,
                external_transaction_id=body.external_transaction_id,
                internal_transaction_id=internal_transaction_id,
                message='unsupported channel',
            )
            return jsonify(response), 400
    except requests.exceptions.HTTPError as http_err:
        print("--------------------------------------------------------------------")
        print("Carga de Archivo| Error detectado")
        print("Canal de Produccion")
        print("Error: ", http_err.response.status_code, http_err.response.text)
        print("--------------------------------------------------------------------")
        response = ResponseError(
            error_code= http_err.response.status_code,
            external_transaction_id=body.external_transaction_id,
            internal_transaction_id=internal_transaction_id,
            message=http_err.response.text,
        )
        return jsonify(response), http_err.response.status_code


def post_upload_archivossuplantacion(body = None):  # noqa: E501
    """post_upload_archivossuplantacion"""
    ext_validas = [".xlsx", ".xls", ".csv"]
    mime_validos = ["application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",  # .xlsx
        "application/vnd.ms-excel",  # .xls
        "text/csv",  # .csv
    ]
    internal = TransactionId()
    internal_transaction_id: str = internal.generate_internal_transaction_id()
    body = RequestArchivos.from_dict(connexion.request.form)
    logger.info(f"post_upload_archivoscobros", internal=internal_transaction_id, external=body.external_transaction_id)
    files = connexion.request.files.getlist("archivo")
    n_files = []
    try:
        if body.channel == 'automatic-contrato-web':
            for file in files:
                if any(file.filename.endswith(ext) for ext in ext_validas):
                    if file.content_type in mime_validos:
                        n_files.append(file.filename)
                    else:
                        response = ResponseArchivos(
                            status=400,
                            external_transaction_id=body.external_transaction_id,
                            internal_transaction_id=internal_transaction_id,
                            mesage=f'Tipo MIME inválido. Solo se permiten tipos {mime_validos}'
                        )
                        return jsonify(response), 400
                else:
                    response = ResponseArchivos(
                        status=400,
                        external_transaction_id=body.external_transaction_id,
                        internal_transaction_id=internal_transaction_id,
                        mesage=f'Archivo con Extension no valida, solo se permiten {ext_validas}'
                    )
                    return jsonify(response), 400
            validation_1 = FormatValidationMethods.valid_formatte_header_suplantacion(files)
            if validation_1 is True:
                consulta = DB_Insert_Methods.insert_data_suplantacion_create(files)
                consulta['external_transaction_id'] = body.external_transaction_id
                consulta['internal_transaction_id'] = internal_transaction_id
                return jsonify(consulta), consulta["status"]
            else:
                validation_1['external_transaction_id'] = body.external_transaction_id
                validation_1['internal_transaction_id'] = internal_transaction_id
                return jsonify(validation_1), validation_1["status"]

        else:
            response = ResponseError(
                error_code=-1,
                external_transaction_id=body.external_transaction_id,
                internal_transaction_id=internal_transaction_id,
                message='unsupported channel',
            )
            return jsonify(response), 400

    except requests.exceptions.HTTPError as http_err:
        print("--------------------------------------------------------------------")
        print("Carga de Archivo| Error detectado")
        print("Canal de Produccion")
        print("Error: ", http_err.response.status_code, http_err.response.text)
        print("--------------------------------------------------------------------")
        response = ResponseError(
            error_code= http_err.response.status_code,
            external_transaction_id=body.external_transaction_id,
            internal_transaction_id=internal_transaction_id,
            message=http_err.response.text,
        )
        return jsonify(response), http_err.response.status_code
