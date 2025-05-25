// src/app/pages/listausuarios/listausuarios.page.ts
import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { IonicModule } from '@ionic/angular';
import { HttpClientModule } from '@angular/common/http';
import { UserService } from 'src/app/services/user.service';

@Component({
  selector: 'app-empleado-lista',
  standalone: true,
  templateUrl: './listausuarios.page.html',
  styleUrls: ['./listausuarios.page.scss'],
  imports: [
    CommonModule,
    FormsModule,
    IonicModule,
    HttpClientModule
  ]
})
export class ListausuariosPage implements OnInit {
  busqueda: string = '';
  empleados: any[] = [];
  administradores: any[] = [];

  constructor(private userService: UserService) {}

  ngOnInit() {
    this.userService.obtenerUsuarios().subscribe(data => {
      console.log("Usuarios obtenidos:", data); // 🔍 depuración
      this.empleados = data.map(usuario => ({
        id: usuario.id,
        nombre: usuario.nombre,
        email: usuario.correo, // ✅ corregido
        tipo: 'Empleado',
        foto: 'assets/icon/avatar.png'
      }));
    });

    this.userService.obtenerAdministradores().subscribe(data => {
      console.log("Administradores obtenidos:", data); // 🔍 depuración
      this.administradores = data.map(admin => ({
        id: admin.id,
        nombre: admin.nombre,
        email: admin.correo, // ✅ corregido
        tipo: 'Administrador',
        foto: 'assets/icon/avatar.png'
      }));
    });
  }

  navegar(url: string) {
    if (url.startsWith('http')) {
      window.location.href = url;
    } else {
      window.location.href = url;
    }
  }

  abrirPerfil() {
    console.log('Abriendo perfil...');
  }
}

