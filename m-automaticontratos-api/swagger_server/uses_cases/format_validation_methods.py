
import pandas as pd

class FormatValidationMethods:
    # Lista de títulos válidos
    FORMATO_COBROS = [
        "CUENTA TITAN", "Referencia interna", "DOCUMENTO IDENTIFICACION", "NOMBRE DEL CLIENTE", "TELEFONOS", "CIUDAD",
        "ESTADO CUENTA", "TIPO CUENTA", "TIPO DE NEGOCIO", "FORMA DE PAGO", "TRANSACCION", "NOM_TRANSACCION",
        "# FAC PEN CARGA", "# FACTURAS PENDIENTE", "SALDO ORIGINAL VENC", "GESTION COBRANZA TOTAL",
        "TOTAL A PAGAR VENCIDO", "SALDO ACTUAL", "TOTAL A PAGAR", "MOVIMIENTOS (+)", "MOVIMIENTOS (-)", "TOTAL PAGO",
        "Valor ajuste", "ESTADO_LIQUIDACION", "LIQ. GC POR VALIDAR", "Gestion OK GC_NO GC", "Fecha pago",
        "[RESUMEN CONTACTO IVR]", "Fecha IVR", "[RESUMEN CONTACTO LLAMADA]", "Fecha llamada", "[LIQ. TVCABLE]",
        "CONVENIO", "Respaldo", "CORREO CLIENTE", "EMAIL_CAMPAÑA", "CELULAR CAMPAÑA", "Fecha terminacion", "Empresa",
        "Dias Vencidos"
    ]

    FORMATO_SUPLANTACION = [
        "Cliente", "Contrato", "Cuenta", "DETALLE", "FECHA EXLUSION"
    ]

    @staticmethod
    def valid_formatte_header_cobranzas(files):
        """ Metodo que valida el formato de cabeceras de las tablas de cobranzas"""

        for file in files:
            try:
                # Leer el archivo Excel o CSV (se asume que todos tienen una hoja)
                if file.filename.endswith('.csv'):
                    df = pd.read_csv(file)
                else:
                    df = pd.read_excel(file, engine='openpyxl')

                # Capturar la fila 1 (encabezados) y limpiar espacios al final
                encabezados = [str(col).strip() for col in df.columns[:40]]

                # Validar los encabezados
                for encabezado in encabezados:
                    if encabezado not in FormatValidationMethods.FORMATO_COBROS:
                        return {
                            'status': 400,
                            'mesage': f"Título '{encabezado}' no válido en el archivo."
                        }
            except Exception as e:
                return {
                    "mesage": f"Error al procesar el archivo: {str(e)}",
                    "status": 500
                }
        return True

    @staticmethod
    def valid_formatte_header_suplantacion(files):
        """ Metodo que valida el formato de cabeceras de las tablas de suplantacion"""
        for file in files:
            try:
                # Leer el archivo Excel o CSV (se asume que todos tienen una hoja)
                if file.filename.endswith('.csv'):
                    df = pd.read_csv(file)
                else:
                    df = pd.read_excel(file, engine='openpyxl')

                # Capturar la fila 1 (encabezados) y limpiar espacios al final
                encabezados = [str(col).strip() for col in df.columns[:40]]

                # Validar los encabezados
                for encabezado in encabezados:
                    if encabezado not in FormatValidationMethods.FORMATO_SUPLANTACION:
                        return {
                            'status': 400,
                            'mesage': f"Título '{encabezado}' no válido en el archivo."
                        }
            except Exception as e:
                return {
                    "mesage": f"Error al procesar el archivo: {str(e)}",
                    "status": 500
                }
        return True