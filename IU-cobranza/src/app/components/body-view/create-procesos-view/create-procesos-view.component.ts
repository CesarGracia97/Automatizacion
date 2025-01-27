import { Component } from '@angular/core';
import { CommunicationService } from '../../../services/views/communication.service';
import { IntermediateService } from '../../../services/methods_mid/intermediate.service';

@Component({
  selector: 'app-create-procesos-view',
  standalone: true,
  imports: [],
  templateUrl: './create-procesos-view.component.html',
  styleUrl: './create-procesos-view.component.css'
})
export class CreateProcesosViewComponent {

  state_modal: boolean | null = null
  

  constructor(private com: CommunicationService, private mid: IntermediateService){}

  ngOnInit(): void {
    this.getDataMeses();
  }

  getDataMeses(){
    this.mid.mid_fetchdataAvailableMonths()
  }

  generateLimitMounthProcess(){

  }

  sendDataProcesosCreate(nombre: string, fecha_inicio: Date, fecha_fin: Date){
    if (nombre && fecha_fin && fecha_inicio){
      
    }


  }
}
