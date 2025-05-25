import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ModalController, IonicModule } from '@ionic/angular';

@Component({
  selector: 'app-nuevajornada',
  templateUrl: './nuevajornada.page.html',
  styleUrls: ['./nuevajornada.page.scss'],
  standalone: true,
  imports: [IonicModule, CommonModule, FormsModule]
})
export class NuevajornadaPage implements OnInit {
  dia: string = '';
  mes: string = '';
  anio: string = '';
  maxAnio: number = new Date().getFullYear();

  // Nuevas propiedades para horas
  horaEntrada: string = '';
  horaSalida: string = '';

  constructor(private modalCtrl: ModalController) {}

  ngOnInit() {}

  cerrarModal() {
    this.modalCtrl.dismiss();
  }

  validarDia() {
    if (this.dia) {
      const dayNum = parseInt(this.dia, 10);
      if (dayNum < 1) this.dia = '1';
      if (dayNum > 31) this.dia = '31';
    }
  }

  validarAnio() {
    if (this.anio) {
      const yearNum = parseInt(this.anio, 10);
      if (yearNum < 1950) this.anio = '1950';
      if (yearNum > this.maxAnio) this.anio = this.maxAnio.toString();
    }
  }

  obtenerFecha(): Date | null {
    if (this.dia && this.mes && this.anio) {
      const fechaStr = `${this.anio}-${this.mes}-${this.dia}`;
      const fecha = new Date(fechaStr);
      return isNaN(fecha.getTime()) ? null : fecha;
    }
    return null;
  }
}
