from django.contrib import admin
from .models import Task
# Register your models here.

class TaskAdmin(admin.ModelAdmin):# Con esta clase de manera automatica muestra la fecha creada y es de solo lectura
    readonly_fields = ('created',)
admin.site.register(Task, TaskAdmin)
