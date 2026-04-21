import { Routes } from '@angular/router';
import { authGuard } from './guards/auth.guard';

export const routes: Routes = [
  { path: '',       redirectTo: '/login', pathMatch: 'full' },
  { path: 'login',  loadComponent: () => import('./pages/login/login.component').then(m => m.LoginComponent) },
  {
    path: 'dashboard',
    canActivate: [authGuard],
    loadComponent: () => import('./pages/dashboard/dashboard.component').then(m => m.DashboardComponent),
  },
  {
    path: 'tasks',
    canActivate: [authGuard],
    loadComponent: () => import('./pages/tasks/tasks.component').then(m => m.TasksComponent),
  },
  {
    path: 'symptoms',
    canActivate: [authGuard],
    loadComponent: () => import('./pages/symptoms/symptoms.component').then(m => m.SymptomsComponent),
  },
  {
    path: 'labs',
    canActivate: [authGuard],
    loadComponent: () => import('./pages/labs/labs.component').then(m => m.LabsComponent),
  },
  {
    path: 'reports',
    canActivate: [authGuard],
    loadComponent: () => import('./pages/reports/reports.component').then(m => m.ReportsComponent),
  },
  { path: '**', redirectTo: '/login' },
];