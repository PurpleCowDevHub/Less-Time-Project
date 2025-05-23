import { ComponentFixture, TestBed } from '@angular/core/testing';
import { NuevajornadaPage } from './nuevajornada.page';

describe('NuevajornadaPage', () => {
  let component: NuevajornadaPage;
  let fixture: ComponentFixture<NuevajornadaPage>;

  beforeEach(() => {
    fixture = TestBed.createComponent(NuevajornadaPage);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
