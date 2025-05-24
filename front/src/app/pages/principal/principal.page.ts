import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { IonicModule } from '@ionic/angular';
import { Router } from '@angular/router';

@Component({
  selector: 'app-principal',
  templateUrl: './principal.page.html',
  styleUrls: ['./principal.page.scss'],
  standalone: true,
  imports: [IonicModule, CommonModule, FormsModule],
})
export class PrincipalPage implements OnInit {
  usuario: string = ''; // Asigna según lógica real
  mostrarReportes: boolean = false;

  constructor(private router: Router) {}

  ngOnInit() {
    console.log('Página principal cargada');
  }

  navegar(destino: string) {
    console.log(`Navegando a: ${destino}`);

    switch(destino) {
      case 'metricas':
        // Ruta interna (Angular/Ionic)
        this.router.navigate(['/metricas']);
        break;
      case 'nomina':
        window.location.href = 'http://localhost:8101/nomina';
        break;
      case 'horario':
        window.location.href = 'http://localhost:8101/horario';
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

}
