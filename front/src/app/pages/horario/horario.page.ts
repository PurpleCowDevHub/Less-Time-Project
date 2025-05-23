import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { IonicModule, ModalController } from '@ionic/angular'; // <-- SE AÑADE ModalController
import { NuevajornadaPage } from '../nuevajornada/nuevajornada.page'; // <-- SE AÑADE IMPORTACIÓN

@Component({
  selector: 'app-horario',
  templateUrl: './Horario.page.html',
  styleUrls: ['./Horario.page.scss'],
  standalone: true,
  imports: [IonicModule, CommonModule, FormsModule],
})
export class HorarioPage {
  empleados = [
    {
      dias: [
        { avatar: 'assets/avatar1.png', estado: '8:59 - 13:45' },
        { estado: '8:59 - 13:45' },
        { estado: 'Día Festivo' },
        { estado: 'Incapacidad' },
        { estado: '8:59 - 13:45' },
      ],
    },
    {
      dias: [
        { avatar: 'assets/avatar2.png', estado: '8:59 - 13:45' },
        { estado: '8:59 - 13:45' },
        { estado: 'Día Festivo' },
        { estado: '8:59 - 13:45' },
        { estado: 'Incapacidad' },
      ],
    },
    {
      dias: [
        { avatar: 'assets/avatar3.png', estado: '8:59 - 13:45' },
        { estado: 'Vacaciones' },
        { estado: 'Día Festivo' },
        { estado: '8:59 - 13:45' },
        { estado: '8:59 - 13:45' },
      ],
    },
    {
      dias: [
        { avatar: 'assets/avatar4.png', estado: '7:00 - 12:00' },
        { estado: '7:00 - 12:00' },
        { estado: '8:00 - 14:00' },
        { estado: 'Vacaciones' },
        { estado: '8:00 - 14:00' },
      ],
    },
    {
      dias: [
        { avatar: 'assets/avatar5.png', estado: 'Incapacidad' },
        { estado: '8:30 - 12:30' },
        { estado: 'Vacaciones' },
        { estado: 'Día Festivo' },
        { estado: '8:30 - 12:30' },
      ],
    },
    {
      dias: [
        { avatar: 'assets/avatar6.png', estado: 'Día Festivo' },
        { estado: 'Incapacidad' },
        { estado: '8:00 - 14:00' },
        { estado: '8:00 - 14:00' },
        { estado: 'Vacaciones' },
      ],
    },
  ];

  constructor(private modalCtrl: ModalController) {} // <-- SE AÑADE CONSTRUCTOR

  abrirPerfil() {
    console.log('Abriendo perfil...');
    // Aquí podrías abrir un modal, popover, o navegar a otra página.
  }

  async abrirNuevaJornada() { // <-- SE AÑADE FUNCIÓN PARA ABRIR MODAL
    const modal = await this.modalCtrl.create({
      component: NuevajornadaPage,
      cssClass: 'custom-modal-jornada',
    });
    await modal.present();
  }
}