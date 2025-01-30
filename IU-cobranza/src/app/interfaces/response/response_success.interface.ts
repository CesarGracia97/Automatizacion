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
        idproceso: number, 
        name: string,
        fiproceso: Date,
        ffproceso: Date
    }[];
    externalTransactionId: string,
    internalTransactionId: string
}

export interface S_ClientesSuspendidos{
    status: number,
    suspendidos: {
        cliente: string,
        contrato: number,
        cuenta: number,
        detalle: string,
        fecha_exclusion: string,
        isvalid: string
    }[];
    externalTransactionId: string,
    internalTransactionId: string
}
