import os

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
        """Este metodo carla la lista de archivos, valida las cedulas repetidas dentro de los archivos y de los archivos entre si"""
        # Ruta para guardar o modificar el archivo de duplicados
        ruta_duplicados = "swagger_server/files/HISTORICO_DUPLICADO.xlsx"

        # Lista para almacenar registros duplicados
        registros_duplicados = []

        # Lista para combinar todas las cédulas y registros
        data_global = []

        # Cargar y validar los archivos
        for archivo in archivos:
            # Cargar el archivo en un DataFrame
            df = pd.read_excel(archivo)

            # Asegurar que las columnas están correctamente definidas
            df.columns = df.columns.str.strip()
            if "DOCUMENTO IDENTIFICACION" not in df.columns:
                raise ValueError("El archivo no contiene la columna 'DOCUMENTO IDENTIFICACION'.")

            # Ajustar las columnas al formato esperado
            df = df[ValidationMethods.FORMATO]

            # Ignorar la primera fila (cabeceras)
            df = df.iloc[1:]

            # Añadir al conjunto global
            data_global.append(df)

            # Validación interna de duplicados
            duplicados_internos = df[df["DOCUMENTO IDENTIFICACION"].duplicated(keep=False)]
            registros_duplicados.append(duplicados_internos)

        # Validación externa (entre todos los archivos)
        if len(data_global) > 1:
            # Unificar todos los registros cargados
            data_consolidada = pd.concat(data_global)

            # Identificar cédulas duplicadas globalmente
            cédulas_duplicadas_globales = data_consolidada["DOCUMENTO IDENTIFICACION"].duplicated(keep=False)

            # Filtrar registros completos con duplicados
            duplicados_externos = data_consolidada[cédulas_duplicadas_globales]
            registros_duplicados.append(duplicados_externos)

        # Consolidar los registros duplicados encontrados
        if registros_duplicados:
            # Combinar los registros duplicados en un único DataFrame
            duplicados_df = pd.concat(registros_duplicados).drop_duplicates()

            # Si el archivo "HISTORICO_DUPLICADO" ya existe, añadir los duplicados al archivo existente
            if os.path.exists(ruta_duplicados):
                historico_existente = pd.read_excel(ruta_duplicados)
                duplicados_df = pd.concat([historico_existente, duplicados_df]).drop_duplicates()

            # Guardar el archivo actualizado
            duplicados_df.to_excel(ruta_duplicados, index=False, header=True)

            return {
                "status": 200,
                "message": "Validación completada. Se actualizó el archivo HISTORICO_DUPLICADO.",
                "path": ruta_duplicados,
            }
        else:
            return {
                "status": 200,
                "message": "No se encontraron cédulas duplicadas en los archivos procesados.",
            }
