import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { IonicModule } from '@ionic/angular';
import { addIcons } from 'ionicons';
import { 
  peopleOutline, 
  calendarOutline, 
  cashOutline,
  barChartOutline 
} from 'ionicons/icons';
// Update the import path below if user.service.ts is located elsewhere
import { UserService } from '../../services/user.service';
import { AlertController } from '@ionic/angular';

@Component({
  selector: 'app-nomina',
  templateUrl: './nomina.page.html',
  styleUrls: ['./nomina.page.scss'],
  standalone: true,
  imports: [IonicModule, CommonModule, FormsModule],
})
export class NominaPage {
  // Datos de ejemplo para la vista


  // Variables para el formulario
  usuarioId: string = '';
  horasTrabajadas: number = 0;
  diasIncapacidad: number = 0;
  horasExtra: number = 0;
  bonificacion: number = 0;
  periodoPago: string = '';
  idEnvioNomina: string = '';

  constructor(
    private userService: UserService,
    private alertController: AlertController
  ) {
    addIcons({
      peopleOutline,
      calendarOutline,
      cashOutline,
      barChartOutline
    });
  }

  // Métodos de navegación
  irAPrincipal() {
    window.location.href = 'http://localhost:8100/principal';
  }

  irAEmpleados() {
    window.location.href = 'http://localhost:8100/listausuarios';
  }

  irACalendario() {
    window.location.href = 'http://localhost:8100/horario';
  }

  irANomina() {
    window.location.href = 'http://localhost:8100/nomina';
  }

  irAPerfilAdmin() {
    window.location.href = 'http://localhost:8100/perfiladmin';
  }

    irADatos() {
    window.location.href = 'http://localhost:8100/datos';
  }

  // Método para crear nómina
  async guardarDatosNomina() {
    // Validación básica
    if (!this.usuarioId || !this.periodoPago) {
      await this.mostrarAlerta('Error', 'ID de empleado y período de pago son obligatorios');
      return;
    }

    try {
      const response = await this.userService.crearNomina(
        this.usuarioId,
        this.horasTrabajadas || 0,
        this.diasIncapacidad || 0,
        this.horasExtra || 0,
        this.bonificacion || 0,
        this.periodoPago
      ).toPromise();

      await this.mostrarAlerta('Éxito', 'Nómina creada exitosamente');
      console.log('Nómina creada:', response);
      
      // Prellenamos el ID para envío automático
      this.idEnvioNomina = this.usuarioId;

    } catch (error) {
      console.error('Error al crear nómina:', error);
      await this.mostrarAlerta('Error', 'No se pudo crear la nómina. Verifique los datos');
    }
  }

  // Método para enviar nómina por correo
  async enviarNominaConDatos() {
    if (!this.idEnvioNomina || !this.periodoPago) {
      await this.mostrarAlerta('Error', 'ID de empleado y período de pago son obligatorios');
      return;
    }

    try {
      const response = await this.userService.enviarNomina(
        this.idEnvioNomina,
        this.periodoPago
      ).toPromise();

      await this.mostrarAlerta('Éxito', 'Nómina enviada exitosamente');
      console.log('Nómina enviada:', response);

    } catch (error) {
      console.error('Error al enviar nómina:', error);
      await this.mostrarAlerta('Error', 'No se pudo enviar la nómina. Verifique los datos');
    }
  }

  // Método auxiliar para mostrar alertas
  private async mostrarAlerta(titulo: string, mensaje: string) {
    const alert = await this.alertController.create({
      header: titulo,
      message: mensaje,
      buttons: ['OK']
    });
    await alert.present();
  }

  // Métodos de ejemplo (pueden eliminarse si no se usan)
  guardarNomina() {
    console.log('Método guardarNomina() llamado');
  }

  enviarNomina() {
    console.log('Método enviarNomina() llamado');
  }
}