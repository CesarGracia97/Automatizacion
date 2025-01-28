from datetime import datetime, timedelta
import calendar
from swagger_server.utils.resource.mysql_configuration import MySQL_Configuration
from swagger_server.utils.tools.tools import Tools

class DB_Queries_Methods:
    @staticmethod
    def query_last_update():
        """Consulta la última actualización de la tabla YTBL_COBRANZAS_EXCLUSION_CLIENTES"""
        try:
            query = """
                SELECT UPDATE_TIME 
                FROM information_schema.tables 
                WHERE TABLE_SCHEMA = %s 
                AND TABLE_NAME = %s;
            """
            db_config = MySQL_Configuration()
            db_config.connect()
            params = ('BD_CON_COBROS', 'YTBL_COBRANZAS_EXCLUSION_CLIENTES')
            results = db_config.fetch_results(query, params)
            db_config.disconnect()

            if results and results[0][0]:
                last_update = results[0][0].date()  #+ timedelta(days=1) # Solo retorna la fecha  # Fecha de última actualización
                return {
                    "status": 200,
                    "fecha": last_update
                }
            else:
                return {
                    "status": 204,
                    "message": "No se encontro informacion relacionada en la tabla"
                }
        except Exception as e:
            return {
                "status": 404,
                "message": e
            }

    @staticmethod
    def query_cuenta_suplantacion(cuenta: int):
        """Verifica si una cuenta existe en la tabla YTBL_COBRANZAS_EXCLUSION_CLIENTES y si cumple las condiciones especificadas."""
        db_config = MySQL_Configuration()
        try:
            # Consulta SQL para verificar si la cuenta existe y obtener el valor de ISVALID
            query = """
                        SELECT ISVALID 
                        FROM YTBL_COBRANZAS_EXCLUSION_CLIENTES 
                        WHERE CUENTA = %s
                    """
            # Ejecutar la consulta
            db_config.connect()

            results = db_config.fetch_results(query, (cuenta,))

            # Evaluar los resultados
            if results:
                is_valid = results[0][0]  # Obtener el valor de ISVALID
                return is_valid == 'Y'
            else:
                return False  # La cuenta no existe

        except Exception as e:
            print(f"Error al ejecutar la consulta: {e}")
            return False

        finally:
            db_config.disconnect()

    @staticmethod
    def query_meses_disponible():
        db_config = MySQL_Configuration()
        db_config.connect()
        tools = Tools()
        try:
            now = datetime.now()
            current_month = now.month
            current_year = now.year

            available_months = [
                {"mes": current_month, "ano": current_year},
                {"mes": (current_month % 12) + 1, "ano": current_year if current_month < 12 else current_year + 1},
            ]

            # Consulta para obtener el último registro
            query = """SELECT FECHAFIN FROM YTBL_COBRANZAS_PROCESO WHERE FECHAFIN IS NOT NULL ORDER BY ID DESC LIMIT 1"""
            result = db_config.fetch_results(query)
            if not result:
                return {
                    "status": 200,
                    "meses": tools.mounthsTranslateGenerator(available_months)
                }
            last_fecha_fin = result[0][0]
            last_fecha_fin = datetime.strptime(last_fecha_fin, "%Y-%m-%d")
            last_month = last_fecha_fin.month
            last_year = last_fecha_fin.year
            available_months = [
                month
                for month in available_months
                if not (
                    (month["ano"] == last_year and month["mes"] == last_month)
                )
            ]
            if available_months:
                return {
                    "status": 200,
                    "meses": tools.mounthsTranslateGenerator(available_months)
                }
            else:
                return {
                    "status": 204,
                    "meses": []
                }
        except Exception as e:
            print(f"Error al consultar los meses disponibles: {e}")
            return {
                "status": 400,
                "message": "ERROR EN LA CONSULTA"
            }
        finally:
            db_config.disconnect()

    @staticmethod
    def query_procesos_disponibles():
        db_config = MySQL_Configuration()
        response = {}
        try:
            query = """SELECT IDPROCESO, NOMBRE, FINICIO, FFIN FROM YTBL_COBRANZAS_PROCESO  WHERE ISVALID = 'Y'"""

            db_config.connect()

            results = db_config.fetch_results(query)
            if results:
                # Convertir los resultados en una lista de diccionarios
                response["procesos"] = [{"IDPROCESO": row[0], "NOMBRE": row[1], "FINICIO": row[2], "FFIN": row[3]} for row in results]
                response["status"] = 200
            else:
                response["status"] = 404
                response["message"] = "No se encontraron procesos disponibles."
        except Exception as e:
            response["message"]= f"Error al ejecutar la consulta: {e}"
            response["status"]= 500
        finally:
            db_config.disconnect()
            return response

    @staticmethod
    def query_idcampana(campana, fcreacion, fechafin)-> int :
        """ Obtiene el IDCAMPANIA recién generado a partir de los datos proporcionados de la campaña."""
        db_config = MySQL_Configuration()
        try:
            # Extraer valores de la campaña
            nombre = campana['nombre']
            descuento = campana['descuento']
            finicio = campana['finicio']
            ffin = campana['ffin']

            # Query para obtener el IDCAMPANIA
            query = """SELECT ID FROM YTBL_COBRANZAS_CAMPANIA
                WHERE NOMBRE = %s AND PORC_DESCUENTO = %s AND FCREACION = %s AND FFIN = %s AND FINICIO = %s 
                AND FECHAFIN = %s AND ISVALID = 'V' ORDER BY ID DESC LIMIT 1"""
            params = (nombre, descuento, fcreacion, ffin, finicio, fechafin)
            db_config.connect()
            result = db_config.fetch_results(query, params)
            db_config.disconnect()
            if result:
                return result[0][0]  # Extraer el IDCAMPANIA
            return None  # Si no hay resultados, retornar None
        except Exception as e:
            raise Exception(f"Error al consultar IDCAMPANIA: {e}")
