import { Injectable } from '@angular/core';
import { uploadFileService } from '../request/upload-file.service';
import { S_AvailableMonths, S_Charge, S_LastUpdate } from '../../interfaces/response/response_success.interface';
import { Observable } from 'rxjs/internal/Observable';
import { FetchDataService } from '../request/fetch-data.service';
import { Update_File } from '../../interfaces/request/request_send.interface';
import { SendDataService } from '../request/sendata.service';

@Injectable({
  providedIn: 'root'
})
export class IntermediateService {

  constructor(private upload: uploadFileService, private fetchdata: FetchDataService, private sendData: SendDataService) { }

  mid_updloadExclutionFile(file: File): Observable<Update_File> {
    return this.upload.uploadExclution(file);
  }

  mid_uploadCobranzaFile(file: File): Observable<Update_File> {
    return  this.upload.uploadCobranza(file);
  }

  mid_fecthdataLastUpdateSuplantacion():Observable<S_LastUpdate>{
    return this.fetchdata.query_LastUpdateSuplantacion();
  }

  mid_fetchdataAvailableMonths(): Observable<S_AvailableMonths>{
    return this.fetchdata.query_AvailableMonths();
  }

  mid_sendDataProcess(data: { [key: string]: any }): Observable<S_Charge>{
    return this.sendData.senDataCreateProcess(data);
  }

  mid_sendDataCampana(data:{ [key: string]: any }, idproceso: number): Observable<S_Charge>{
    return this.sendData.sendDataCreateCampana(data, idproceso)
  }
}
