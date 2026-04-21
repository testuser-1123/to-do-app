import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink } from '@angular/router';
import { ApiService } from '../../services/api.service';
import { AuthService } from '../../services/auth.service';
import { ThemeService } from '../../services/theme.service';
import { UserProfile } from '../../models';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [CommonModule, RouterLink],
  templateUrl: './dashboard.component.html',
})
export class DashboardComponent implements OnInit {
  profile: UserProfile | null = null;
  loading = false;
  error = '';

  constructor(
    public theme: ThemeService,
    private api: ApiService,
    public auth: AuthService,
  ) {}

  ngOnInit(): void {
    this.loading = true;
    this.api.getProfile().subscribe({
      next: p => {
        this.profile = p;
        this.theme.loadFromProfile(p.brain_fog_mode);
        this.loading = false;
      },
      error: () => { this.error = 'Failed to load profile.'; this.loading = false; },
    });
  }

  toggleBrainFog(): void {
    this.theme.toggle();
    if (this.profile) {
      this.profile.brain_fog_mode = this.theme.isBrainFog;
    }
  }

  logout(): void {
    this.auth.logout();
  }
}
