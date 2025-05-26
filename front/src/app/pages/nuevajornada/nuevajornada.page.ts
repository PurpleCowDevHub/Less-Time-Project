import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ModalController, IonicModule, ToastController } from '@ionic/angular';
import { UserService } from 'src/app/services/user.service';

@Component({
  selector: 'app-nuevajornada',
  templateUrl: './nuevajornada.page.html',
  styleUrls: ['./nuevajornada.page.scss'],
  standalone: true,
  imports: [IonicModule, CommonModule, FormsModule],
})
export class NuevajornadaPage {
  dia: string = '';
  mes: string = '';
  anio: string = '';
  maxAnio: number = new Date().getFullYear();

  usuario: string = '';
  observacion: string = '';
  horaEntrada: string = '';
  horaSalida: string = '';
  diasSeleccionados: string[] = [];

  constructor(
    private modalCtrl: ModalController,
    private userService: UserService,
    private toastCtrl: ToastController
  ) {}

  cerrarModal() {
    this.modalCtrl.dismiss();
  }

  validarDia() {
    const d = parseInt(this.dia);
    if (d < 1) this.dia = '1';
    if (d > 31) this.dia = '31';
  }

  validarAnio() {
    const y = parseInt(this.anio);
    if (y < 1950) this.anio = '1950';
    if (y > this.maxAnio) this.anio = this.maxAnio.toString();
  }

  toggleDia(dia: string, event: any) {
    if (event.target.checked) {
      this.diasSeleccionados.push(dia);
    } else {
      this.diasSeleccionados = this.diasSeleccionados.filter(d => d !== dia);
    }
  }

  obtenerFecha(): string | null {
    if (this.dia && this.mes && this.anio) {
      return `${this.anio}-${this.mes}-${this.dia}`;
    }
    return null;
  }

  guardarJornada() {
    const fecha = this.obtenerFecha();
    if (!fecha || !this.usuario || !this.horaEntrada || !this.horaSalida || this.diasSeleccionados.length === 0) {
      this.mostrarToast('Completa todos los campos requeridos.');
      return;
    }

    for (let dia of this.diasSeleccionados) {
      const payload = {
        usuario_id: this.usuario,
        dia_semana: dia,
        hora_entrada: this.horaEntrada,
        hora_salida: this.horaSalida,
        observacion: this.observacion,
        fecha: fecha
      };

      this.userService.asignarHorario(payload).subscribe({
        next: () => this.mostrarToast(`Horario para ${dia} guardado.`),
        error: () => this.mostrarToast(`Error al guardar jornada para ${dia}.`)
      });
    }

    this.modalCtrl.dismiss();
  }

  async mostrarToast(msg: string) {
    const toast = await this.toastCtrl.create({
      message: msg,
      duration: 2000,
      position: 'bottom',
    });
    toast.present();
  }
}

