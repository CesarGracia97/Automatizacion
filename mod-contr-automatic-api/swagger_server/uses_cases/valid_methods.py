import os
from datetime import datetime

import pandas as pd

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
    def valid_formatte(archivos):
        """ Metodo que valida el formato de cabeceras de las tablas."""

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
                            'mesage': f"Título '{encabezado}' no válido en el archivo."
                        }
            except Exception as e:
                return {
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
    def valid_ci(archivos):
        """
        Este método unifica los archivos en memoria, detecta registros duplicados según el
        "DOCUMENTO IDENTIFICACION" y registros completamente idénticos.
        """
        try:
            # Ruta base para guardar los archivos
            base_path = os.path.join("swagger_server", "files")
            duplicates_path = os.path.join(base_path, "DUPLICADOS")
            no_duplicates_path = os.path.join(base_path, "NO_DUPLICADOS")

            # Crear directorios si no existen
            os.makedirs(duplicates_path, exist_ok=True)
            os.makedirs(no_duplicates_path, exist_ok=True)

            # Obtener la fecha actual para los nombres de los archivos
            fecha_actual = datetime.now().strftime("%d-%m-%Y")
            archivo_duplicados = os.path.join(duplicates_path, f"REPORTE_DUPLICADOS_{fecha_actual}.xlsx")
            archivo_no_duplicados = os.path.join(no_duplicates_path, f"REPORTE_NDUPLICADOS_{fecha_actual}.xlsx")

            # Lista para almacenar DataFrames de cada archivo
            dataframes = []

            # Cargar y procesar cada archivo
            for archivo in archivos:
                if archivo.filename.endswith(".csv"):
                    df = pd.read_csv(archivo)
                else:
                    df = pd.read_excel(archivo)

                # Validar que las columnas coincidan con el formato esperado
                df.columns = df.columns.str.strip()  # Eliminar espacios en los nombres de las columnas
                if not all(col in df.columns for col in ValidationMethods.FORMATO):
                    raise ValueError("El archivo no tiene las columnas requeridas.")

                # Seleccionar solo las columnas definidas en el formato
                df = df[ValidationMethods.FORMATO]

                # Agregar el DataFrame procesado a la lista
                dataframes.append(df)

            # Unificar todos los DataFrames en uno solo
            df_unificado = pd.concat(dataframes, ignore_index=True)

            # Eliminar espacios en los valores de "DOCUMENTO IDENTIFICACION"
            df_unificado["DOCUMENTO IDENTIFICACION"] = df_unificado["DOCUMENTO IDENTIFICACION"].astype(str).str.strip()

            # Detectar duplicados por "DOCUMENTO IDENTIFICACION"
            duplicados_cedulas = df_unificado[df_unificado["DOCUMENTO IDENTIFICACION"].duplicated(keep=False)]
            no_duplicados = df_unificado.drop(duplicados_cedulas.index)

            # Guardar los registros duplicados en un archivo Excel
            if not duplicados_cedulas.empty:
                duplicados_cedulas.to_excel(archivo_duplicados, index=False, columns=ValidationMethods.FORMATO)
            else:
                archivo_duplicados = None  # No se crea archivo si no hay duplicados

            # Guardar los registros no duplicados en otro archivo Excel
            if not no_duplicados.empty:
                no_duplicados.to_excel(archivo_no_duplicados, index=False, columns=ValidationMethods.FORMATO)
            else:
                archivo_no_duplicados = None  # No se crea archivo si no hay registros únicos

            # Construir la respuesta
            resultados = {
                "status": 200,
                "mensaje": "Validación completada.",
                "archivo_duplicados": archivo_duplicados if archivo_duplicados else "No se generó archivo de duplicados.",
                "archivo_no_duplicados": archivo_no_duplicados if archivo_no_duplicados else "No se generó archivo de no duplicados."
            }

            return resultados

        except Exception as e:
            return {
                "mesage": f"Error al procesar los archivos: {str(e)}",
                "status": 500
            }

