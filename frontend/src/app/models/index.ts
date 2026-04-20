export interface AuthTokens {
  access: string;
  refresh: string;
  username: string;
}

export interface UserProfile {
  id: number;
  username: string;
  email: string;
  brain_fog_mode: boolean;
  xp_points: number;
  created_at: string;
}

export interface Doctor {
  id: number;
  name: string;
  specialty: string;
  email: string;
}

export interface MedicalTask {
  id: number;
  title: string;
  consequence_text: string;
  due_date: string | null;
  valid_until: string | null;
  current_stock: number;
  is_done: boolean;
  priority: 'low' | 'medium' | 'high';
  created_at: string;
}

export interface SymptomEntry {
  id: number;
  task: number | null;
  name: string;
  severity: number;
  notes: string;
  recorded_at: string;
}

export interface LabReport {
  id: number;
  file: string;
  transcribed_conclusion: string;
  is_verified: boolean;
  uploaded_at: string;
  updated_at: string;
}

export interface Notification {
  id: number;
  message: string;
  level: 'info' | 'warning' | 'escalation';
  is_read: boolean;
  expires_at: string | null;
  created_at: string;
  is_expired: boolean;
}
