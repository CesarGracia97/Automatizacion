from http.client import responses
from operator import truediv

import pandas as pd
from flask import jsonify

from swagger_server.models import ResponseArchivos, ResponseEVArchivos, ResponseError


class ValidationMethods:
    # Lista de títulos válidos
    FORMATO = [
        "CUENTA TITAN", "Referencia interna", "DOCUMENTO IDENTIFICACION", "NOMBRE DEL CLIENTE", "TELEFONOS", "CIUDAD",
        "ESTADO CUENTA", "TIPO CUENTA", "TIPO DE NEGOCIO", "FORMA DE PAGO", "TRANSACCION", "NOM_TRANSACCION",
        "# FAC PEN CARGA", "# FACTURAS PENDIENTE", "SALDO ORIGINAL VENC", "GESTION COBRANZA TOTAL",
        "TOTAL A PAGAR VENCIDO", "SALDO ACTUAL", "TOTAL A PAGAR", "MOVIMIENTOS (+)", "MOVIMIENTOS (-)", "TOTAL PAGO",
        "Valor ajuste", "ESTADO_LIQUIDACION", "LIQ. GC POR VALIDAR", "Gestion OK GC_NO GC", "Fecha pago",
        "[RESUMEN CONTACTO IVR]", "Fecha IVR", "[RESUMEN CONTACTO LLAMADA]", "Fecha llamada", "[LIQ. TVCABLE]",
        "CONVENIO", "Respaldo", "CORREO CLIENTE", "EMAIL_CAMPAÑA", "CELULAR CAMPAÑA", "Fecha terminacion", "Empresa",
        "Dias Vencidos"
    ]

    @staticmethod
    def valid_formatte(archivos, internalTransactionId: str, externalTransactionId: str):
        """ Metodo que valida el formato de cabeceras de las tablas."""
        # Lista para almacenar los nombres de archivos validados correctamente
        archivos_validos = []

        for archivo in archivos:
            try:
                # Leer el archivo Excel o CSV (se asume que todos tienen una hoja)
                if archivo.filename.endswith('.csv'):
                    df = pd.read_csv(archivo)
                else:
                    df = pd.read_excel(archivo, engine='openpyxl')

                # Capturar la fila 1 (encabezados) y limpiar espacios al final
                encabezados = [str(col).strip() for col in df.columns[:40]]

                # Validar los encabezados
                for encabezado in encabezados:
                    if encabezado not in ValidationMethods.FORMATO:
                        return {
                            'status': 400,
                            'file_name': archivo.filename,
                            'mesage': f"Título '{encabezado}' no válido en el archivo.",
                            'external_transaction_id': externalTransactionId,
                            'internal_transaction_id': internalTransactionId
                        }
            except Exception as e:
                return {
                    "external_transaction_id": externalTransactionId,
                    "internal_transaction_id": internalTransactionId,
                    "mesage": f"Error al procesar el archivo: {str(e)}",
                    "status": 500
                }
        # Retornar la lista de archivos validados correctamente
        #response = ResponseArchivos(
        #    mesage='Todos los archivos han sido validados correctamente.',
        #    file_name=f'{archivos_validos}',
        #    internal_transaction_id=internalTransactionId,
        #    external_transaction_id=externalTransactionId
        #)
        #return jsonify(response), 200
        return True

    @staticmethod
    def comparete_files(archivos, archivo_fusionado):
        """Este metodo coge los archivos, obtiene los datos de cada uno y los compara con los datos del
        archivo fusionado para verificar que el archivo no salga corrupto"""
