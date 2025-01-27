import { Component } from '@angular/core';
import { CommunicationService } from '../../../services/views/communication.service';
import { CommonModule } from '@angular/common';
import { IntermediateService } from '../../../services/methods_mid/intermediate.service';

@Component({
  selector: 'app-upload-cobros-view',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './upload-cobros-view.component.html',
  styleUrl: './upload-cobros-view.component.css'
})
export class UploadCobrosViewComponent {

  visual_update: boolean = true;
  visual_loading: boolean = false;
  visual_message_final: boolean = false;
  visual_status: boolean | null = null;
  uploadedFiles: File | null = null;// Almacenamos los archivos seleccionados

  constructor( private mid: IntermediateService, private communacation: CommunicationService ){}

  onFileSelect(event: Event) {
    const input = event.target as HTMLInputElement;

    if (input.files && input.files.length > 0) {
      this.uploadedFiles = input.files[0]; // Obtén los archivos seleccionados
      this.visual_update = false;
      this.visual_loading = true; // Activa la animación de carga
      
      this.mid.mid_uploadCobranzaFile(this.uploadedFiles).subscribe({
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
      this.visualState(success)
    }, 3000);
  }

  visualState(success: boolean){
    this.communacation.state_4_modal_visualization(success, "cobranza")
  }
}
