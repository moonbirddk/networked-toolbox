import logging

from django.shortcuts import render, redirect
from django.contrib import messages

from .forms import AddToolForm
from .models import Tool

log = logging.getLogger(__name__)

def home(request):
    return render(request, 'tools/home.html', {})

def add_tool(request):

    form = AddToolForm()

    if request.method == 'POST':
        form = AddToolForm(request.POST)
        if form.is_valid():
            log.debug(form.cleaned_data)
            tool = Tool.objects.create(**form.cleaned_data)
            messages.success(request, "You created a tool")
            return redirect('/')

    context = {'form': form}
    return render(request,'tools/add.html', context)

