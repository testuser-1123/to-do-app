import { Component, OnInit } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { RouterLink } from '@angular/router';
import { ApiService } from '../../services/api.service';
import { SymptomEntry } from '../../models';

@Component({
  selector: 'app-symptoms',
  standalone: true,
  imports: [FormsModule, CommonModule, RouterLink],
  templateUrl: './symptoms.component.html',
})
export class SymptomsComponent implements OnInit {
  symptoms: SymptomEntry[] = [];
  searchResults: SymptomEntry[] = [];
  loading = false;
  searching = false;
  error = '';
  formError = '';

  searchQuery = '';
  name = '';
  severity = 5;
  notes = '';

  constructor(private api: ApiService) {}

  ngOnInit(): void {
    this.loadSymptoms();
  }

  loadSymptoms(): void {
    this.loading = true;
    this.api.getSymptoms().subscribe({
      next: s => { this.symptoms = s; this.loading = false; },
      error: () => { this.error = 'Failed to load symptoms.'; this.loading = false; },
    });
  }

  searchSymptom(): void {
    if (!this.searchQuery.trim()) return;
    this.searching = true;
    this.error = '';

    this.api.searchSymptoms(this.searchQuery).subscribe({
      next: r => { this.searchResults = r; this.searching = false; },
      error: (err) => {
        this.error = err.error?.query?.[0] ?? 'Search failed.';
        this.searching = false;
      },
    });
  }

  saveSymptom(): void {
    if (!this.name.trim()) {
      this.formError = 'Symptom name is required.';
      return;
    }
    this.formError = '';
    this.api.saveSymptom({ name: this.name, severity: this.severity, notes: this.notes }).subscribe({
      next: s => {
        this.symptoms.unshift(s);
        this.name = '';
        this.severity = 5;
        this.notes = '';
      },
      error: (err) => {
        this.formError = err.error?.name?.[0] ?? 'Failed to save symptom.';
      },
    });
  }
}
