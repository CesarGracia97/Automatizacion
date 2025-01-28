import { Component } from '@angular/core';
import { CommunicationService } from '../../../services/views/communication.service';
import { IntermediateService } from '../../../services/methods_mid/intermediate.service';
import { DataStorageService } from '../../../services/data_storage/data-storage.service';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-create-campanas-view',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './create-campanas-view.component.html',
  styleUrl: './create-campanas-view.component.css'
})
export class CreateCampanasViewComponent {

  state_modal: boolean | null = null;

  constructor(private com: CommunicationService, private mid: IntermediateService, private ds: DataStorageService){}

  ngOnInit(): void {
    this.com.state_campana_modal$.subscribe(state => {this.state_modal = state});
  }
}
