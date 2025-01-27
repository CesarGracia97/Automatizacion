import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { UuidgeneratorService } from '../../utils/uuidgenerator.service';
import { Observable } from 'rxjs';
import { S_Charge } from '../../interfaces/response/response_success.interface';

@Injectable({
  providedIn: 'root'
})
export class SendDataService {

  constructor(private http: HttpClient, private  uuidService: UuidgeneratorService) { }

  senDataCreateProcess(data:{ [key: string]: any }): Observable<S_Charge>{
    const headers = new HttpHeaders({ 'Content-Type': 'application/json' });
    const body = {
      'channel': 'automatic-contrato-web',
      'externalTransactionId': this.uuidService.generateUUID(),
      'proceso': data
    };
    return this.http.post<S_Charge>('http://127.0.0.1:2014/rest/m-automaticontratos-api/v1.0/post/create/procesos', body, { headers });
  }

  sendDataCreateCampana(data:{ [key: string]: any }, idproceso: number): Observable<S_Charge> {
    const headers = new HttpHeaders({ 'Content-Type': 'application/json' });
    const body = {
      'channel': 'automatic-contrato-web',
      'externalTransactionId': this.uuidService.generateUUID(),
      'campana': data,
      'idproceso': idproceso
    };
    return this.http.post<S_Charge>('http://127.0.0.1:2014/rest/m-automaticontratos-api/v1.0/post/create/campanas', body, { headers });
  }
}
