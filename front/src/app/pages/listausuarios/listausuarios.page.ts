import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { IonicModule } from '@ionic/angular';

@Component({
  selector: 'app-empleado-lista',
  standalone: true,
  templateUrl: './listausuarios.page.html',
  styleUrls: ['./listausuarios.page.scss'],
  imports: [
    CommonModule,
    FormsModule,
    IonicModule,
  ]
})
export class ListausuariosPage {
  busqueda: string = '';

  empleados = [
    { id: 'E001', nombre: 'Ana Torres', email: 'ana.torres@empresa.com', foto: 'assets/icon/avatar.png', tipo: 'Empleado' },
    { id: 'E002', nombre: 'Luis Gómez', email: 'luis.gomez@empresa.com', foto: 'assets/icon/avatar.png', tipo: 'Empleado' },
    { id: 'E003', nombre: 'María López', email: 'maria.lopez@empresa.com', foto: 'assets/icon/avatar.png', tipo: 'Empleado' },
    { id: 'E004', nombre: 'Carlos Ruiz', email: 'carlos.ruiz@empresa.com', foto: 'assets/icon/avatar.png', tipo: 'Empleado' },
    { id: 'E005', nombre: 'Laura Fernández', email: 'laura.fernandez@empresa.com', foto: 'assets/icon/avatar.png', tipo: 'Empleado' },
    { id: 'E006', nombre: 'Jorge Martínez', email: 'jorge.martinez@empresa.com', foto: 'assets/icon/avatar.png', tipo: 'Empleado' },
    { id: 'E007', nombre: 'Sofía Díaz', email: 'sofia.diaz@empresa.com', foto: 'assets/icon/avatar.png', tipo: 'Empleado' },
    { id: 'E008', nombre: 'Ricardo Morales', email: 'ricardo.morales@empresa.com', foto: 'assets/icon/avatar.png', tipo: 'Empleado' },
    { id: 'E009', nombre: 'Elena Castro', email: 'elena.castro@empresa.com', foto: 'assets/icon/avatar.png', tipo: 'Empleado' },
    { id: 'E010', nombre: 'Mario Sánchez', email: 'mario.sanchez@empresa.com', foto: 'assets/icon/avatar.png', tipo: 'Empleado' }
  ];

  administradores = [
    { id: 'A001', nombre: 'Pedro Admin', email: 'pedro.admin@empresa.com', foto: 'assets/icon/avatar.png', tipo: 'Administrador' },
    { id: 'A002', nombre: 'Carla Admin', email: 'carla.admin@empresa.com', foto: 'assets/icon/avatar.png', tipo: 'Administrador' }
  ];

  get listaCompleta() {
    return [...this.empleados, ...this.administradores];
  }

  navegar(url: string) {
    if (url.startsWith('http')) {
      window.location.href = url;
    } else {
      // Aquí podrías usar router si lo importas y lo inyectas
      window.location.href = url; // Por ahora uso window.location para simplificar
    }
  }

  abrirPerfil() {
    console.log('Abriendo perfil...');
  }
}
