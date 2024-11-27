import connexion
import requests
from flask import jsonify

from swagger_server.models import RequestArchivos, ResponseError
from swagger_server.models.e_archivos400 import EArchivos400  # noqa: E501
from swagger_server.models.response_archivos import ResponseArchivos  # noqa: E501
from swagger_server.uses_cases.valid_methods import ValidationMethods
from swagger_server.utils.transactions.transaction import TransactionId


def get_archivos_carga(body = None):  # noqa: E501
    """get_archivos_carga"""
    ext_validas = [".xlsx", ".xls", ".csv"]
    mime_validos = ["application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",  # .xlsx
        "application/vnd.ms-excel",  # .xls
        "text/csv",  # .csv
    ]
    internal = TransactionId()
    body = RequestArchivos.from_dict(connexion.request.form)
    archivos = connexion.request.files.getlist("archivo")
    narchivos = []
    try:
        if body.channel == 'automatic-contrato-web':
            for archivo in archivos:
                if any(archivo.filename.endswith(ext) for ext in ext_validas):
                    if archivo.content_type in mime_validos:
                        narchivos.append(archivo.filename)
                    else:
                        response = ResponseArchivos(
                            status=400,
                            external_transaction_id=body.external_transaction_id,
                            internal_transaction_id=internal.generate_internal_transaction_id(),
                            file_name=archivo.filename,
                            mesage=f'Tipo MIME inválido. Solo se permiten tipos {mime_validos}'
                        )
                        return jsonify(response), 400
                else:
                    response = ResponseArchivos(
                        status=400,
                        external_transaction_id=body.external_transaction_id,
                        internal_transaction_id=internal.generate_internal_transaction_id(),
                        file_name=archivo.filename,
                        mesage=f'Archivo con Extension no valida, solo se permiten {ext_validas}'
                    )
                    return jsonify(response), 400
            validacion = ValidationMethods.valid_formatte(archivos, internal.generate_internal_transaction_id(), body.external_transaction_id)
            if validacion:
                print("funciono")
            else:
                # Si `valid_formatte` retorna un error, enviarlo
                return jsonify(validacion), validacion["status"]

        else:
            response = ResponseError(
                error_code= -1,
                external_transaction_id=body.external_transaction_id,
                internal_transaction_id=internal.generate_internal_transaction_id(),
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
            internal_transaction_id=internal.generate_internal_transaction_id(),
            message=http_err.response.text,
        )
        return jsonify(response), http_err.response.status_code
