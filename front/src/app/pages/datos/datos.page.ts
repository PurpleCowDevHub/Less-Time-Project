import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import {
  IonContent,
  IonHeader,
  IonTitle,
  IonToolbar,
  IonList,
  IonItem,
  IonIcon,
  IonButton,
  IonAvatar
} from '@ionic/angular/standalone';

@Component({
  selector: 'app-datos',
  templateUrl: './datos.page.html',
  styleUrls: ['./datos.page.scss'],
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,
    IonContent,
    IonHeader,
    IonTitle,
    IonToolbar,
    IonList,
    IonItem,
    IonIcon,
    IonButton,
    IonAvatar
  ]
})
export class DatosPage implements OnInit {

  constructor() { }

  ngOnInit() { }

  irAPrincipal() {
    window.location.href = 'http://localhost:8100/home';
  }

  irAEmpleados() {
    window.location.href = 'http://localhost:8100/empleados';
  }

  irACalendario() {
    window.location.href = 'http://localhost:8100/calendario';
  }

  irANomina() {
    window.location.href = 'http://localhost:8100/nomina';
  }

  irAPerfilAdmin() {
    window.location.href = 'http://localhost:8100/perfiladmin';
  }

}
