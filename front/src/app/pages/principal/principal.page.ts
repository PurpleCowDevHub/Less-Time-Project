import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { IonicModule } from '@ionic/angular';

@Component({
  selector: 'app-principal',
  templateUrl: './principal.page.html',
  styleUrls: ['./principal.page.scss'],
  imports: [CommonModule, FormsModule, IonicModule]
})
export class PrincipalPage implements OnInit {

  constructor() {}

  ngOnInit() {}

  openSection(section: string) {
    console.log('Abrir sección:', section);
  }
}
