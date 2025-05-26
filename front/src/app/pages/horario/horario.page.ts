import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { IonicModule, ModalController } from '@ionic/angular';
import { NuevajornadaPage } from '../nuevajornada/nuevajornada.page';
import { Router } from '@angular/router';
import { addIcons } from 'ionicons';
import { UserService, HorarioDetalle } from '../../services/user.service';
import {
  peopleOutline,
  calendarOutline,
  cashOutline,
  barChartOutline,
} from 'ionicons/icons';

interface HorarioDetallado {
  id: string;
  correo: string;
  empresa: string;
  diaSemana: string;
  horaEntrada: string;
  horaSalida: string;
  observacion: string;
}

@Component({
  selector: 'app-horario',
  templateUrl: './horario.page.html',
  styleUrls: ['./horario.page.scss'],
  standalone: true,
  imports: [IonicModule, CommonModule, FormsModule],
})
export class HorarioPage {
  usuarioId: string = '';
  fecha: string = '';
  fechaListar: string = '';
  errorMensaje: string = '';
  horarioDetallado: HorarioDetalle[] = [];
  usuariosConHorario: any[] = [];

  constructor(
    private modalCtrl: ModalController,
    private router: Router,
    private userService: UserService
  ) {
    addIcons({
      peopleOutline,
      calendarOutline,
      cashOutline,
      barChartOutline,
    });
  }

  abrirPerfil() {
    console.log('Abriendo perfil...');
  }

  async abrirNuevaJornada() {
    const modal = await this.modalCtrl.create({
      component: NuevajornadaPage,
      cssClass: 'custom-modal-jornada',
    });
    await modal.present();
  }

  navegar(url: string) {
    if (url.startsWith('http')) {
      window.location.href = url;
    } else {
      this.router.navigateByUrl(url);
    }
  }

  irPerfilAdmin() {
    window.location.href = 'http://localhost:8100/perfiladmin';
  }

  buscarHorario() {
    if (!this.usuarioId || !this.fecha) {
      this.errorMensaje = 'Por favor complete todos los campos';
      return;
    }

    this.userService.obtenerHorario(this.usuarioId, this.fecha).subscribe({
      next: (horarios) => {
        this.horarioDetallado = horarios;
        this.errorMensaje = '';
      },
      error: (error) => {
        this.errorMensaje = 'Error al obtener el horario: ' + error.message;
        console.error('Error:', error);
      },
    });
  }

  listarUsuarios() {
    if (!this.fechaListar) {
      this.errorMensaje = 'Por favor ingrese una fecha para listar';
      return;
    }

    this.userService.listarUsuariosConHorarios(this.fechaListar).subscribe({
      next: (usuarios) => {
        this.usuariosConHorario = usuarios.map((usuario) => ({
          ...usuario,
          ...usuario.horarios[0], // Expandir el primer horario del usuario
        }));
        this.errorMensaje = '';
      },
      error: (error) => {
        this.errorMensaje = 'Error al listar usuarios: ' + error.message;
        console.error('Error:', error);
      },
    });
  }
}
