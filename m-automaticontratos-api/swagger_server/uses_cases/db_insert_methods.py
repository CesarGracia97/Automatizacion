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
        """ Procesa los archivos Excel o CSV y verifica cada registro con la consulta query_cuenta_suplantacion. """
        total_registros = 0
        registros_insertados = 0

        for file in files:
            try:
                # Leer el archivo en un DataFrame de Pandas
                df = pd.read_excel(file) if file.filename.endswith('.xls') or file.filename.endswith(
                    '.xlsx') else pd.read_csv(file)

                total_registros += len(df)

                # Iterar sobre los registros del DataFrame
                for index, row in df.iterrows():
                    cuenta_titan = row.get("CUENTA TITAN")

                    if pd.isna(cuenta_titan):
                        print(f"Registro en la fila {index + 2} tiene una CUENTA TITAN vacía.")
                        continue

                    # Verificar si la cuenta existe en la base de datos
                    query = DB_Queries_Methods
                    cuenta_valida = query.query_cuenta_suplantacion(int(cuenta_titan))

                    is_valid = 'Y' if not cuenta_valida else 'N'

                    # Preparar los valores para insertar en la base de datos
                    values = (
                        int(cuenta_titan),
                        row.get("Referencia interna"),
                        row.get("DOCUMENTO IDENTIFICACION"),
                        row.get("NOMBRE DEL CLIENTE"),
                        row.get("TELEFONOS"),
                        row.get("CIUDAD"),
                        row.get("ESTADO CUENTA"),
                        row.get("TIPO CUENTA"),
                        row.get("TIPO DE NEGOCIO"),
                        row.get("FORMA DE PAGO"),
                        row.get("TRANSACCION"),
                        row.get("NOM_TRANSACCION"),
                        row.get("# FAC PEN CARGA"),
                        row.get("# FACTURAS PENDIENTE"),
                        row.get("SALDO ORIGINAL VENC"),
                        row.get("GESTION COBRANZA TOTAL"),
                        row.get("TOTAL A PAGAR VENCIDO"),
                        row.get("SALDO ACTUAL"),
                        row.get("TOTAL A PAGAR"),
                        row.get("MOVIMIENTOS (+)"),
                        row.get("MOVIMIENTOS (-)"),
                        row.get("TOTAL PAGO"),
                        row.get("Valor ajuste"),
                        row.get("ESTADO_LIQUIDACION"),
                        row.get("LIQ. GC POR VALIDAR"),
                        row.get("Gestion OK GC_NO GC"),
                        row.get("Fecha pago"),
                        row.get("[RESUMEN CONTACTO IVR]"),
                        row.get("Fecha IVR"),
                        row.get("[RESUMEN CONTACTO LLAMADA]"),
                        row.get("Fecha llamada"),
                        row.get("[LIQ. TVCABLE]"),
                        row.get("CONVENIO"),
                        row.get("Respaldo"),
                        row.get("CORREO CLIENTE"),
                        row.get("EMAIL_CAMPAÑA"),
                        row.get("CELULAR CAMPAÑA"),
                        row.get("Fecha terminacion"),
                        row.get("Empresa"),
                        row.get("Dias Vencidos"),
                        datetime.now().date(),
                        file.filename,
                        is_valid
                    )

                    # Insertar los datos en la base de datos
                    query = """
                        INSERT INTO YTBL_COBRANZAS_BASE_COBRANZAS (
                            CUENTA, REFERENCIA_INTERNA, DOCUMENTO_IDENTIFICACION, NOMBRE_CLIENTE, TELEFONOS, CIUDAD,
                            ESTADO_CUENTA, TIPO_CUENTA, TIPO_NEGOCIO, FORMA_PAGO, TRANSACCION, NOM_TRANSACCION,
                            NFACPEN_CARGA, NFACTURAS_PENDIENTE, SALDO_ORIGINAL_VENC, GESTION_COBRANZA_TOTAL,
                            TOTAL_A_PAGAR_VENCIDO, SALDO_ACTUAL, TOTAL_A_PAGAR, MOVIMIENTOS_POS, MOVIMIENTOS_NEG,
                            TOTAL_PAGO, VALOR_AJUSTE, ESTADO_LIQUIDACION, LIQ_GC_POR_VALIDAR, GESTION_OK_GC_NO_GC,
                            FECHA_PAGO, RESUMEN_CONTACTO_IVR, FECHA_IVR, RESUMEN_CONTACTO_LLAMADA, FECHA_LLAMADA,
                            LIQ_TVCABLE, CONVENIO, RESPALDO, CORREO_CLIENTE, EMAIL_CAMPANA, CELULAR_CAMPANA,
                            FECHA_TERMINACION, EMPRESA, DIAS_VENCIDOS, FECHA_CREACION, NOMBRE_ARCHIVO, ISVALID
                        ) VALUES (
                            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                        )
                    """
                    db_config = MySQL_Configuration()
                    db_config.connect()
                    db_config.execute_query(query, values)
                    db_config.disconnect()

                    registros_insertados += 1
                    print(f"Registro de la cuenta {cuenta_titan} insertado con éxito.")

            except Exception as e:
                return {
                    "message": str(e),
                    "status": 400
                }

        if registros_insertados == total_registros:
            return {
                "message": "Todos los registros de BD fueron guardados correctamente",
                "status": 200
            }
        else:
            return {
                "message": f"Se procesaron {registros_insertados}/{total_registros} registros.",
                "status": 204
            }

    @staticmethod
    def insert_data_proceso_create(data):
        """
        Inserta datos en la tabla YTBL_COBRANZAS_PROCESO_COBRO:param datos: Un diccionario que contiene los siguientes campos:
                      - nombre: str, nombre del proceso.
                      - finicio: datetime, fecha inicial del proceso.
                      - ffin: datetime (opcional), fecha final del proceso.
                      - mes: int, número del mes del proceso (1 = enero, 12 = diciembre).
        """
        # Validar que el objeto datos tenga los campos requeridos
        response = {}
        if not all(key in data for key in ['nombre', 'finicio', 'mes']):
            raise ValueError("Faltan campos requeridos en el objeto 'datos'.")

        nombre = data['nombre']
        finicio = data['finicio']
        mes = data['mes']  # Mes como número entero (1-12)
        fcreacion = datetime.now().date()  # Fecha de creación actual

        # Validar que el mes sea un número válido
        if not (1 <= mes <= 12):
            raise ValueError(f"El valor de 'mes' ({mes}) no es válido. Debe estar entre 1 y 12.")

        # Calcular la fecha final del mes (FFIN)
        if 'ffin' in data and data['ffin'] is not None:
            ffin = data['ffin']
        else:
            # Calcular el último día del mes
            year = finicio.year
            _, last_day = calendar.monthrange(year, mes)
            ffin = datetime(year, mes, last_day).date()

        # Conectar a la base de datos y ejecutar el query
        query = """
            INSERT INTO YTBL_COBRANZAS_PROCESO (NOMBRE, FCREACION, FINICIO, FFIN, ISVALID)
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
            ffin = campana['ffin']
            # Calcular fecha de creación y último día del mes de `ffin`
            fcreacion = datetime.now().date()
            _, last_day = calendar.monthrange(ffin.year, ffin.month)
            ffin_end_of_month = datetime(ffin.year, ffin.month, last_day).date()
            query = """INSERT INTO YTBL_COBRANZAS_CAMPANIA (NOMBRE, PORC_DESCUENTO, FCREACION, FFIN, FINICIO, FECHAFIN, ISVALID)
                VALUES (%s, %s, %s, %s, %s, %s, %s)"""
            params = (campana['nombre'], campana['descuento'], fcreacion, ffin_end_of_month, campana['finicio'], ffin, 'V')
            db_config.connect()
            db_config.execute_query(query, params)
            db_config.disconnect()
            # Proceso para obtener el IDCAMPANIA recién insertado
            id_campana = DB_Queries_Methods.query_idcampana(campana, fcreacion, ffin_end_of_month)

            if not id_campana:
                raise Exception("No se pudo obtener el ID de la campaña recién insertada.")

            # Proceso para registrar la relación entre proceso y campaña
            DB_Insert_Methods.insert_data_relation_proceso_campana( idProceso, id_campana, campana, fcreacion, ffin_end_of_month)

            response["status"] = 200
            response["message"] = "Datos insertados correctamente en la tabla YTBL_COBRANZAS_CAMPANIA."
        except Exception as e:
            response["status"] = 500
            response["message"] = f"Error al insertar datos: {e}"
        finally:
            return response

    @staticmethod
    def insert_data_relation_proceso_campana(idProceso, idCampana, campana, fcreacion,ffin_end_of_month):
        try:
            db_config = MySQL_Configuration()
            query = """ INSERT INTO YTBL_COBRANZAS_PROCESO_CAMPANIA(IDPROCESO, IDCAMPANIA, FCREACION, FFIN, FINICIO, FECHAFIN, ISVALID)
            VALUES (%s, %s, %s, %s, %s, %s, %s)"""
            params = (idProceso, idCampana,fcreacion, ffin_end_of_month, campana['finicio'], campana['ffin'], 'V')
            db_config.connect()
            db_config.execute_query(query, params)
            db_config.disconnect()
        except Exception as e:
            raise Exception(f"Error al insertar la relacion: {e}")
