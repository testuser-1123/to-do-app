import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';
import { ApiService } from './api.service';

@Injectable({ providedIn: 'root' })
export class ThemeService {
  private _brainFog = new BehaviorSubject<boolean>(false);
  readonly brainFog$ = this._brainFog.asObservable();

  constructor(private api: ApiService) {}

  get isBrainFog(): boolean {
    return this._brainFog.value;
  }

  loadFromProfile(brainFogMode: boolean): void {
    this._brainFog.next(brainFogMode);
    this.applyBodyClass(brainFogMode);
  }

  toggle(): void {
    const newVal = !this._brainFog.value;
    this._brainFog.next(newVal);
    this.applyBodyClass(newVal);
    this.api.updateProfile({ brain_fog_mode: newVal }).subscribe();
  }

  private applyBodyClass(active: boolean): void {
    document.body.classList.toggle('brain-fog', active);
  }
}
