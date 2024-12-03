import connexion
import requests
from flask import jsonify

from swagger_server.models import RequestArchivos, ResponseError
from swagger_server.models.e_archivos400 import EArchivos400  # noqa: E501
from swagger_server.models.response_archivos import ResponseArchivos  # noqa: E501
from swagger_server.uses_cases.files_methods import FilesMethods
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
                            internal_transaction_id=internal.generate_internal_transaction_id(),
                            file_name=file.filename,
                            mesage=f'Tipo MIME inválido. Solo se permiten tipos {mime_validos}'
                        )
                        return jsonify(response), 400
                else:
                    response = ResponseArchivos(
                        status=400,
                        external_transaction_id=body.external_transaction_id,
                        internal_transaction_id=internal.generate_internal_transaction_id(),
                        file_name=file.filename,
                        mesage=f'Archivo con Extension no valida, solo se permiten {ext_validas}'
                    )
                    return jsonify(response), 400
            validation_1 = ValidationMethods.valid_formatte(files)

            if validation_1 is True:
                validation_2 = ValidationMethods.valid_ci(files)
                # new_file = FilesMethods.fusion_files(files)
            else:
                validation_1['external_transaction_id'] = body.external_transaction_id
                validation_1['internal_transaction_id'] = internal.generate_internal_transaction_id()
                return jsonify(validation_1), validation_1["status"]

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
