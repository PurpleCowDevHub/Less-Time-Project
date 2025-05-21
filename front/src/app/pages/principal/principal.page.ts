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
  usuario: string = '';
  mostrarReportes: boolean = false;

  constructor(private router: Router) {}

  ngOnInit() {
    console.log('Página principal cargada');
  }

  navegar(destino: string) {
    console.log(`Navegando a: ${destino}`);
    // this.router.navigate([`/${destino}`]);
  }

  irAPrincipal() {
    console.log('Volviendo a la página principal');
    // this.router.navigate(['/principal']);
  }

  abrirPerfil() {
    console.log('Abrir perfil de usuario');
    // Lógica para mostrar el perfil, modal o navegar
  }

  toggleReportes() {
    this.mostrarReportes = !this.mostrarReportes;
  }
}