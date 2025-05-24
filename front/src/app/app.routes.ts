import { Routes } from '@angular/router';

export const routes: Routes = [
  {
    path: 'home',
    loadComponent: () => import('./home/home.page').then((m) => m.HomePage),
  },
  {
    path: '',
    redirectTo: 'register',
    pathMatch: 'full',
  },
  {
    path: 'register',
    loadComponent: () => import('./pages/register/register.page').then( m => m.RegisterPage)
  },
  {
    path: 'login',
    loadComponent: () => import('./pages/login/login.page').then( m => m.LoginPage)
  },
  {
    path: 'principal',
    loadComponent: () => import('./pages/principal/principal.page').then( m => m.PrincipalPage)
  },
  {
    path: 'horario',
    loadComponent: () => import('./pages/horario/horario.page').then( m => m.HorarioPage)
  },
  {
    path: 'perfiladmin',
    loadComponent: () => import('./pages/perfiladmin/perfiladmin.page').then( m => m.PerfiladminPage)
  },
  {
    path: 'nuevajornada',
    loadComponent: () => import('./pages/nuevajornada/nuevajornada.page').then( m => m.NuevajornadaPage)
  },
  {
    path: 'nomina',
    loadComponent: () => import('./pages/nomina/nomina.page').then( m => m.NominaPage)
  },


];
