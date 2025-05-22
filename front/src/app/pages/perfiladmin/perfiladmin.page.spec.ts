import { ComponentFixture, TestBed } from '@angular/core/testing';
import { PerfiladminPage } from './perfiladmin.page';

describe('PerfiladminPage', () => {
  let component: PerfiladminPage;
  let fixture: ComponentFixture<PerfiladminPage>;

  beforeEach(() => {
    fixture = TestBed.createComponent(PerfiladminPage);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
