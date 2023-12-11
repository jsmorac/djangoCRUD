from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import TaskForm
from .models import Task
from django.utils import timezone
from django.contrib.auth.decorators import login_required #con esto impedimos que se pueda ingresar a un url si no se tiene el usuario logueado
#los que tienen los login required son las paginas a las que no se puede acceder si no esta logueado

# Create your views here.


def home(request):
    return render(request, 'home.html')


def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html', {
            'form': UserCreationForm
        })
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(
                    username=request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('tasks')
            except IntegrityError:
                return render(request, 'signup.html', {
                    'form': UserCreationForm,
                    'error': 'User already exist'
                })
        return render(request, 'signup.html', {
            'form': UserCreationForm,
            'error': 'Contraseña no coincide'
        })

@login_required
def tasks(request):
    tasks = Task.objects.filter(user = request.user, datencompleted__isnull=True) #Me devuelve solo las tareas de la base de datos que correspondan al usuario y tambien con el datencompleted muestra en pantalla solo las tareas que aun no estan completas con la fecha(ademas con esto se ve las tareas desde el fornt y no solo desde el admin )
    return render(request, 'tasks.html', {'tasks': tasks}) #con esto se esta enviando un datos que se llama 'tasks' que contiene las tareas

@login_required
def tasks_completed(request):
    tasks = Task.objects.filter(user = request.user, datencompleted__isnull=False) .order_by('-datencompleted')# basicamente ahora los time que ya esten son las que estan completas y con el (-) las ordena desde la ultima hasta la anterior
    return render(request, 'tasks.html', {'tasks': tasks})
        
@login_required
def create_task(request):
    if request.method == 'GET': #peticion del navegador cuando se revisa
        return render(request, 'create_task.html',{
            'form' : TaskForm
        })
    else:
        try:
            form = TaskForm(request.POST)
            new_task = form.save(commit=False)# Esto sirve para guardar los datos en una instancia de base de datos pero con el false no lo guarda
            new_task.user = request.user #Este es para asignarle la tarea al usuario
            new_task.save()#Esto sirve para generar un dato en la base de datos
            return redirect('tasks')
        except ValueError:#esta parte sirve para mostrar de nuevo el formulario pero con un error de valor
            return render(request, 'create_task.html',{
                'form' : TaskForm,
                'error': 'Datos no validos',
            })

@login_required
def task_detail(request, task_id):#recibe un id, revisar el urls
    if request.method == 'GET':#Recordar que se usa el methodo get se utiliza para solicitar datos de la pagina
        task = get_object_or_404(Task,pk=task_id, user =request.user)#Sirve para buscar un dato donde task_id da la tarea sin embargo con el get... ayuda a que al buscar una tarea que no existe como la numero 100 no se caiga el servicor si no que salga error 404. El Task es necesario ya que es el modelo que va a consultar. Por ultimo el user es necesario para que solo el usuario pueda acceder a sus tareas y no a la de otros usuarios.
        form = TaskForm(instance=task)#llena el formulario con esa tarea
        return render(request, 'task_detail.html',{'task':task, 'form':form})#recordar que el 'task' simplemente es una variable que va a contener lo de task
    else:
        try:
            task = get_object_or_404(Task,pk=task_id, user =request.user)
            form = TaskForm(request.POST, instance=task)#recibe los datos nuevo y genera un nuevo formulario
            form.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'task_detail.html',{'task':task, 'form':form, 'error':'error actualizando la tarea'})

@login_required
def complete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id , user = request.user)
    if request.method == 'POST':
        task.datencompleted = timezone.now()#Basicamente cuando el tiempo se guarde la tarea ya esta completa
        task.save()
        return redirect('tasks')

@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id , user = request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('tasks')

@login_required
def signout(request):#cerrar sesion
    logout(request)
    return redirect('home')


def signin(request):#Iniciar sesion con usuario ya creado
    if request.method == 'GET':
        return render(request, 'signin.html',{
            'form':AuthenticationForm
        })
    else:
        user = authenticate(request, username=request.POST['username'], password = request.POST['password'])
        if user is None:#basicamente si el usuario o la contraseña es incorrecto te devuelve al mismo formulario pero te sale el mensaje de error
            return render(request, 'signin.html',{
            'form':AuthenticationForm,
            'error': 'Usuario o contraseña incorrecta'
        })
        else:#caso contrario se va a la pagina tarea y con el login se guarda la sesion
            login(request, user)
            return redirect('tasks')
