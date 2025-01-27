import { Component } from '@angular/core';
import { CommunicationService } from '../../../services/views/communication.service';

@Component({
  selector: 'app-change-proveedor-view',
  standalone: true,
  imports: [],
  templateUrl: './change-proveedor-view.component.html',
  styleUrl: './change-proveedor-view.component.css'
})
export class ChangeProveedorViewComponent {

  state_modal: boolean | null = null

  constructor(private com: CommunicationService){}

  ngOnInit(): void {
    this.com.state_transaccion_modal$.subscribe(state => {this.state_modal = state})
  }
}
