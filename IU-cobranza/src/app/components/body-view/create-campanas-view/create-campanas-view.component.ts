import { Component } from '@angular/core';
import { CommunicationService } from '../../../services/views/communication.service';
import { IntermediateService } from '../../../services/methods_mid/intermediate.service';
import { DataStorageService } from '../../../services/data_storage/data-storage.service';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { S_Charge } from '../../../interfaces/response/response_success.interface';

@Component({
  selector: 'app-create-campanas-view',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './create-campanas-view.component.html',
  styleUrl: './create-campanas-view.component.css'
})
export class CreateCampanasViewComponent {

  state_modal: boolean | null = null; // modal encendida

  state_response: boolean | null = null; state_loading: boolean | null = null;  message: string | null = null; //estados de Respuesta

  idproceso: number = 0; name: string | null = ''; finic: string = ''; ffinc: string  = ''; descu: number | null = null//variables de campaña

  minDate: string | null = null; minFinDate: string | null = null; maxDate: string | null = null; // variables para fecha

  procesos: { idproceso: number, name: string, fiproceso: Date, ffproceso: Date }[] = []
  procsele: any = null;

  constructor(private com: CommunicationService, private mid: IntermediateService, private ds: DataStorageService){}

  ngOnInit(): void {
    this.getDataProcesos();
    this.com.state_campana_modal$.subscribe(state => {this.state_modal = state});
    this.ds.dProcesoshabilitados$.subscribe(data => {if(data) this.procesos = data.procesos})
  }

  private getDataProcesos(): void {
    this.mid.mid_fetchdataAvailableProcess().subscribe();
  }

  setLimitsDate(){
    if(this.procsele){
      this.minDate = this.formatDate(this.procsele.fiproceso);
      this.maxDate = this.formatDate(this.procsele.ffproceso);
      this.idproceso = this.procsele.idproceso
    }
  }

  setLimitsDateFin(){
    if (this.finic) {
      this.minFinDate = this.finic; // La fecha mínima de finalización es la fecha de inicio seleccionada
    }
  }
  
  createCampana():void {
    if( !this.name || !this.descu || !this.idproceso || !this.ffinc || !this.finic ){
      this.state_response = true;
      this.message = 'Por favor, completa todos los campos antes de continuar.'
      alert('Por favor, completa todos los campos antes de continuar.');
      return;
    }
    if(new Date(this.finic) > new Date(this.ffinc)){
      this.state_response = true;
       this.message = 'La fecha de inicio no puede ser mayor que la fecha de finalización.'
      alert('La fecha de inicio no puede ser mayor que la fecha de finalización.');
      return;
    }
    const campana:  { [key: string]: any }  = { nombre: this.name, descuento: this.descu, finicio: this.finic, ffin: this.ffinc }
    this.state_loading = true;
    this.state_response = null;
    this.message = null;
    this.mid.mid_sendDataCampana(campana, this.idproceso).subscribe({
      next: (response: S_Charge) => {
        this.state_loading = false; // Oculta la animación de carga
        this.state_response = true; // Muestra el div del mensaje
        this.message = response.message; // Almacena el mensaje en la variable
      },
      error: (errorResponse: any) => {
        this.state_loading = false; // Oculta la animación de carga
        this.state_response = true; // Muestra el div del mensaje
        this.message =
        errorResponse.error.message || 'Ocurrió un error inesperado.'; // Maneja el mensaje de error
      },
    });
  }  
  
  closeModal():void {
    this.com.state_4_modal_visualization(false, 'campana')
  }

  private formatDate(date: Date): string {
    return new Date(date).toISOString().split('T')[0];
  }
}
