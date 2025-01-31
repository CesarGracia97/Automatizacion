import { Injectable } from '@angular/core';
import { BehaviorSubject, Subject } from 'rxjs';
import { S_AvailableMonths, S_AvailableProcess, S_ClientesSuspendidos } from '../../interfaces/response/response_success.interface';

@Injectable({
  providedIn: 'root'
})
export class DataStorageService {
  private dMesesHabilitados_Subject = new BehaviorSubject<S_AvailableMonths | null>(null);
  dMesesHabilitados$ = this.dMesesHabilitados_Subject.asObservable();

  private dProcesoshabilitados_Subject = new BehaviorSubject<S_AvailableProcess | null>(null)
  dProcesoshabilitados$ = this.dProcesoshabilitados_Subject.asObservable();

  private dClientesSuspendidos_Subject = new BehaviorSubject<S_ClientesSuspendidos | null>(null);
  dClientesSuspendidos = this.dClientesSuspendidos_Subject.asObservable();

  constructor() {}

  //Meses Habilitados
  // Método para actualizar los datos
  setAvailableMonths(data: S_AvailableMonths): void {
    this.dMesesHabilitados_Subject.next(data);
  }

  // Método para obtener el valor actual almacenado
  getAvailableMonths(): S_AvailableMonths | null {
    return this.dMesesHabilitados_Subject.getValue();
  }

  //Procesos Habilitados
  setAvailableProcesos(data: S_AvailableProcess): void {
    this.dProcesoshabilitados_Subject.next(data)
  }

  getAvailableProcesos(): S_AvailableProcess | null {
    return this.dProcesoshabilitados_Subject.getValue()
  }

  //Clientes Suspendidos Habilitados
  setClientesSuspendidos(data: S_ClientesSuspendidos): void {
    this.dClientesSuspendidos_Subject.next(data);
  }

  getClientesSuspendidos(): S_ClientesSuspendidos | null{
    return this.dClientesSuspendidos_Subject.getValue();
  }
}
