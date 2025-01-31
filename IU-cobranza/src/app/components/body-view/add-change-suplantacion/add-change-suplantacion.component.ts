import { CommonModule } from '@angular/common';
import { Component, OnInit } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { CommunicationService } from '../../../services/views/communication.service';

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

  //variables para nuevos suspendidos
  agg_cliente: string | null = null; agg_contrato: number = 0; agg_cuenta: number = 0; 
  agg_detalle: string | null = null; agg_fexclusion: string | null = null;
  
  constructor(private com: CommunicationService){ }

  ngOnInit(): void {
    this.com.state_addgg_modal$.subscribe()
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
    }
  }

  sendDataCreateNewSuspendido(){

  }

  closeModal():void {
    this.com.state_4_modal_visualization(false, 'addgg')
  }
}
