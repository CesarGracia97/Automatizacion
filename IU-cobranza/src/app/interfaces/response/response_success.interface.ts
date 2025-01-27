export interface S_LastUpdate{
    status: number,
    fecha: Date,
    externalTransactionId: string,
    internalTransactionId: string
}

export interface S_AvailableMonths{
    status: number,
    meses: string[],
    externalTransactionId: string,
    internalTransactionId: string
}

export interface S_Charge{
    status: number,
    message: string,
    externalTransactionId: string,
    internalTransactionId: string
}
