import { Injectable } from '@angular/core';
import { BehaviorSubject, Subject } from 'rxjs';
import { S_AvailableMonths } from '../../interfaces/response/response_success.interface';

@Injectable({
  providedIn: 'root'
})
export class DataStorageService {

  // BehaviorSubject inicializado con un valor vacío
  private dMesesHabilitados_Subject = new BehaviorSubject<S_AvailableMonths | null>(null);
  dMesesHabilitados_Subject$ = this.dMesesHabilitados_Subject.asObservable();

  constructor() {}

  // Método para actualizar los datos
  setAvailableMonths(data: S_AvailableMonths): void {
    this.dMesesHabilitados_Subject.next(data);
  }

  // Método para obtener el valor actual almacenado
  getAvailableMonths(): S_AvailableMonths | null {
    return this.dMesesHabilitados_Subject.getValue();
  }
}
