from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from .forms import DeviceCreateForm
from .models import Device
from .models import LatencyTest
from django.utils import timezone
from pythonping import ping
import subprocess
from django.contrib.auth.decorators import login_required
from collections import Counter
# Create your views here.


def home(request):

    return render(request, 'home.html')


def signup(request):

    if request.method == 'GET':
        return render(request, 'signup.html', {
            "form": UserCreationForm
        })
    else:
        if request.POST['password1'] == request.POST['password2']:
            # register user
            try:
                user = User.objects.create_user(
                    username=request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('devices')
            except:
                return render(request, 'signup.html', {
                    "form": UserCreationForm,
                    'error': 'Usuario ya existe'
                })

        else:
            return render(request, 'signup.html', {
                "form": UserCreationForm,
                'error': 'Contraseñas no coinciden'
            })


@login_required
def devices(request):
    devices = Device.objects.all()
    # devices = Device.objects.filter(user=request.user)

    return render(request, 'devices.html', {
        'devices': devices
    })


@login_required
def pingTest(request):
    pingTests = LatencyTest.objects.all().order_by('-dateTest')
    pingTests = pingTests[::-1]
    pingCount = len(pingTests)
    devices = Device.objects.all()
    pruebas = LatencyTest.objects.all()
    devicesCount = devices.count()

    equipos = Device.objects.values()
    pruebas = LatencyTest.objects.values()

    conectan = LatencyTest.objects.filter(result='Conecto').count()
    noConectan = LatencyTest.objects.filter(result='No conecto').count()

    equipos = list(equipos)
    pruebas = list(pruebas)

    for x in equipos:
        flag = 0
        print()
        for y in pruebas:
            if x['id'] == y['device_id']:
                flag = flag + 1
        x['equiposRepetido'] = flag

    return render(request, 'pingTest.html', {
        'pingTests': pingTests,
        'pingCount': pingCount,
        'devices': devices,
        'devicesCount': devicesCount,
        'conectan': conectan,
        'noConectan': noConectan,
        'equipos': equipos,
    })


@login_required
def deviceCreate(request):
    if request.method == 'GET':
        return render(request, 'deviceCreate.html', {
            'form': DeviceCreateForm
        })
    else:
        try:
            device = DeviceCreateForm(request.POST)
            newDevice = device.save(commit=False)
            newDevice.user = request.user
            newDevice.save()
            return redirect('devices')
        except:
            return render(request, 'deviceCreate.html', {
                'form': DeviceCreateForm,
                'error': 'Introduzca datos validos'
            })


@login_required
def deviceDetail(request, device_id):
    if request.method == 'GET':
        device = get_object_or_404(Device, pk=device_id, user=request.user)
        form = DeviceCreateForm(instance=device)
        return render(request, 'deviceDetail.html', {
            'device': device,
            'form': form,
        })
    else:
        try:
            device = get_object_or_404(Device, pk=device_id, user=request.user)
            deviceForm = DeviceCreateForm(request.POST, instance=device)
            deviceForm.save()
            return redirect('devices')
        except ValueError:
            return render(request, 'deviceDetail.html', {
                'device': device,
                'form': form,
                'error': 'Error al actualizar el dispositivo'
            })


@login_required
def deviceDelete(request, device_id):
    device = get_object_or_404(Device, pk=device_id)
    if request.method == 'POST':
        device.delete()
        return redirect('devices')


@login_required
def devicePing(request, device_id):
    device = get_object_or_404(Device, pk=device_id)
    test = LatencyTest()
    print(request.user)
    if request.method == 'POST':
        # pingResult = ping(device.ipAdress)
        pingResult = subprocess.call(['ping', '-n', '1', device.ipAdress])
        if pingResult == 0:
            result = 'Conecto'
        else:
            result = 'No conecto'
        test.device = device
        test.dateTest = timezone.now()
        test.result = result
        test.user = request.user
        test.save()
        return redirect('devices')


@login_required
def signout(request):
    logout(request)
    return redirect('home')


def signin(request):
    if request.method == "GET":
        return render(request, 'signin.html', {
            'form': AuthenticationForm,
        })
    else:
        user = authenticate(
            request, username=request.POST["username"], password=request.POST["password"])
        if user is None:
            return render(request, 'signin.html', {
                'form': AuthenticationForm,
                'error': "Usuario o Contraseña incorrecto"
            })
        else:
            login(request, user)
            return redirect('devices')
