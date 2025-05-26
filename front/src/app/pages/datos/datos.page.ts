import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { IonContent, IonHeader, IonTitle, IonToolbar, IonList, IonItem, IonIcon, IonButton, IonAvatar } from '@ionic/angular/standalone';
import { UserService } from 'src/app/services/user.service';
import Chart from 'chart.js/auto';

@Component({
  selector: 'app-datos',
  templateUrl: './datos.page.html',
  styleUrls: ['./datos.page.scss'],
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,
    IonContent,
    IonHeader,
    IonTitle,
    IonToolbar,
    IonList,
    IonItem,
    IonIcon,
    IonButton,
    IonAvatar
  ]
})
export class DatosPage implements OnInit {
  data: any;
  edadKeys: string[] = [];
  ventasKeys: string[] = [];
  chart: any;

  constructor(private userService: UserService) {}

  ngOnInit() {
    this.userService.obtenerMetricas().subscribe(response => {
      this.data = response;
      this.edadKeys = Object.keys(this.data.distribucion_edades);
      this.ventasKeys = Object.keys(this.data.ventas_simuladas_por_mes);
      this.crearGrafico();
    });
  }

  crearGrafico() {
    const valores = this.edadKeys.map(key => this.data.distribucion_edades[key]);

    const canvas: any = document.getElementById('edadChart');
    if (this.chart) this.chart.destroy();

    this.chart = new Chart(canvas, {
      type: 'bar',
      data: {
        labels: this.edadKeys,
        datasets: [{
          label: 'Cantidad de empleados',
          data: valores,
          backgroundColor: 'rgba(66, 133, 244, 0.7)',
          borderColor: 'rgba(66, 133, 244, 1)',
          borderWidth: 1
        }]
      },
      options: {
        responsive: true,
        plugins: {
          legend: { display: false }
        },
        scales: {
          y: {
            beginAtZero: true,
            ticks: { stepSize: 1 }
          }
        }
      }
    });
  }

  irAPrincipal() { window.location.href = 'http://localhost:8100/home'; }
  irAEmpleados() { window.location.href = 'http://localhost:8100/empleados'; }
  irACalendario() { window.location.href = 'http://localhost:8100/calendario'; }
  irANomina() { window.location.href = 'http://localhost:8100/nomina'; }
  irAPerfilAdmin() { window.location.href = 'http://localhost:8100/perfiladmin'; }
}

