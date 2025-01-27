import { Component } from '@angular/core';
import { ChangeProveedorViewComponent } from "./change-proveedor-view/change-proveedor-view.component";
import { CreateCampanasViewComponent } from "./create-campanas-view/create-campanas-view.component";
import { CreateProcesosViewComponent } from "./create-procesos-view/create-procesos-view.component";
import { UploadCobrosViewComponent } from "./upload-cobros-view/upload-cobros-view.component";
import { CommunicationService } from '../../services/views/communication.service';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-body-view',
  standalone: true,
  imports: [CommonModule, ChangeProveedorViewComponent, CreateCampanasViewComponent, CreateProcesosViewComponent, UploadCobrosViewComponent],
  templateUrl: './body-view.component.html',
  styleUrl: './body-view.component.css'
})
export class BodyViewComponent {

  cobros_view: boolean = false;
  campanas_view: boolean = false;
  transacciones_view: boolean = false;
  proceso_view: boolean = false;
  addgsup_view: boolean = false;

  constructor(private com: CommunicationService){}
  
  ngOnInit(): void {
    this.com.state_transaccion_modal$.subscribe(state => {this.transacciones_view = state});
    this.com.state_campana_modal$.subscribe(state => {this.campanas_view = state});
    this.com.state_cobranza_modal$.subscribe(state => {this.cobros_view = state});
    this.com.state_proceso_modal$.subscribe(state => {this.proceso_view = state});
    this.com.state_addgg_modal$.subscribe(state => { this.addgsup_view = state})
  }

  show_view(type: string){
    const validTypes = new Set(['cobranza', 'transaccion', 'campana', 'proceso', 'addgg']);
    if (validTypes.has(type)) {
      this.com.state_4_modal_visualization(true, type);
    } else {
      console.error("Ingresa la correcta carajo");
    }
  }
}
