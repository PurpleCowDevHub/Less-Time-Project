import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { IonicModule } from '@ionic/angular';
import { Router } from '@angular/router';
import { addIcons } from 'ionicons';
import {
  mailOutline,
  chatbubblesOutline,
  notificationsOutline,
  logOutOutline
} from 'ionicons/icons';

@Component({
  selector: 'app-principal',
  templateUrl: './principal.page.html',
  styleUrls: ['./principal.page.scss'],
  standalone: true,
  imports: [IonicModule, CommonModule, FormsModule],
})
export class PrincipalPage implements OnInit {
    usuario: string = '';
  mostrarReportes: boolean = false;

  constructor(private router: Router) {
    addIcons({
      mailOutline,
      chatbubblesOutline,
      notificationsOutline,
      logOutOutline
    });
  }

  ngOnInit() {
    console.log('Página principal cargada');
    // Obtener el nombre completo del usuario del localStorage
    const nombreCompleto = localStorage.getItem('nombreUsuario');
    this.usuario = nombreCompleto || 'Usuario';
  }

  navegar(destino: string) {
    console.log(`Navegando a: ${destino}`);

    switch(destino) {
      case 'datos':
       window.location.href = 'http://localhost:8100/datos';
        break;
      case 'nomina':
        window.location.href = 'http://localhost:8100/nomina';
        break;
      case 'horario':
        window.location.href = 'http://localhost:8100/horario';
        break;
      case 'empleados':
        window.location.href = 'http://localhost:8100/listausuarios';
        break;
      default:
        console.warn('Destino desconocido:', destino);
    }
  }

  irAPrincipal() {
    console.log('Volviendo a la página principal');
    this.router.navigate(['/principal']);
  }

  abrirPerfil() {
    console.log('Abrir perfil de usuario');
    window.location.href = 'http://localhost:8100/perfiladmin';
  }

  toggleReportes() {
    this.mostrarReportes = !this.mostrarReportes;
  }
  correo: string = 'Simon8rm@gmail.com';

  cerrarSesion() {
    console.log('Cerrando sesión...');
    // Limpiar datos específicos
    localStorage.removeItem('nombreUsuario');
    localStorage.removeItem('usuario_id');
    // Limpiar todo el localStorage
    localStorage.clear();
    this.usuario = '';
    this.router.navigate(['/login']);
  }
}

