// src/app/services/user.service.ts
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

interface LoginResponse {
  mensaje: string;
  usuario_id: string;
  empresa: string;
  nombre: string;
}

@Injectable({
  providedIn: 'root'
})
export class UserService {
  private apiUrl = 'http://localhost:8000'; // ✅ URL base correcta

  constructor(private http: HttpClient) { }

  login(correo: string, contrasena: string): Observable<LoginResponse> {
    return this.http.post<LoginResponse>(`${this.apiUrl}/login`, {
      correo,
      contrasena
    });
  }

  obtenerUsuarios(): Observable<any[]> {
    return this.http.get<any[]>(`${this.apiUrl}/admin/usuarios`); // ✅ URL corregida
  }

  obtenerAdministradores(): Observable<any[]> {
    return this.http.get<any[]>(`${this.apiUrl}/admin/administradores`); // ✅ URL corregida
  }

  eliminarUsuario(id: string): Observable<void> {
    return this.http.delete<void>(`${this.apiUrl}/admin/usuarios/${id}`); // ✅ URL corregida
  }
}


