import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { IonicModule, ToastController } from '@ionic/angular';
import { NavController } from '@ionic/angular';


@Component({
  selector: 'app-register',
  templateUrl: './register.page.html',
  styleUrls: ['./register.page.scss'],
  standalone: true,
  imports: [IonicModule, CommonModule, FormsModule]
})
export class RegisterPage implements OnInit {
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
  mes: string = '';
  anio: string = '';
  maxAnio: number = new Date().getFullYear() - 13; // Edad mínima: 13 años

  constructor(private toastController: ToastController) { }

  ngOnInit() { }

  validarDia() {
    if (this.dia) {
      const dayNum = parseInt(this.dia);
      if (dayNum < 1) this.dia = '1';
      if (dayNum > 31) this.dia = '31';
    }
  }

  validarAnio() {
    if (this.anio) {
      const yearNum = parseInt(this.anio);
      if (yearNum < 1950) this.anio = '1950';
      if (yearNum > this.maxAnio) this.anio = this.maxAnio.toString();
    }
  }

  async mostrarError(mensaje: string) {
    const toast = await this.toastController.create({
      message: mensaje,
      duration: 3000,
      position: 'top',
      color: 'danger'
    });
    await toast.present();
  }

  async registrarUsuario() {
    // Validar campos de fecha
    if (!this.dia || !this.mes || !this.anio) {
      await this.mostrarError('Por favor complete todos los campos de la fecha de nacimiento');
      return;
    }

    // Validar día según mes
    const diaNum = parseInt(this.dia);
    const mesNum = parseInt(this.mes);
    const anioNum = parseInt(this.anio);

    // Validar meses con 30 días
    if ([4, 6, 9, 11].includes(mesNum) && diaNum > 30) {
      await this.mostrarError('El mes seleccionado solo tiene 30 días');
      return;
    }

    // Validar febrero
    if (mesNum === 2) {
      const esBisiesto = (anioNum % 4 === 0 && anioNum % 100 !== 0) || (anioNum % 400 === 0);
      const maxDiasFeb = esBisiesto ? 29 : 28;
      
      if (diaNum > maxDiasFeb) {
        await this.mostrarError(`Febrero de ${anioNum} solo tiene ${maxDiasFeb} días`);
        return;
      }
    }

    // Formatear fecha como YYYY-MM-DD
    const diaFormateado = this.dia.padStart(2, '0');
    this.usuario.fecha_nacimiento = `${this.anio}-${this.mes}-${diaFormateado}`;

    // Validar contraseñas coinciden
    if (this.usuario.contrasena !== this.usuario.confirmar_contrasena) {
      await this.mostrarError('Las contraseñas no coinciden');
      return;
    }

    // Validar contraseña cumple requisitos
    const passwordRegex = /^(?=.*[A-Z])(?=.*\d).{8,}$/;
    if (!passwordRegex.test(this.usuario.contrasena)) {
      await this.mostrarError('La contraseña debe tener al menos 8 caracteres, una mayúscula y un número');
      return;
    }

    // Validar formato de email
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(this.usuario.correo)) {
      await this.mostrarError('Por favor ingrese un correo electrónico válido');
      return;
    }

    console.log('Usuario a registrar:', this.usuario);
    // Aquí puedes integrar con tu backend FastAPI
  }
}

