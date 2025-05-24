import { ComponentFixture, TestBed } from '@angular/core/testing';
import { ListausuariosPage } from './listausuarios.page';

describe('ListausuariosPage', () => {
  let component: ListausuariosPage;
  let fixture: ComponentFixture<ListausuariosPage>;

  beforeEach(() => {
    fixture = TestBed.createComponent(ListausuariosPage);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
