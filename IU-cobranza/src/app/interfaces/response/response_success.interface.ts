export interface S_LastUpdate{
    status: number,
    fecha: Date,
    externalTransactionId: string,
    internalTransactionId: string
}

export interface S_AvailableMonths{
    status: number,
    meses: {
        nombre: string; // Nombre del mes traducido (Ejemplo: "Enero 2025")
        mes: number;    // Número del mes (Ejemplo: 1 para Enero)
        ano: number;    // Año del mes (Ejemplo: 2025)
    }[];
    externalTransactionId: string,
    internalTransactionId: string
}

export interface S_Charge{
    status: number,
    message: string,
    externalTransactionId: string,
    internalTransactionId: string
}

export interface S_AvailableProcess{
    status: number,
    procesos: {
        IDPROCESO: number, 
        NOMBRE: string,
        FINICIO: Date,
        FFIN: Date
    }[];
    externalTransactionId: string,
    internalTransactionId: string
}
