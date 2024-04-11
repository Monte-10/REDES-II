from django.shortcuts import render, redirect
from .models import Dispositivo
from .forms import DispositivoForm

def lista_dispositivos(request):
    dispositivos = Dispositivo.objects.all()
    return render(request, 'list.html', {'dispositivos': dispositivos})

def nuevo_dispositivo(request):
    if request.method == "POST":
        form = DispositivoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_dispositivos')
    else:
        form = DispositivoForm()
    return render(request, 'new.html', {'form': form})

def editar_dispositivo(request, pk):
    dispositivo = Dispositivo.objects.get(pk=pk)
    if request.method == "POST":
        form = DispositivoForm(request.POST, instance=dispositivo)
        if form.is_valid():
            form.save()
            return redirect('lista_dispositivos')
    else:
        form = DispositivoForm(instance=dispositivo)
    return render(request, 'edit.html', {'form': form})