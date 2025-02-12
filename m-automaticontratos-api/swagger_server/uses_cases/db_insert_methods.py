import pandas as pd
from datetime import datetime
import calendar
from swagger_server.utils.resource.mysql_configuration import MySQL_Configuration
from swagger_server.uses_cases.db_queries_methods import DB_Queries_Methods


class DB_Insert_Methods:

    @staticmethod
    def insert_data_suplantacion_create(file):
        """
        Procesa una lista de archivos Excel o CSV para verificar la existencia
        de los datos en la tabla YTBL_COBRANZAS_EXCLUSION_CLIENTES. Inserta nuevos registros si es necesario
        y muestra mensajes finales basados en los resultados.
        """
        message: str = ""
        status_code: int = 0
        db_config = MySQL_Configuration()
        db_config.connect()  # Establecer conexión con la base de datos

        try:
            todos_registros_existentes = True
            algunos_registros_insertados = False

            for file in file:
                # Leer archivo como DataFrame
                if file.filename.endswith(".csv"):
                    df = pd.read_csv(file)
                else:
                    df = pd.read_excel(file)

                # Crear listas para separar registros que existen y no existen
                registros_existentes = []
                registros_no_existentes = []

                # Iterar sobre los registros del archivo
                for _, row in df.iterrows():
                    try:
                        cliente = row["Cliente"]
                        contrato = int(str(row["Contrato"]).replace(" ", ""))  # Eliminar espacios y convertir a int
                        cuenta = int(str(row["Cuenta"]).replace(" ", ""))  # Eliminar espacios y convertir a int
                        detalle = row["DETALLE"]
                        fecha_exclusion = row["FECHA EXLUSION"]
                        params = (cuenta,)
                        # Query para verificar la existencia del registro basado en la columna CUENTA
                        query = """
                                                SELECT 1 FROM YTBL_COBRANZAS_EXCLUSION_CLIENTES 
                                                WHERE CUENTA = %s
                                                AND ISVALID ='Y'
                                            """


                        # Ejecutar la consulta
                        result = db_config.fetch_results(query, params)

                        if result:
                            # La cuenta ya existe y es válida, no se inserta
                            registros_existentes.append({
                                "Cliente": cliente,
                                "Contrato": contrato,
                                "Cuenta": cuenta,
                                "DETALLE": detalle,
                                "FECHA EXLUSION": fecha_exclusion
                            })
                        else:
                            # La cuenta no existe o existe pero no es válida, se inserta
                            registros_no_existentes.append({
                                "Cliente": cliente,
                                "Contrato": contrato,
                                "Cuenta": cuenta,
                                "DETALLE": detalle,
                                "FECHA EXLUSION": fecha_exclusion
                            })

                            # Insertar el registro en la base de datos con las nuevas columnas
                            insert_query = """
                                                    INSERT INTO YTBL_COBRANZAS_EXCLUSION_CLIENTES (
                                                        CLIENTE, CONTRATO, CUENTA, DETALLE, FECHA_EXCLUSION, 
                                                        FECHA_CREACION, ISVALID, NAME_FILE
                                                    )
                                                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                                                """
                            fecha_creacion = datetime.now().strftime('%Y-%m-%d')  # Fecha actual
                            isvalid = "Y"  # Siempre será "Y"
                            name_file = file.filename  # Nombre del archivo actual
                            insert_params = (cliente, contrato, cuenta, detalle, fecha_exclusion,
                                             fecha_creacion, isvalid, name_file)
                            db_config.execute_query(insert_query, insert_params)
                            algunos_registros_insertados = True
                    except ValueError:
                        raise ValueError("Error al procesar los valores de Contrato o Cuenta en el archivo.")

                if registros_no_existentes:
                    todos_registros_existentes = False

            # Mensaje final basado en los resultados
            if todos_registros_existentes:
                message = "LOS DATOS DEL EXCEL YA EXISTEN EN LA BD"
                status_code = 204
            elif algunos_registros_insertados:
                if len(registros_no_existentes) == len(df):
                    message = "LA BASE DE DATOS FUE ACTUALIZADA EXITOSAMENTE"
                    status_code = 200
                else:
                    message = "ALGUNOS DATOS DEL EXCEL YA EXISTEN EN LA BD, LOS QUE NO EXISTIAN YA FUERON CARGADOS EXITOSAMENTE"
                    status_code = 200

        finally:
            db_config.disconnect()  # Cerrar conexión con la base de datos
            return {"message": message, "status": status_code}

    @staticmethod
    def insert_data_cobros_create(files):
        """ Procesa los archivos Excel o CSV y verifica cada registro antes de insertarlo en la base de datos. """
        total_registros = 0
        registros_insertados = 0

        for file in files:
            try:
                # Leer el archivo en un DataFrame de Pandas
                df = pd.read_excel(file) if file.filename.endswith('.xls') or file.filename.endswith('.xlsx') else pd.read_csv(file)
                df.columns = df.columns.str.strip()  # Normalizar nombres de columnas
                total_registros += len(df)

                # Conectar a la base de datos una sola vez por archivo
                db_config = MySQL_Configuration()
                db_config.connect()

                for index, row in df.iterrows():
                    cuenta_titan = row.get("CUENTA TITAN")

                    if pd.isna(cuenta_titan):
                        print(f"Registro en la fila {index + 2} tiene una CUENTA TITAN vacía. Saltando...")
                        continue

                    # Verificar si la cuenta ya existe en la base de datos
                    query = DB_Queries_Methods()
                    cuenta_valida = query.query_cuenta_suplantacion(int(cuenta_titan))

                    is_valid = 'Y' if not cuenta_valida else 'N'

                    # Preparar valores para la inserción
                    values = (
                        int(cuenta_titan),
                        int(str(row.get("Referencia interna", 0))) if not pd.isna(row.get("Referencia interna")) else 0,
                        row.get("DOCUMENTO IDENTIFICACION", "") if not pd.isna(row.get("DOCUMENTO IDENTIFICACION")) else "",
                        row.get("NOMBRE DEL CLIENTE", "") if not pd.isna(row.get("NOMBRE DEL CLIENTE")) else "",
                        row.get("TELEFONOS", "") if not pd.isna(row.get("TELEFONOS")) else "",

                        row.get("CIUDAD", "") if not pd.isna(row.get("CIUDAD")) else "",
                        row.get("ESTADO CUENTA", "") if not pd.isna(row.get("ESTADO CUENTA")) else "",
                        row.get("TIPO CUENTA", "") if not pd.isna(row.get("TIPO CUENTA")) else "",
                        row.get("TIPO DE NEGOCIO", "") if not pd.isna(row.get("TIPO DE NEGOCIO")) else "",
                        row.get("FORMA DE PAGO", "") if not pd.isna(row.get("FORMA DE PAGO")) else "",

                        int(str(row.get("TRANSACCION", 0))) if not pd.isna(row.get("TRANSACCION")) else 0,
                        row.get("NOM_TRANSACCION", "") if not pd.isna(row.get("NOM_TRANSACCION")) else "",
                        row.get("# FAC PEN CARGA", "") if not pd.isna(row.get("# FAC PEN CARGA")) else "",
                        row.get("# FACTURAS PENDIENTE", "") if not pd.isna(row.get("# FACTURAS PENDIENTE")) else "",
                        float(str(row.get("SALDO ORIGINAL VENC", 0.00)).replace(",", ".")) if not pd.isna(row.get("SALDO ORIGINAL VENC")) else 0.00,

                        float(str(row.get("GESTION COBRANZA TOTAL", 0.00)).replace(",", ".")) if not pd.isna(row.get("GESTION COBRANZA TOTAL")) else 0.00,
                        float(str(row.get("TOTAL A PAGAR VENCIDO", 0.00)).replace(",", ".")) if not pd.isna(row.get("TOTAL A PAGAR VENCIDO")) else 0.00,
                        float(str(row.get("SALDO ACTUAL", 0.00)).replace(",", ".")) if not pd.isna(row.get("SALDO ACTUAL")) else 0.00,
                        float(str(row.get("TOTAL A PAGAR", 0.00)).replace(",", ".")) if not pd.isna(row.get("TOTAL A PAGAR")) else 0.00,
                        float(str(row.get("MOVIMIENTOS (+)", 0.00)).replace(",", ".")) if not pd.isna(row.get("MOVIMIENTOS (+)")) else 0.00,

                        float(str(row.get("MOVIMIENTOS (-)", 0.00)).replace(",", ".")) if not pd.isna(row.get("MOVIMIENTOS (-)")) else 0.00,
                        float(str(row.get("TOTAL PAGO", 0.00)).replace(",", ".")) if not pd.isna(row.get("TOTAL PAGO")) else 0.00,
                        float(str(row.get("Valor ajuste", 0.00)).replace(",", ".")) if not pd.isna(row.get("Valor ajuste")) else 0.00,
                        row.get("ESTADO_LIQUIDACION", "") if not pd.isna(row.get("ESTADO_LIQUIDACION")) else "",
                        float(str(row.get("LIQ. GC POR VALIDAR", 0.00)).replace(",", ".")) if not pd.isna(row.get("LIQ. GC POR VALIDAR")) else 0.00,

                        row.get("Gestion OK GC_NO GC", "") if not pd.isna(row.get("Gestion OK GC_NO GC")) else "",
                        row.get("Fecha pago", None) if not pd.isna(row.get("Fecha pago")) else None,
                        row.get("[RESUMEN CONTACTO IVR]", "") if not pd.isna(row.get("[RESUMEN CONTACTO IVR]")) else "",
                        row.get("Fecha IVR", None) if not pd.isna(row.get("Fecha IVR")) else None,
                        row.get("[RESUMEN CONTACTO LLAMADA]", "") if not pd.isna(row.get("[RESUMEN CONTACTO LLAMADA]")) else "",

                        row.get("Fecha llamada", None) if not pd.isna(row.get("Fecha llamada")) else None,
                        row.get("[LIQ. TVCABLE]", "") if not pd.isna(row.get("[LIQ. TVCABLE]")) else "",
                        row.get("CONVENIO", "") if not pd.isna(row.get("CONVENIO")) else "",
                        int(str(row.get("Respaldo", "0"))) if not pd.isna(row.get("Respaldo")) else 0,
                        row.get("CORREO CLIENTE", "") if not pd.isna(row.get("CORREO CLIENTE")) else "",

                        row.get("EMAIL_CAMPAÑA", "") if not pd.isna(row.get("EMAIL_CAMPAÑA")) else "",
                        row.get("CELULAR CAMPAÑA", "") if not pd.isna(row.get("CELULAR CAMPAÑA")) else "",
                        row.get("Fecha terminacion", None) if not pd.isna(row.get("Fecha terminacion")) else None,
                        row.get("Empresa", "") if not pd.isna(row.get("Empresa")) else "",
                        int(str(row.get("Dias Vencidos", "0"))) if not pd.isna(row.get("Dias Vencidos")) else 0,

                        datetime.now().date(),
                        file.filename,
                        is_valid
                    )

                    # Query de inserción
                    insert_query = """
                        INSERT INTO YTBL_COBRANZAS_BASE (
                        CUENTA, REFERENCIA_INTERNA, DOCUMENTO_IDENTIFICACION, NOMBRE_CLIENTE, TELEFONOS, 
                        CIUDAD, ESTADO_CUENTA, TIPO_CUENTA, TIPO_NEGOCIO, FORMA_PAGO,
                        TRANSACCION, NOM_TRANSACCION, NFACPEN_CARGA, NFACTURAS_PENDIENTE, SALDO_ORIGINAL_VENC, 
                        GESTION_COBRANZA_TOTAL, TOTAL_A_PAGAR_VENCIDO, SALDO_ACTUAL, TOTAL_A_PAGAR, MOVIMIENTOS_POS,
                        MOVIMIENTOS_NEG, TOTAL_PAGO, VALOR_AJUSTE, ESTADO_LIQUIDACION, LIQ_GC_POR_VALIDAR, 
                        GESTION_OK_GC_NO_GC, FECHA_PAGO, RESUMEN_CONTACTO_IVR, FECHA_IVR, RESUMEN_CONTACTO_LLAMADA,
                        FECHA_LLAMADA, LIQ_TVCABLE, CONVENIO, RESPALDO, CORREO_CLIENTE,
                        EMAIL_CAMPANA, CELULAR_CAMPANA, FECHA_TERMINACION, EMPRESA, DIAS_VENCIDOS,
                        FECHA_CREACION, NOMBRE_ARCHIVO, ISVALID
                        ) VALUES (
                        %s, %s, %s, %s, %s,
                        %s, %s, %s, %s, %s,
                        %s, %s, %s, %s, %s,
                        %s, %s, %s, %s, %s,
                        %s, %s, %s, %s, %s,
                        %s, %s, %s, %s, %s,
                        %s, %s, %s, %s, %s,
                        %s, %s, %s, %s, %s,
                        %s, %s, %s
                        )
                    """
                    try:
                        result = db_config.execute_query(insert_query, values)
                        if result:
                            registros_insertados += 1
                            print(f"Registro insertado con éxito: CUENTA {cuenta_titan}")
                        else:
                            print(f"⚠️ Error al insertar CUENTA {cuenta_titan}. No se realizó la operación.")
                    except Exception as e:
                        print(f"❌ Error al insertar CUENTA {cuenta_titan}: {str(e)}")

                db_config.disconnect()

            except Exception as e:
                return {"message": str(e), "status": 400}

        if registros_insertados == total_registros:
            return {"message": "Todos los registros de BD fueron guardados correctamente", "status": 200}
        else:
            return {"message": f"Se procesaron {registros_insertados}/{total_registros} registros.", "status": 204}


    @staticmethod
    def insert_data_proceso_create(data):
        """
        Inserta datos en la tabla YTBL_COBRANZAS_PROCESO_COBRO:param datos: Un diccionario que contiene los siguientes campos:
        """
        # Validar que el objeto datos tenga los campos requeridos
        response = {}
        nombre = data.nombre
        fcreacion = datetime.now().date()  # Fecha de creación actua
        finicio = data.finicio
        ffin = data.ffin

        # Conectar a la base de datos y ejecutar el query
        query = """
            INSERT INTO YTBL_COBRANZAS_PROCESO (NOMBRE, FCREACION, FIPROCESO, FFPROCESO, ISVALID)
            VALUES (%s, %s, %s, %s, %s)
        """
        params = (nombre, fcreacion, finicio, ffin, 'Y')

        db_config = MySQL_Configuration()
        try:
            db_config.connect()
            db_config.execute_query(query, params)
            response["status"] = 200
            response["message"] = "Datos insertados Correctamente"
        except Exception as e:
            response["status"] = 500
            response["message"] = f"Error al insertar datos: {e}"

        finally:
            db_config.disconnect()
            return response

    @staticmethod
    def insert_data_campana_create(campana, idProceso):
        """Inserta un registro en la tabla YTBL_COBRANZAS_CAMPANIA"""
        response = {"status": None, "message": ""}
        db_config = MySQL_Configuration()
        try:
            # Calcular fecha de creación y último día del mes de `ffin`
            fcreacion = datetime.now().date()
            query = """INSERT INTO YTBL_COBRANZAS_CAMPANA (NOMBRE, PORC_DESCUENTO, FCREACION, FICAMPANA, FFCAMPANA, ISVALID)
                VALUES (%s, %s, %s, %s, %s, %s)"""
            params = (campana.nombre, campana.descuento, fcreacion, campana.finicio, campana.ffin, 'Y')
            db_config.connect()
            db_config.execute_query(query, params)
            db_config.disconnect()
            # Proceso para obtener el IDCAMPANIA recién insertado
            id_campana = DB_Queries_Methods.query_idcampana(campana, fcreacion)

            if not id_campana:
                raise Exception("No se pudo obtener el ID de la campaña recién insertada.")

            # Proceso para registrar la relación entre proceso y campaña
            DB_Insert_Methods.insert_data_relation_proceso_campana( idProceso, id_campana, campana, fcreacion)

            response["status"] = 200
            response["message"] = "Datos insertados correctamente en la tabla YTBL_COBRANZAS_CAMPANIA."
        except Exception as e:
            response["status"] = 500
            response["message"] = f"Error al insertar datos: {e}"
        finally:
            return response

    @staticmethod
    def insert_data_relation_proceso_campana(idProceso, idCampana, campana, fcreacion):
        try:
            db_config = MySQL_Configuration()
            query = """ INSERT INTO YTBL_COBRANZAS_PROCESO_CAMPANA(IDPROCESO, IDCAMPANA, FCREACION, FINICIO, FECHAFIN, ISVALID)
            VALUES (%s, %s, %s, %s, %s, %s)"""
            params = (idProceso, idCampana, fcreacion, campana.finicio, campana.ffin, 'Y')
            db_config.connect()
            db_config.execute_query(query, params)
            db_config.disconnect()
        except Exception as e:
            raise Exception(f"Error al insertar la relacion: {e}")

    @staticmethod
    def insert_data_suspendidos(suspendido):
        """"""
        response = {}
        db_config = MySQL_Configuration()
        try:
            fcreacion = datetime.now().date()
            query = """INSERT INTO YTBL_COBRANZAS_EXCLUSION_CLIENTES (CUENTA, CLIENTE, CONTRATO, DETALLE, FECHA_EXCLUSION, 
            FECHA_CREACION, NAME_FILE, ISVALID) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
            params = (suspendido.cuenta, suspendido.cliente, suspendido.contrato, suspendido.detalle,
                      suspendido.fecha_exclusion, fcreacion, 'WEB_CONTRATOS', 'Y')
            db_config.connect()
            db_config.execute_query(query, params)
            db_config.disconnect()
            response["status"] = 200
            response["message"] = "Datos insertados correctamente en la tabla YTBL_COBRANZAS_EXCLUSION_CLIENTES."
        except Exception as e:
            response["status"] = 500
            response["message"] = f"Error al insertar datos: {e}"
        finally:
            return response
