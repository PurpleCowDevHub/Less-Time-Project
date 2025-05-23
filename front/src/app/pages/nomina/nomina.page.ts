import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ModalController, IonicModule } from '@ionic/angular';
import { ReactiveFormsModule } from '@angular/forms';


@Component({
  selector: 'app-nomina',
  templateUrl: './nomina.page.html',
  styleUrls: ['./nomina.page.scss'],
  standalone: true,
  imports: [IonicModule, CommonModule],
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

  abrirPerfil() {
    console.log('Abriendo perfil...');
  }
}

