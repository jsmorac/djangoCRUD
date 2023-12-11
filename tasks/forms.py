from django import forms 
from .models import Task

class TaskForm(forms.ModelForm):#esto me permite extender formularios
    class Meta:
        model = Task
        fields = ['title', 'description', 'important'] #Estoy accendiendo solo a esos items del formulario creado en models.py
        widgets = {
            'title':forms.TextInput(attrs={'class': 'form-control'}),
            'description':forms.Textarea(attrs={'class': 'form-control'}),
            'important':forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }