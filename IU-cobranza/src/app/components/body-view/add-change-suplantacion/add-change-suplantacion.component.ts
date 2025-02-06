import { CommonModule } from '@angular/common';
import { Component, OnInit } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { CommunicationService } from '../../../services/views/communication.service';
import { IntermediateService } from '../../../services/methods_mid/intermediate.service';
import { S_Charge, S_ClientesSuspendidos } from '../../../interfaces/response/response_success.interface';
import { DataStorageService } from '../../../services/data_storage/data-storage.service';

@Component({
  selector: 'app-add-change-suplantacion',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './add-change-suplantacion.component.html',
  styleUrl: './add-change-suplantacion.component.css'
})
export class AddChangeSuplantacionComponent implements OnInit {

  state_modal: boolean | null = null;

  agg: boolean | null = null; mod: boolean | null = null; //mostrar sectores

  state_response: boolean | null = null; state_loading: boolean | null = null; message_text: string | null = null;

  c_suplentes: { cliente: string, contrato: number, cuenta: number, detalle: string, fecha_exclusion: string, isvalid: string }[] =[]
  clienteSeleccionado: { cliente: string, contrato: number, cuenta: number, detalle: string, fecha_exclusion: string, isvalid: string } | null = null;
  contratocliente: number | null = null; 


  //variables para nuevos suspendidos
  agg_cliente: string | null = null; agg_contrato: number = 0; agg_cuenta: number = 0; 
  agg_detalle: string | null = null; agg_fexclusion: string | null = null;
  
  constructor(
    private com: CommunicationService, private mid: IntermediateService, private ds: DataStorageService
  ){ }

  ngOnInit(): void {
    this.ds.dClientesSuspendidos$.subscribe(data => {if (data) this.c_suplentes = data.suspendidos})
    this.getDataSuplantantes();
  }

  getDataSuplantantes(){
    this.mid.mid_fetchdataClientesSuspendidos().subscribe();
  }

  mostrarSectorBody(sector: string){
    const permitidos = ['AGG', 'MOD']
    if (permitidos.includes(sector)){
      switch(sector){
        case 'AGG':
          this.mod = false; this.agg = true;
          break
        case 'MOD':
          this.agg = false; this.mod = true;
          break;
      }
    } else {
      alert('NO TE PASES DE LISTO CHIC@, ESO NO EXISTE.');
      return;
    }
  }

  sendDataCreateNewSuspendido(){
    if(!this.agg_cliente || !this.agg_contrato || !this.agg_cuenta || ! this.agg_detalle || !this.agg_fexclusion){
      alert("COMPLETE TODOS LOS CAMPOS");
      return;
    }
    const cliente: { [key: string]: any } = { cliente: this.agg_cliente, contrato: this.agg_contrato, cuenta: this.agg_cuenta, detalle: this.agg_detalle, fecha_exclusion: this.agg_fexclusion };
    this.state_loading = true; // Muestra la animación de carga
    this.state_response = null; // Oculta cualquier mensaje previo
    this.message_text = null; // Limpia el mensaje previo
    this.mid.mid_sendDataClientesSuspendidos(cliente).subscribe({
      next: (response: S_Charge) => {
        this.state_loading = false; // Oculta la animación de carga
        this.state_response = true; // Muestra el div del mensaje
        this.message_text = response.message; // Almacena el mensaje en la variable
      },
      error: (errorResponse: any) => {
        this.state_loading = false; // Oculta la animación de carga
        this.state_response = true; // Muestra el div del mensaje
        this.message_text =
          errorResponse.error.message || 'Ocurrió un error inesperado.'; // Maneja el mensaje de error
      },
    });
    this.getDataSuplantantes();
  }

  closeModal():void {
    this.com.state_4_modal_visualization(false, 'addgg')
  }
}
