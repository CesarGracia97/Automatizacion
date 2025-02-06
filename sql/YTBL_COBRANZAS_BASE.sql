USE BD_CON_COBROS;
CREATE TABLE IF NOT EXISTS YTBL_COBRANZAS_BASE (
ID INT AUTO_INCREMENT PRIMARY KEY,

CUENTA bigint,
REFERENCIA_INTERNA int,
DOCUMENTO_IDENTIFICACION varchar(100),
NOMBRE_CLIENTE varchar(100),
TELEFONOS varchar(100),

CIUDAD varchar(100),
ESTADO_CUENTA varchar(100),
TIPO_CUENTA varchar(100),
TIPO_NEGOCIO varchar(100),
FORMA_PAGO varchar(100),

TRANSACCION int,
NOM_TRANSACCION varchar(100),
NFACPEN_CARGA varchar(100),
NFACTURAS_PENDIENTE varchar(100),
SALDO_ORIGINAL_VENC double,

GESTION_COBRANZA_TOTAL double,
TOTAL_A_PAGAR_VENCIDO double,
SALDO_ACTUAL double,
TOTAL_A_PAGAR double,
MOVIMIENTOS_POS double,

MOVIMIENTOS_NEG double,
TOTAL_PAGO double,
VALOR_AJUSTE double,
ESTADO_LIQUIDACION varchar(100),
LIQ_GC_POR_VALIDAR double,

GESTION_OK_GC_NO_GC varchar(100),
FECHA_PAGO date,
RESUMEN_CONTACTO_IVR varchar(100),
FECHA_IVR date,
RESUMEN_CONTACTO_LLAMADA varchar(100),

FECHA_LLAMADA date,
LIQ_TVCABLE varchar(100),
CONVENIO varchar(100),
RESPALDO int,
CORREO_CLIENTE varchar(100),

EMAIL_CAMPANA varchar(100),
CELULAR_CAMPANA varchar(100),
FECHA_TERMINACION date,
EMPRESA varchar(100),
DIAS_VENCIDOS int,

FECHA_CREACION date, 
NOMBRE_ARCHIVO varchar(100),
ISVALID varchar(1)
);


USE BD_CON_COBROS;
DROP TABLE YTBL_COBRANZAS_BASE;
