import { ComponentFixture, TestBed } from '@angular/core/testing';
import { NominaPage } from './nomina.page';

describe('NominaPage', () => {
  let component: NominaPage;
  let fixture: ComponentFixture<NominaPage>;

  beforeEach(() => {
    fixture = TestBed.createComponent(NominaPage);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
