import pandas as pd
from datetime import datetime
import calendar
from swagger_server.utils.resource.mysql_configuration import MySQL_Configuration
from swagger_server.uses_cases.db_queries_methods import DB_Queries_Methods

class DB_Update_Method:

    @staticmethod
    def update_data_suspendidos(suspendidos):
        """"""
        response = {}
        try:
            db_config = MySQL_Configuration()
            query = """UPDATE YTBL_COBRANZAS_EXCLUSION_CLIENTES SET ISVALID =%s WHERE CONTRATO = %s"""
            params = (suspendidos.isvalid, suspendidos.contrato)
            db_config.connect()
            db_config.execute_query(query, params)
            db_config.disconnect()
            response["status"] = 200
            response["message"] = "Se actualizo el registro del usuario suspendido."
        except Exception as e:
            response["message"]= f"Error al ejecutar la consulta: {e}"
            response["status"]= 500
        finally:
            return response
