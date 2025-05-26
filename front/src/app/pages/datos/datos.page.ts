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

    constructor() {}

    ngOnInit() {
      // Datos de nómina simulados
      this.data = {
        salario_bruto_promedio: "$4,406,666.67",
        salario_bruto_sumatoria: "$13,220,000.00",
        salario_neto_promedio: "$4,054,133.33",
        salario_neto_sumatoria: "$12,162,400.00",
        horas_trabajadas_promedio: 63.33,
        horas_trabajadas_sumatoria: 190,
        bonificacion_promedio: "$53,333.33",
        bonificacion_sumatoria: "$160,000.00",
        edad_promedio: 21.5,
        edad_sumatoria: 129,
        distribucion_edades: {
          "<20": 0,
          "20-29": 6,
          "30-39": 0,
          "40-49": 0,
          "50-59": 0,
          "60+": 0
        },
        ventas_simuladas_por_mes: {
          "2025-01": 31304.24,
          "2025-02": 41512.04,
          "2025-03": 39687.84,
          "2025-04": 43137.17,
          "2025-05": 42745.38,
          "2026-12": 30799.54
        }
      };

      // Claves necesarias para iterar en *ngFor
      this.edadKeys = Object.keys(this.data.distribucion_edades);
      this.ventasKeys = Object.keys(this.data.ventas_simuladas_por_mes);
    }

    // Funciones de navegación
    irAPrincipal() {
      window.location.href = 'http://localhost:8100/home';
    }

    irAEmpleados() {
      window.location.href = 'http://localhost:8100/empleados';
    }

    irACalendario() {
      window.location.href = 'http://localhost:8100/calendario';
    }

    irANomina() {
      window.location.href = 'http://localhost:8100/nomina';
    }

    irAPerfilAdmin() {
      window.location.href = 'http://localhost:8100/perfiladmin';
    }
  }
