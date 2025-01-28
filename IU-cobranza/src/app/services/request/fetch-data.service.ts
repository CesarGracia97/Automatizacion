import { Injectable } from '@angular/core';
import { UuidgeneratorService } from '../../utils/uuidgenerator.service';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs/internal/Observable';
import { S_AvailableMonths, S_AvailableProcess, S_LastUpdate } from '../../interfaces/response/response_success.interface';

@Injectable({
  providedIn: 'root'
})
export class FetchDataService {

  constructor(private http: HttpClient, private  uuidService: UuidgeneratorService) { }

  query_LastUpdateSuplantacion(): Observable <S_LastUpdate> {
    const headers = new HttpHeaders({ 'Content-Type': 'application/json' });
    const body = {
      'channel': 'automatic-contrato-web',
      'externalTransactionId': this.uuidService.generateUUID(),
      'peticion': "suplantacion"
    };
    return this.http.post<S_LastUpdate>('http://127.0.0.1:2014/rest/m-automaticontratos-api/v1.0/get/queries', body, { headers });
  }

  query_AvailableMonths(): Observable <S_AvailableMonths>{
    const headers = new HttpHeaders({ 'Content-Type': 'application/json' });
    const body = {
      'channel': 'automatic-contrato-web',
      'externalTransactionId': this.uuidService.generateUUID(),
      'peticion': "meses-disponibles"
    };
    return this.http.post<S_AvailableMonths>('http://127.0.0.1:2014/rest/m-automaticontratos-api/v1.0/get/queries', body, { headers });
  }

  query_AvailableProcess(): Observable<S_AvailableProcess>{
    const headers = new HttpHeaders({ 'Content-Type': 'application/json' });
    const body = {
      'channel': 'automatic-contrato-web',
      'externalTransactionId': this.uuidService.generateUUID(),
      'peticion': "proceso"
    };
    return this.http.post<S_AvailableProcess>('http://127.0.0.1:2014/rest/m-automaticontratos-api/v1.0/get/queries', body, { headers });
  }
}
