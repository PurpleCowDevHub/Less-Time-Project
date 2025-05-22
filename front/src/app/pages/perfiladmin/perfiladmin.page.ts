import { Component } from '@angular/core';
import { IonicModule } from '@ionic/angular';
import { FormsModule } from '@angular/forms'; 
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-perfiladmin',
  standalone: true,
  imports: [CommonModule, FormsModule, IonicModule],
  templateUrl: './perfiladmin.page.html',
  styleUrls: ['./perfiladmin.page.scss']
})
export class PerfiladminPage {
  abrirPerfil() {
    console.log('Abriendo perfil...');
    // Aquí podrías abrir un modal, popover, o navegar a otra página.
  }
}

