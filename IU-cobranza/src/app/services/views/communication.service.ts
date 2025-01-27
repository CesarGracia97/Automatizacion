import { Injectable } from '@angular/core';
import { Subject } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class CommunicationService {

  private state_principal_modal_Subject = new Subject<boolean>();
  state_principal_modal$ = this.state_principal_modal_Subject.asObservable();

  private state_cobranza_modal_Subject =  new Subject<boolean>();
  state_cobranza_modal$ = this.state_cobranza_modal_Subject.asObservable();

  private state_transaccion_modal_Subject =  new Subject<boolean>();
  state_transaccion_modal$ = this.state_transaccion_modal_Subject.asObservable();

  private state_proceso_modal_Subject =  new Subject<boolean>();
  state_proceso_modal$ = this.state_proceso_modal_Subject.asObservable();
  
  private state_campana_modal_Subject =  new Subject<boolean>();
  state_campana_modal$ = this.state_campana_modal_Subject.asObservable();

  private state_addgg_modal_Subject = new Subject<boolean>();
  state_addgg_modal$ = this.state_addgg_modal_Subject.asObservable();

  constructor() { }

  principal_state_modal_visualization(state: boolean){
    this.state_principal_modal_Subject.next(state);
  }

  state_4_modal_visualization(state: boolean, type: string){
    switch(type){
      case 'cobranza':
        this.state_cobranza_modal_Subject.next(state);
        break;
      case 'transaccion':
        this.state_transaccion_modal_Subject.next(state);
        break;
      case 'campana':
        this.state_campana_modal_Subject.next(state);
        break;
      case 'proceso':
        this.state_proceso_modal_Subject.next(state);
        break;
      case 'addgg':
        this.state_addgg_modal_Subject.next(state);
    }
  }
}
