import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ModalController, IonicModule } from '@ionic/angular';
import { ReactiveFormsModule } from '@angular/forms';


@Component({
  selector: 'app-nuevajornada',
  templateUrl: './nuevajornada.page.html',
  styleUrls: ['./nuevajornada.page.scss'],
  standalone: true,
  imports: [IonicModule, CommonModule, FormsModule]
})
export class NuevajornadaPage implements OnInit {
  constructor(private modalCtrl: ModalController) {}

  ngOnInit() {}

  cerrarModal() {
    this.modalCtrl.dismiss();
  }
}
