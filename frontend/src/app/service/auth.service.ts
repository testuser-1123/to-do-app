import { Injectable } from '@angular/core';
import { Router } from '@angular/router';
import { BehaviorSubject, Observable, tap, catchError, throwError } from 'rxjs';
import { ApiService } from './api.service';
import { AuthTokens } from '../models';

const ACCESS_KEY  = 'med_access';
const REFRESH_KEY = 'med_refresh';

@Injectable({ providedIn: 'root' })
export class AuthService {
  private _loggedIn = new BehaviorSubject<boolean>(this.hasValidToken());
  readonly loggedIn$ = this._loggedIn.asObservable();

  constructor(private api: ApiService, private router: Router) {}

  private hasValidToken(): boolean {
    return !!localStorage.getItem(ACCESS_KEY);
  }

  getAccessToken(): string | null {
    return localStorage.getItem(ACCESS_KEY);
  }

  getRefreshToken(): string | null {
    return localStorage.getItem(REFRESH_KEY);
  }

  storeTokens(tokens: AuthTokens): void {
    localStorage.setItem(ACCESS_KEY, tokens.access);
    localStorage.setItem(REFRESH_KEY, tokens.refresh);
  }

  clearTokens(): void {
    localStorage.removeItem(ACCESS_KEY);
    localStorage.removeItem(REFRESH_KEY);
    this._loggedIn.next(false);
  }

  login(username: string, password: string): Observable<AuthTokens> {
    return this.api.login(username, password).pipe(
      tap(tokens => {
        this.storeTokens(tokens);
        this._loggedIn.next(true);
      })
    );
  }

  logout(): void {
    const refresh = this.getRefreshToken();
    if (refresh) {
      this.api.logout(refresh).subscribe({ error: () => {} });
    }
    this.clearTokens();
    this.router.navigate(['/login']);
  }

  /** Called by HTTP interceptor on 401 */
  handleUnauthorized(): void {
    this.clearTokens();
    this.router.navigate(['/login']);
  }

  isAuthenticated(): boolean {
    return this.hasValidToken();
  }
}
