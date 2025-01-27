import { Injectable } from '@angular/core';
import { UuidgeneratorService } from '../../utils/uuidgenerator.service';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs/internal/Observable';
import { Update_File } from '../../interfaces/request/request_send.interface';

@Injectable({
  providedIn: 'root'
})
export class uploadFileService {

  constructor(private http: HttpClient, private  uuidService: UuidgeneratorService) { }

  uploadExclution (files: File): Observable<Update_File> {
    const formData = new FormData();
    formData.append('archivo', files)
    formData.append('channel', 'automatic-contrato-web');
    formData.append('externalTransactionId', this.uuidService.generateUUID());
    return this.http.post<Update_File>('http://127.0.0.1:2014/rest/m-automaticontratos-api/v1.0/put/upload/suplantacion',formData);
  }

  uploadCobranza(files: File): Observable<Update_File> {
    const formData = new FormData();
    formData.append('archivo', files)
    formData.append('channel', 'automatic-contrato-web');
    formData.append('externalTransactionId', this.uuidService.generateUUID());
    return this.http.post<Update_File>('http://127.0.0.1:2014/rest/m-automaticontratos-api/v1.0/post/upload/archivos',formData);
  }
}
