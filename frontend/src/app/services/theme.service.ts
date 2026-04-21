import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';
import { ApiService } from './api.service';

@Injectable({ providedIn: 'root' })
export class ThemeService {
  private _brainFog = new BehaviorSubject<boolean>(false);
  readonly brainFog$ = this._brainFog.asObservable();
  private readonly storageKey = 'brainFogMode';
  
  private lastToggleTime = 0;

  constructor(private api: ApiService) {
    const savedState = localStorage.getItem(this.storageKey);
    if (savedState !== null) {
      const isActive = savedState === 'true';
      this._brainFog.next(isActive);
      this.applyBodyClass(isActive);
    }
  }

  get isBrainFog(): boolean {
    return this._brainFog.value;
  }

  loadFromProfile(backendValue: boolean): void {

    if (Date.now() - this.lastToggleTime < 3000) {
      return;
    }

    if (this._brainFog.value !== backendValue) {
      this._brainFog.next(backendValue);
      localStorage.setItem(this.storageKey, String(backendValue));
      this.applyBodyClass(backendValue);
    }
  }

  toggle(): void {
    const newVal = !this._brainFog.value;
    this.lastToggleTime = Date.now();
    
    this._brainFog.next(newVal);
    localStorage.setItem(this.storageKey, String(newVal));
    this.applyBodyClass(newVal);

    this.api.updateProfile({ brain_fog_mode: newVal }).subscribe({
      error: (err) => console.error('Failed to sync theme:', err)
    });
  }

  private applyBodyClass(active: boolean): void {
    if (active) {
      document.body.classList.add('brain-fog');
    } else {
      document.body.classList.remove('brain-fog');
    }
  }
}