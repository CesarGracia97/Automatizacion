import { Component } from '@angular/core';
import { CommunicationService } from '../../../services/views/communication.service';

@Component({
  selector: 'app-create-campanas-view',
  standalone: true,
  imports: [],
  templateUrl: './create-campanas-view.component.html',
  styleUrl: './create-campanas-view.component.css'
})
export class CreateCampanasViewComponent {

  state_modal: boolean | null = null

  constructor(private com: CommunicationService){}

  ngOnInit(): void {
    this.com.state_campana_modal$.subscribe(state => {this.state_modal = state})
  }
}
