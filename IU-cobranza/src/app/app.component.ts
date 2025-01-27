import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { VentanaModalComponent } from './components/ventana-modal/ventana-modal.component';
import { BodyViewComponent } from './components/body-view/body-view.component';
import { CommunicationService } from './services/views/communication.service';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [VentanaModalComponent, BodyViewComponent, CommonModule],
  templateUrl: './app.component.html',
  styleUrl: './app.component.css'
})
export class AppComponent {
  title = 'IU-cobranza';
  state_modal: boolean |  null = null;

  constructor(
    private comunication: CommunicationService
  ){}

  ngOnInit(): void {
    this.state_modal = true
    this.comunication.state_principal_modal$.subscribe(state => {this.state_modal = state})
  }
}
