import { Component, OnInit } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { RouterLink } from '@angular/router';
import { ApiService } from '../../services/api.service';
import { ThemeService } from '../../services/theme.service';
import { LabReport } from '../../models';

@Component({
  selector: 'app-labs',
  standalone: true,
  imports: [FormsModule, CommonModule, RouterLink],
  templateUrl: './labs.component.html',
})
export class LabsComponent implements OnInit {
  labs: LabReport[] = [];
  loading = false;
  uploading = false;
  error = '';

  transcribedConclusion: { [id: number]: string } = {};
  selectedFile: File | null = null;

  constructor(public theme: ThemeService, private api: ApiService) {}

  ngOnInit(): void {
    this.loadLabs();
  }

  loadLabs(): void {
    this.loading = true;
    this.api.getLabs().subscribe({
      next: labs => { this.labs = labs; this.loading = false; },
      error: () => { this.error = 'Failed to load lab reports.'; this.loading = false; },
    });
  }

  onFileSelected(event: Event): void {
    const input = event.target as HTMLInputElement;
    this.selectedFile = input.files?.[0] ?? null;
  }

  uploadLab(): void {
    if (!this.selectedFile) {
      this.error = 'Please select a file first.';
      return;
    }
    const fd = new FormData();
    fd.append('file', this.selectedFile);
    this.uploading = true;
    this.error = '';

    this.api.uploadLab(fd).subscribe({
      next: lab => {
        this.labs.unshift(lab);
        this.selectedFile = null;
        this.uploading = false;
      },
      error: () => { this.error = 'Upload failed.'; this.uploading = false; },
    });
  }

  saveConclusion(lab: LabReport): void {
    const text = this.transcribedConclusion[lab.id] ?? '';
    if (!text.trim()) {
      this.error = 'Conclusion cannot be empty.';
      return;
    }
    this.api.saveConclusion(lab.id, text).subscribe({
      next: updated => {
        const i = this.labs.findIndex(l => l.id === lab.id);
        if (i !== -1) this.labs[i] = updated;
      },
      error: () => { this.error = 'Failed to save conclusion.'; },
    });
  }
}
