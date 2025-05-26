import { Component } from '@angular/core';
import { IonicModule } from '@ionic/angular';
import { FormsModule } from '@angular/forms'; 
import { CommonModule } from '@angular/common';
import { addIcons } from 'ionicons';
import { 
  peopleOutline, 
  calendarOutline, 
  cashOutline,
  barChartOutline 
} from 'ionicons/icons';

@Component({
  selector: 'app-perfiladmin',
  standalone: true,
  imports: [CommonModule, FormsModule, IonicModule],
  templateUrl: './perfiladmin.page.html',
  styleUrls: ['./perfiladmin.page.scss']
})
export class PerfiladminPage {
  constructor() {
    addIcons({
      peopleOutline,
      calendarOutline,
      cashOutline,
      barChartOutline
    });
  }

  abrirPerfil() {
    console.log('Abriendo perfil...');
    // Aquí podrías abrir un modal, popover, o navegar a otra página.
  }

  irAPrincipal() {
    window.location.href = 'http://localhost:8100/principal';
  }

  irAEmpleados() {
    window.location.href = 'http://localhost:8100/listausuarios';
  }

  irACalendario() {
    window.location.href = 'http://localhost:8100/horario';
  }

  irANomina() {
    window.location.href = 'http://localhost:8100/nomina';
  }

  irAPerfilAdmin() {
    window.location.href = 'http://localhost:8100/perfiladmin';
  }

  irADatos() {
    window.location.href = 'http://localhost:8100/datos';
  }
}

