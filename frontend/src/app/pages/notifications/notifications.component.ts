import { Component, OnInit, OnDestroy } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink } from '@angular/router';
import { ApiService } from '../../services/api.service';
import { Notification } from '../../models';

@Component({
  selector: 'app-notifications',
  standalone: true,
  imports: [CommonModule, RouterLink],
  templateUrl: './notifications.component.html',
})
export class NotificationsComponent implements OnInit, OnDestroy {
  notifications: Notification[] = [];
  loading = false;
  error = '';
  private pollTimer: any;

  constructor(private api: ApiService) {}

  ngOnInit(): void {
    this.load();
    this.pollTimer = setInterval(() => this.load(), 30_000);
  }

  ngOnDestroy(): void {
    clearInterval(this.pollTimer);
  }

  load(): void {
    this.api.getNotifications().subscribe({
      next: all => {
        this.notifications = all.filter(n =>
          n.level === 'escalation' || !n.is_expired || !n.is_read
        );
      },
      error: () => { this.error = 'Failed to fetch notifications.'; },
    });
  }

  clear(n: Notification): void {
    this.api.clearNotification(n.id).subscribe({
      next: updated => {
        const i = this.notifications.findIndex(x => x.id === n.id);
        if (i !== -1) this.notifications[i] = updated;
      },
      error: () => { this.error = 'Failed to clear notification.'; },
    });
  }
}
