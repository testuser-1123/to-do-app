import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import {
  AuthTokens, UserProfile, MedicalTask,
  SymptomEntry, LabReport, Notification
} from '../models';

const BASE = 'http://localhost:8000/api';

@Injectable({ providedIn: 'root' })
export class ApiService {
  constructor(private http: HttpClient) {}

  // ── Auth ────────────────────────────────────────────────────────────────
  login(username: string, password: string): Observable<AuthTokens> {
    return this.http.post<AuthTokens>(`${BASE}/auth/login/`, { username, password });
  }

  logout(refresh: string): Observable<any> {
    return this.http.post(`${BASE}/auth/logout/`, { refresh });
  }

  // ── Profile ─────────────────────────────────────────────────────────────
  getProfile(): Observable<UserProfile> {
    return this.http.get<UserProfile>(`${BASE}/profile/me/`);
  }

  updateProfile(data: Partial<UserProfile>): Observable<UserProfile> {
    return this.http.patch<UserProfile>(`${BASE}/profile/me/`, data);
  }

  // ── Tasks ────────────────────────────────────────────────────────────────
  getTasks(): Observable<MedicalTask[]> {
    return this.http.get<MedicalTask[]>(`${BASE}/tasks/`);
  }

  createTask(task: Partial<MedicalTask>): Observable<MedicalTask> {
    return this.http.post<MedicalTask>(`${BASE}/tasks/`, task);
  }

  updateTask(id: number, data: Partial<MedicalTask>): Observable<MedicalTask> {
    return this.http.patch<MedicalTask>(`${BASE}/tasks/${id}/`, data);
  }

  deleteTask(id: number): Observable<void> {
    return this.http.delete<void>(`${BASE}/tasks/${id}/`);
  }

  // ── Symptoms ─────────────────────────────────────────────────────────────
  searchSymptoms(query: string): Observable<SymptomEntry[]> {
    const params = new HttpParams().set('query', query);
    return this.http.get<SymptomEntry[]>(`${BASE}/symptoms/search/`, { params });
  }

  getSymptoms(): Observable<SymptomEntry[]> {
    return this.http.get<SymptomEntry[]>(`${BASE}/symptoms/`);
  }

  saveSymptom(data: Partial<SymptomEntry>): Observable<SymptomEntry> {
    return this.http.post<SymptomEntry>(`${BASE}/symptoms/`, data);
  }

  // ── Labs ─────────────────────────────────────────────────────────────────
  getLabs(): Observable<LabReport[]> {
    return this.http.get<LabReport[]>(`${BASE}/labs/`);
  }

  uploadLab(formData: FormData): Observable<LabReport> {
    return this.http.post<LabReport>(`${BASE}/labs/`, formData);
  }

  saveConclusion(id: number, conclusion: string): Observable<LabReport> {
    return this.http.patch<LabReport>(`${BASE}/labs/${id}/`, {
      transcribed_conclusion: conclusion
    });
  }

  // ── Notifications ────────────────────────────────────────────────────────
  getNotifications(): Observable<Notification[]> {
    return this.http.get<Notification[]>(`${BASE}/notifications/`);
  }

  clearNotification(id: number): Observable<Notification> {
    return this.http.patch<Notification>(`${BASE}/notifications/${id}/`, { is_read: true });
  }

  // ── Reports ───────────────────────────────────────────────────────────────
  generatePdf(fromDate: string, toDate: string): Observable<Blob> {
    const params = new HttpParams()
      .set('from_date', fromDate)
      .set('to_date', toDate);
    return this.http.get(`${BASE}/reports/summary/pdf/`, {
      params,
      responseType: 'blob'
    });
  }
}
