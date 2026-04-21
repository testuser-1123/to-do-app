import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { CommonModule } from '@angular/common';
import { AuthService } from '../../services/auth.service';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [FormsModule, CommonModule],
  templateUrl: './login.component.html',
})
export class LoginComponent {
  username = '';
  password = '';
  loading = false;
  error = '';

  constructor(private auth: AuthService, private router: Router) {}

  onLogin(): void {
    if (!this.username || !this.password) {
      this.error = 'Please enter both username and password.';
      return;
    }
    this.loading = true;
    this.error = '';

    this.auth.login(this.username, this.password).subscribe({
      next: () => this.router.navigate(['/dashboard']),
      error: (err) => {
        this.loading = false;
        this.error = err.error?.non_field_errors?.[0]
          ?? err.error?.detail
          ?? 'Login failed. Please try again.';
      },
    });
  }
}
