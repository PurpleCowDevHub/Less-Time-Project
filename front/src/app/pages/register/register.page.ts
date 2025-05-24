import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { IonicModule } from '@ionic/angular';

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

  constructor() { }

  ngOnInit() { }

  registrarUsuario() {
    console.log(this.usuario);
    // Aquí se puede integrar con FastAPI u otro backend
  }

}



