import { Component } from '@angular/core';
import { CommunicationService } from '../../../services/views/communication.service';
import { IntermediateService } from '../../../services/methods_mid/intermediate.service';
import { CommonModule } from '@angular/common';
import { DataStorageService } from '../../../services/data_storage/data-storage.service';
import { FormsModule } from '@angular/forms';
import { S_Charge } from '../../../interfaces/response/response_success.interface';

@Component({
  selector: 'app-create-procesos-view',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './create-procesos-view.component.html',
  styleUrl: './create-procesos-view.component.css'
})
export class CreateProcesosViewComponent {

  state_modal: boolean | null = null
  state_response: boolean | null = null
  state_loading: boolean | null = null
  message_text: string | null = null;

  meses: { nombre: string; mes: number; ano: number }[] = [];
  minDate: string | null = null; maxDate: string | null = null;
  mesSel: string | null = null; 
  name: string =''; finicio: string = ''; ffin: string = ''; mes: number | null = null;

  constructor(private com: CommunicationService, private mid: IntermediateService, private ds: DataStorageService){}

  ngOnInit(): void {
    this.getDataMeses();
    this.ds.dMesesHabilitados_Subject$.subscribe(data => { if (data)this.meses = data.meses; });
  }

  getDataMeses(): void {
    this.mid.mid_fetchdataAvailableMonths().subscribe();
  }

  setLimits(): void {
    if (this.mesSel) {
      const [mes, ano] = this.mesSel.split('-').map(Number);
      const firstDay = new Date(ano, mes - 1, 1);
      const lastDay = new Date(ano, mes, 0);

      this.minDate = this.formatDate(firstDay);
      this.maxDate = this.formatDate(lastDay);
    }
  }
  
  private formatDate(date: Date): string {
    const year = date.getFullYear();
    const month = (date.getMonth() + 1).toString().padStart(2, '0');
    this.mes = parseInt(month);
    const day = date.getDate().toString().padStart(2, '0');
    return `${year}-${month}-${day}`;
  }

  createProceso(): void {
    if (!this.name || !this.finicio || !this.ffin || !this.mes) {
      alert('Por favor, completa todos los campos antes de continuar.');
      return;
    }
    if (new Date(this.finicio) > new Date(this.ffin)) {
      alert('La fecha de inicio no puede ser mayor que la fecha de finalización.');
      return;
    }
    const proceso: { [key: string]: any } = { nombre: this.name, finicio: this.finicio, ffin: this.ffin, mes: this.mes  };
    this.state_loading = true; // Muestra la animación de carga
    this.state_response = null; // Oculta cualquier mensaje previo
    this.message_text = null; // Limpia el mensaje previo
    this.mid.mid_sendDataProcess(proceso).subscribe({
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
  }
}
