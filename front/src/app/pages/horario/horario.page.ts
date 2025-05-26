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

@Component({
  selector: 'app-horario',
  templateUrl: './horario.page.html',
  styleUrls: ['./horario.page.scss'],
  standalone: true,
  imports: [IonicModule, CommonModule, FormsModule],
})
export class HorarioPage {
  empleados = [
    {
      dias: [
        { estado: '' },
        { estado: '' },
        { estado: '' },
        { estado: '' },
        { estado: '' },
      ],
    },
    {
      dias: [
        { estado: '' },
        { estado: '' },
        { estado: '' },
        { estado: '' },
        { estado: '' },
      ],
    },
    {
      dias: [
        { estado: '' },
        { estado: '' },
        { estado: '' },
        { estado: '' },
        { estado: '' },
      ],
    },
    {
      dias: [
        { estado: '' },
        { estado: '' },
        { estado: '' },
        { estado: '' },
        { estado: '' },
      ],
    },
    {
      dias: [
        { estado: '' },
        { estado: '' },
        { estado: '' },
        { estado: '' },
        { estado: '' },
      ],
    },
    {
      dias: [
        { estado: '' },
        { estado: '' },
        { estado: '' },
        { estado: '' },
        { estado: '' },
      ],
    },
  ];

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
    // Aquí podrías abrir un modal, popover, o navegar a otra página.
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
      // Navegación externa
      window.location.href = url;
    } else {
      // Navegación interna con Angular Router
      this.router.navigateByUrl(url);
    }
  }

  irPerfilAdmin() {
    window.location.href = 'http://localhost:8100/perfiladmin';
  }
}
