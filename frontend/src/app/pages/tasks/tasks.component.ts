import { Component, OnInit } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { RouterLink } from '@angular/router';
import { ApiService } from '../../services/api.service';
import { ThemeService } from '../../services/theme.service';
import { MedicalTask } from '../../models';

@Component({
  selector: 'app-tasks',
  standalone: true,
  imports: [FormsModule, CommonModule, RouterLink],
  templateUrl: './tasks.component.html',
})
export class TasksComponent implements OnInit {
  tasks: MedicalTask[] = [];
  loading = false;
  error = '';

  title = '';
  consequenceText = '';
  dueDate = '';
  validUntil = '';
  currentStock = 0;
  showForm = false;
  formError = '';

  constructor(public theme: ThemeService, private api: ApiService) {}

  ngOnInit(): void {
    this.loadTasks();
  }

  loadTasks(): void {
    this.loading = true;
    this.api.getTasks().subscribe({
      next: tasks => { this.tasks = tasks; this.loading = false; },
      error: () => { this.error = 'Failed to load tasks.'; this.loading = false; },
    });
  }

  saveTask(): void {
    if (!this.title.trim()) {
      this.formError = 'Title is required.';
      return;
    }
    this.formError = '';
    this.api.createTask({
      title: this.title,
      consequence_text: this.consequenceText,
      due_date: this.dueDate || null,
      valid_until: this.validUntil || null,
      current_stock: this.currentStock,
    }).subscribe({
      next: task => {
        this.tasks.unshift(task);
        this.resetForm();
      },
      error: (err) => {
        this.formError = err.error?.title?.[0] ?? 'Failed to save task.';
      },
    });
  }

  markDone(task: MedicalTask): void {
    this.api.updateTask(task.id, { is_done: true }).subscribe({
      next: updated => {
        const i = this.tasks.findIndex(t => t.id === task.id);
        if (i !== -1) this.tasks[i] = updated;
      },
      error: () => { this.error = 'Failed to update task.'; },
    });
  }

  deleteTask(id: number): void {
    this.api.deleteTask(id).subscribe({
      next: () => { this.tasks = this.tasks.filter(t => t.id !== id); },
      error: () => { this.error = 'Failed to delete task.'; },
    });
  }

  resetForm(): void {
    this.title = '';
    this.consequenceText = '';
    this.dueDate = '';
    this.validUntil = '';
    this.currentStock = 0;
    this.showForm = false;
  }
}
