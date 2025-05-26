import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import {
  IonContent,
  IonHeader,
  IonTitle,
  IonToolbar,
  IonList,
  IonItem,
  IonIcon,
  IonButton,
  IonAvatar
} from '@ionic/angular/standalone';
import { UserService } from 'src/app/services/user.service';
import { Chart } from 'chart.js/auto';
import { addIcons } from 'ionicons';
import {
  peopleOutline,
  calendarOutline,
  cashOutline,
  barChartOutline
} from 'ionicons/icons';

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

  constructor(private userService: UserService) {
    addIcons({
      peopleOutline,
      calendarOutline,
      cashOutline,
      barChartOutline
    });
  }

  ngOnInit() {
    this.userService.obtenerMetricas().subscribe((res) => {
      this.data = res;
      this.edadKeys = Object.keys(this.data.distribucion_edades);
      this.ventasKeys = Object.keys(this.data.ventas_simuladas_por_mes);

      this.renderizarGraficaEdad();
    });
  }

  renderizarGraficaEdad() {
    const canvas = document.getElementById('edadChart') as HTMLCanvasElement;
    if (canvas) {
      new Chart(canvas, {
        type: 'bar',
        data: {
          labels: this.edadKeys,
          datasets: [{
            label: 'Cantidad',
            data: this.edadKeys.map(k => this.data.distribucion_edades[k]),
            backgroundColor: 'rgba(66, 133, 244, 0.5)',
            borderColor: 'rgba(66, 133, 244, 1)',
            borderWidth: 1
          }]
        },
        options: {
          responsive: true,
          plugins: {
            legend: {
              display: false
            },
            title: {
              display: false
            }
          },
          scales: {
            y: {
              beginAtZero: true
            }
          }
        }
      });
    }
  }

  irAPrincipal() {
    window.location.href = 'http://localhost:8100/home';
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
}
