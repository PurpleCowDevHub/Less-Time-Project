import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

interface LoginResponse {
  mensaje: string;
  usuario_id: string;
  empresa: string;
  nombre: string;
}

interface NominaResponse {
  mensaje: string;
  usuario_id: string;
  salario_bruto: string;
  menos_salud_4: string;
  menos_pension_4: string;
  salario_neto: string;
  periodo_pago: string;
}

interface EmailResponse {
  message: string;
  usuario_id: string;
}

interface RegistroPayload {
  nombre: string;
  apellido: string;
  cedula: string;
  correo: string;
  contrasena: string;
  confirmar_contrasena: string;
  empresa: string;
  es_admin: boolean;
  fecha_nacimiento?: string;
}

@Injectable({
  providedIn: 'root'
})
export class UserService {
  private apiUrl = 'http://localhost:8000';

  constructor(private http: HttpClient) {}

  // Autenticación
  login(correo: string, contrasena: string): Observable<LoginResponse> {
    return this.http.post<LoginResponse>(`${this.apiUrl}/login`, { correo, contrasena });
  }

  registrar(usuario: RegistroPayload): Observable<any> {
    return this.http.post(`${this.apiUrl}/register`, usuario);
  }

  // Administración
  obtenerUsuarios(): Observable<any[]> {
    return this.http.get<any[]>(`${this.apiUrl}/admin/usuarios`);
  }

  obtenerAdministradores(): Observable<any[]> {
    return this.http.get<any[]>(`${this.apiUrl}/admin/administradores`);
  }

  eliminarUsuario(id: string): Observable<void> {
    return this.http.delete<void>(`${this.apiUrl}/admin/usuarios/${id}`);
  }

  // Nómina
  crearNomina(
    usuario_id: string,
    horas_trabajadas: number,
    dias_incapacidad: number,
    horas_extra: number,
    bonificacion: number,
    periodo_pago: string
  ): Observable<NominaResponse> {
    return this.http.post<NominaResponse>(`${this.apiUrl}/admin/crear_nomina`, {
      usuario_id,
      horas_trabajadas,
      dias_incapacidad,
      horas_extra,
      bonificacion,
      periodo_pago
    });
  }

  enviarNomina(usuario_id: string, periodo_pago: string): Observable<EmailResponse> {
    return this.http.post<EmailResponse>(`${this.apiUrl}/enviar-nomina`, {
      usuario_id,
      periodo_pago
    });
  }

  // 🔵 Obtener métricas para el dashboard
  obtenerMetricas(): Observable<any> {
    return this.http.get<any>(`${this.apiUrl}/admin/metrics`);
  }
}
