from django.shortcuts import render
from .keepalived import generate_keepalived_config
from django.shortcuts import render, redirect
from .forms import HAConfigForm

def ha_config(request):
    if request.method == 'POST':
        form = HAConfigForm(request.POST)
        if form.is_valid():
           obj = form.save()
           generate_keepalived_config(obj)
           return redirect('/')

    else:
        form = HAConfigForm()

    return render(request, 'ha/config.html', {'form': form})

# Create your views here.
