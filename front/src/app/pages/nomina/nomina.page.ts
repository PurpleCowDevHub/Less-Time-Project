import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { IonicModule } from '@ionic/angular';

@Component({
  selector: 'app-nomina',
  templateUrl: './nomina.page.html',
  styleUrls: ['./nomina.page.scss'],
  standalone: true,
  imports: [IonicModule, CommonModule, FormsModule],
})
export class NominaPage {
  grupos = [
    {
      titulo: 'Sueldos y salarios',
      empleados: 52,
      percepciones: '$2,410,021.00',
      deducciones: '$805,139.00',
      total: '$1,604,882.00',
    },
    {
      titulo: 'Asimilados',
      empleados: 78,
      percepciones: '$1,645,015.00',
      deducciones: '$702,513.00',
      total: '$938,153.00',
    },
  ];

  idNomina: string = '';
  usuarioId: string = '';
  horasTrabajadas: number = 0;
  diasIncapacidad: number = 0;
  horasExtra: number = 0;
  bonificacion: number = 0;
  periodoPago: string = '';
  idEnvioNomina: string = '';

  irAPrincipal() {
    window.location.href = 'http://localhost:8101/principal';
  }

  irAEmpleados() {
    window.location.href = 'http://localhost:8100/listausuarios';
  }

  irACalendario() {
    window.location.href = 'http://localhost:8101/horario';
  }

  irANomina() {
    window.location.href = 'http://localhost:8101/nomina';
  }

  irAPerfilAdmin() {
    window.location.href = 'http://localhost:8100/perfiladmin';
  }

  guardarNomina() {
    console.log(`Guardando nómina con ID: ${this.idNomina}`);
  }

  guardarDatosNomina() {
    console.log('Datos para nómina:', {
      usuarioId: this.usuarioId,
      horasTrabajadas: this.horasTrabajadas,
      diasIncapacidad: this.diasIncapacidad,
      horasExtra: this.horasExtra,
      bonificacion: this.bonificacion,
      periodoPago: this.periodoPago,
    });
  }

  enviarNominaConDatos() {
    console.log('Enviando nómina con ID:', this.idEnvioNomina);
  }

  enviarNomina() {
    console.log('Enviar nómina básico con ID:', this.idNomina);
  }
}


