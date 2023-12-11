from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)#sirve para guardar fecha y hora de cuando fue creada la tarea(lo hace por defecto por los parentesis)
    datencompleted = models.DateTimeField(null=True, blank=True)#el usuario pone la fecha cuando cumple una tarea y con el blank se refiere que es opcional para el admin
    important = models.BooleanField(default=False)#Todas las tareas no son importantes por las que ponen en true si lo son
    user = models.ForeignKey(User, on_delete=models.CASCADE)# el user tiene relacionado un id que es capaz de eliminar al usuario junto con las tareas con el models.cascade
    def __str__(self):
        return self.title + ' -by '+ self.user.username # esto sirve para poner el nombre de la tarea en la pagina junto con el nombre de usuario