import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { IonicModule, AlertController } from '@ionic/angular';
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

  constructor(
    private userService: UserService,
    private alertController: AlertController
  ) {}

  ngOnInit() {
    this.cargarUsuarios();
  }

  cargarUsuarios() {
    this.userService.obtenerUsuarios().subscribe(data => {
      this.empleados = data.map(u => ({
        id: u.id,
        nombre: u.nombre,
        email: u.correo,
        tipo: 'Empleado',
        foto: 'assets/icon/avatar.png'
      }));
    });

    this.userService.obtenerAdministradores().subscribe(data => {
      this.administradores = data.map(a => ({
        id: a.id,
        nombre: a.nombre,
        email: a.correo,
        tipo: 'Administrador',
        foto: 'assets/icon/avatar.png'
      }));
    });
  }

  async eliminarUsuario() {
    const id = this.busqueda.trim();

    if (!id) {
      this.mostrarAlerta('Por favor ingresa un ID válido.');
      return;
    }

    const confirm = await this.alertController.create({
      header: 'Confirmar eliminación',
      message: `¿Estás seguro de eliminar al usuario con ID <strong>${id}</strong>?`,
      buttons: [
        { text: 'Cancelar', role: 'cancel' },
        {
          text: 'Eliminar',
          handler: () => {
            this.userService.eliminarUsuario(id).subscribe({
              next: () => {
                this.mostrarAlerta('Usuario eliminado correctamente.');
                this.cargarUsuarios();
              },
              error: err => {
                console.error(err);
                this.mostrarAlerta('Error al eliminar el usuario.');
              }
            });
          }
        }
      ]
    });

    await confirm.present();
  }

  async mostrarAlerta(mensaje: string) {
    const alerta = await this.alertController.create({
      header: 'Aviso',
      message: mensaje,
      buttons: ['OK']
    });
    await alerta.present();
  }

  navegar(url: string) {
    window.location.href = url;
  }

  abrirPerfil() {
    console.log('Abriendo perfil...');
  }
}


