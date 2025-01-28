import { Component } from '@angular/core';
import { CommunicationService } from '../../services/views/communication.service';
import { CommonModule } from '@angular/common';
import { IntermediateService } from '../../services/methods_mid/intermediate.service';
import { S_LastUpdate } from '../../interfaces/response/response_success.interface';

@Component({
  selector: 'app-ventana-modal',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './ventana-modal.component.html',
  styleUrl: './ventana-modal.component.css'
})
export class VentanaModalComponent {

  visual_message: boolean = true;
  visual_update: boolean = false;
  visual_loading: boolean = false;
  visual_message_final: boolean = false;
  visual_status: boolean | null = null;
  uploadedFiles: File | null = null;// Almacenamos los archivos seleccionados
  lastUpdateDate: string | null = null; // Variable para almacenar la fecha
  fecha: S_LastUpdate [] = []

  constructor( private comunication: CommunicationService, private mid: IntermediateService){}

  ngOnInit(): void {
    this.fetchLastUpdateDate();
  }

  fetchLastUpdateDate() {
    this.mid.mid_fecthdataLastUpdateSuplantacion().subscribe({
      next: (response) => {
        // Convertir la fecha al formato día-mes-año
        const date = new Date(response.fecha);
        date.setDate(date.getDate() + 1); // Sumar 1 día
        this.lastUpdateDate = date.toLocaleDateString('es-ES', {
          day: '2-digit',
          month: '2-digit',
          year: 'numeric',
        });
      },
      error: () => {
        console.error('Error al obtener la fecha de última actualización');
        this.lastUpdateDate = '-- / -- / --'; // Valor por defecto en caso de error
      }
    });
  }
  
  saltar() {
    this.comunication.principal_state_modal_visualization(false);
  }

  actualizar() {
    this.visual_message = false;
    this.visual_update = true;
  }
  
  onFileSelect(event: Event) {
    const input = event.target as HTMLInputElement;

    if (input.files && input.files.length > 0) {
      this.uploadedFiles = input.files[0]; // Obtén los archivos seleccionados
      this.visual_update = false;
      this.visual_loading = true; // Activa la animación de carga
      
      this.mid.mid_updloadExclutionFile(this.uploadedFiles).subscribe({
        next: () => {
          // Respuesta exitosa
          this.handleResponse(true);
        },
        error: () => {
          // Respuesta con error
          this.handleResponse(false);
        }
      });
    }
  }

  private handleResponse(success: boolean) {
    this.visual_loading = false;
    this.visual_status = success;
    this.visual_message_final = true;

    // Resetea los estados después de 3 segundos
    setTimeout(() => {
      this.visual_status = null;
      this.visual_message_final = false;
      this.saltar();
    }, 3000);
  }

}
