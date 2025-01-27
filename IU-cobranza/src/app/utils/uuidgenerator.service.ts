import { Injectable } from '@angular/core';
import { v4 as uuidv4 } from 'uuid'; // Importamos la función para generar UUID v4

@Injectable({
  providedIn: 'root'
})
export class UuidgeneratorService {

  constructor() { }

  // Método para generar un UUID
  generateUUID(): string {
    return uuidv4();
  }
}
