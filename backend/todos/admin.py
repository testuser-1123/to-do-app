from django.contrib import admin
from .models import Category, Task, Subtask

admin.site.register(Category)
admin.site.register(Task)
admin.site.register(Subtask)