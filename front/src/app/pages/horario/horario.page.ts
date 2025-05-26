import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { IonicModule, ModalController } from '@ionic/angular';
import { NuevajornadaPage } from '../nuevajornada/nuevajornada.page';
import { Router } from '@angular/router';
import { addIcons } from 'ionicons';
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

  usuariosConHorario: Array<{
    id: string;
    correo: string;
    empresa: string;
    diaSemana: string;
    horaEntrada: string;
    horaSalida: string;
    observacion: string;
  }> = [];

  horarioDetallado: HorarioDetallado | null = null;

  constructor(private modalCtrl: ModalController, private router: Router) {
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
    console.log('Buscando horario para Usuario ID:', this.usuarioId, 'en fecha:', this.fecha);
    // Implementar la lógica para obtener horario aquí

    // Aquí deberías hacer tu llamada al servicio para obtener los datos
    // Por ahora simularemos datos de ejemplo
    this.horarioDetallado = {
      id: this.usuarioId,
      correo: 'usuario@ejemplo.com',
      empresa: 'Empresa Ejemplo',
      diaSemana: 'Lunes',
      horaEntrada: '08:00 AM',
      horaSalida: '05:00 PM',
      observacion: 'Sin novedades'
    };
  }

  listarUsuarios() {
    if (!this.fechaListar) {
      alert('Por favor ingresa una fecha para listar.');
      return;
    }

    console.log('Listando usuarios con horarios para la fecha:', this.fechaListar);

    // Simulación de datos
    this.usuariosConHorario = [
      {
        id: 'U001',
        correo: 'usuario1@example.com',
        empresa: 'Empresa A',
        diaSemana: 'Lunes',
        horaEntrada: '08:00 AM',
        horaSalida: '05:00 PM',
        observacion: 'Sin novedades',
      },
      {
        id: 'U002',
        correo: 'usuario2@example.com',
        empresa: 'Empresa B',
        diaSemana: 'Lunes',
        horaEntrada: '09:00 AM',
        horaSalida: '06:00 PM',
        observacion: 'Reunión por la tarde',
      },
    ];
  }
}
