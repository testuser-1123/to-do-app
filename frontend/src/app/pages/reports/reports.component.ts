import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { RouterLink } from '@angular/router';
import { ApiService } from '../../services/api.service';

@Component({
  selector: 'app-reports',
  standalone: true,
  imports: [FormsModule, CommonModule, RouterLink],
  templateUrl: './reports.component.html',
})
export class ReportsComponent {
  fromDate = '';
  toDate = '';
  loading = false;
  error = '';
  fieldErrors: Record<string, string> = {};

  constructor(private api: ApiService) {}

  generatePdf(): void {
    this.fieldErrors = {};
    if (!this.fromDate) { this.fieldErrors['fromDate'] = 'Start date is required.'; }
    if (!this.toDate)   { this.fieldErrors['toDate']   = 'End date is required.'; }
    if (Object.keys(this.fieldErrors).length) return;

    this.loading = true;
    this.error = '';
    this.api.generatePdf(this.fromDate, this.toDate).subscribe({
      next: (blob) => {
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `report_${this.fromDate}_${this.toDate}.pdf`;
        a.click();
        URL.revokeObjectURL(url);
        this.loading = false;
      },
      error: (err) => {
        this.loading = false;
        this.error = err.error?.non_field_errors?.[0] ?? 'Failed to generate report.';
      },
    });
  }
}
