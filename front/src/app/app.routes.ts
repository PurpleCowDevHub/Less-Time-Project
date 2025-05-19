import { Routes } from '@angular/router';

export const routes: Routes = [
  {
    path: 'home',
    loadComponent: () => import('./home/home.page').then((m) => m.HomePage),
  },
  {
    path: '',
    redirectTo: 'home',
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
    path: 'nomina',
    loadComponent: () => import('./Front/nomina/nomina.page').then( m => m.NominaPage)
  },
  {
    path: 'nomina',
    loadComponent: () => import('./pages/nomina/nomina.page').then( m => m.NominaPage)
  },
];
