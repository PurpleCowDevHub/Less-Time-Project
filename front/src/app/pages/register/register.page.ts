import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { IonicModule, ToastController } from '@ionic/angular';
import { RouterModule, Router } from '@angular/router';
import { UserService } from 'src/app/services/user.service';

@Component({
  selector: 'app-register',
  templateUrl: './register.page.html',
  styleUrls: ['./register.page.scss'],
  standalone: true,
  imports: [IonicModule, CommonModule, FormsModule, RouterModule],
})
export class RegisterPage {
  usuario = {
    nombre: '',
    apellido: '',
    cedula: '',
    correo: '',
    contrasena: '',
    confirmar_contrasena: '',
    empresa: '',
    es_admin: false,
    fecha_nacimiento: ''
  };

  dia: string = '';
  mes: string = '';  // ✅ Esto es lo importante
  anio: string = '';
  maxAnio: number = new Date().getFullYear() - 13;

  constructor(
    private toastController: ToastController,
    private userService: UserService,
    private router: Router
  ) {}

  async registrarUsuario() {
    console.log("Botón presionado");

    if (!this.dia || !this.mes || !this.anio) {
      await this.mostrarError('Por favor completa la fecha de nacimiento');
      return;
    }

    const diaFormateado = String(this.dia).padStart(2, '0');
    this.usuario.fecha_nacimiento = `${this.anio}-${this.mes}-${diaFormateado}`;

    if (this.usuario.contrasena !== this.usuario.confirmar_contrasena) {
      await this.mostrarError('Las contraseñas no coinciden');
      return;
    }

    try {
      await this.userService.registrar(this.usuario).toPromise();

      const toast = await this.toastController.create({
        message: 'Usuario registrado correctamente',
        duration: 3000,
        color: 'success',
        position: 'top'
      });
      await toast.present();

      this.router.navigate(['/login']);

    } catch (error: any) {
      console.error("❌ Error al registrar:", error);
      let mensaje = 'Error interno del servidor';

      if (error.status === 400 && error.error?.detail?.message) {
        mensaje = error.error.detail.message;
      } else if (error.status === 422) {
        mensaje = 'Datos inválidos: ' + (error.error?.detail?.details?.[0]?.error || 'Verifica los campos');
      }

      const toast = await this.toastController.create({
        message: mensaje,
        duration: 4000,
        color: 'danger',
        position: 'top'
      });
      await toast.present();
    }
  }

  async mostrarError(mensaje: string) {
    const toast = await this.toastController.create({
      message: mensaje,
      duration: 3000,
      color: 'danger',
      position: 'top'
    });
    await toast.present();
  }
}




