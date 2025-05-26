// user.service.ts (actualizado)
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class UserService {
  private apiUrl = 'http://localhost:8000';

  constructor(private http: HttpClient) {}

  login(correo: string, contrasena: string): Observable<any> {
    return this.http.post(`${this.apiUrl}/login`, { correo, contrasena });
  }

  registrar(usuario: any): Observable<any> {
    return this.http.post(`${this.apiUrl}/register`, usuario);
  }

  obtenerUsuarios(): Observable<any[]> {
    return this.http.get<any[]>(`${this.apiUrl}/admin/usuarios`);
  }

  obtenerAdministradores(): Observable<any[]> {
    return this.http.get<any[]>(`${this.apiUrl}/admin/administradores`);
  }

  eliminarUsuario(id: string): Observable<void> {
    return this.http.delete<void>(`${this.apiUrl}/admin/usuarios/${id}`);
  }

  crearNomina(usuario_id: string, horas_trabajadas: number, dias_incapacidad: number, horas_extra: number, bonificacion: number, periodo_pago: string): Observable<any> {
    return this.http.post(`${this.apiUrl}/admin/crear_nomina`, {
      usuario_id,
      horas_trabajadas,
      dias_incapacidad,
      horas_extra,
      bonificacion,
      periodo_pago
    });
  }

  enviarNomina(usuario_id: string, periodo_pago: string): Observable<any> {
    return this.http.post(`${this.apiUrl}/enviar-nomina`, { usuario_id, periodo_pago });
  }

  obtenerMetricas(): Observable<any> {
    return this.http.get<any>(`${this.apiUrl}/admin/metrics`);
  }

  // ✅ Nuevo servicio para asignar jornada
  asignarHorario(payload: {
    usuario_id: string,
    dia_semana: string,
    hora_entrada: string,
    hora_salida: string,
    observacion: string,
    fecha?: string
  }): Observable<any> {
    return this.http.post(`${this.apiUrl}/admin/horarios`, payload);
  }
}
