import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { IonicModule } from '@ionic/angular';
import { UserService } from '../../services/user.service';
import { Router, RouterLink } from '@angular/router';
import { HttpClientModule } from '@angular/common/http';

@Component({
  selector: 'app-login',
  templateUrl: './login.page.html',
  styleUrls: ['./login.page.scss'],
  standalone: true,
  imports: [
    CommonModule, 
    FormsModule, 
    IonicModule, 
    HttpClientModule,
    RouterLink // Añade esta línea
  ]
})
export class LoginPage {
  email: string = '';
  password: string = '';
  errorMessage: string = '';
  isLoading: boolean = false;

  constructor(
    private userService: UserService,
    private router: Router
  ) {}

  login() {
    this.errorMessage = '';
    
    if (!this.email || !this.password) {
      this.errorMessage = 'Por favor ingresa correo y contraseña';
      return;
    }

    this.isLoading = true;
    
    this.userService.login(this.email, this.password).subscribe({
      next: (response) => {
        this.isLoading = false;
        console.log('Login exitoso:', response);
        
        // Guardar el nombre en localStorage
        localStorage.setItem('nombreUsuario', response.nombre || 'Usuario');
        
        // Redirigir según el tipo de usuario
        if (response.mensaje.includes('administrador')) {
          this.router.navigate(['/perfiladmin']);
        } else {
          this.router.navigate(['/principal']);
        }
      },
      error: (err) => {
        this.isLoading = false;
        console.error('Error en login:', err);
        this.errorMessage = err.status === 401 
          ? 'Credenciales incorrectas. Por favor intenta nuevamente.' 
          : 'Error en el servidor. Por favor intenta más tarde.';
      }
    });
  }
}