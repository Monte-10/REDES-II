from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import *

def index(request):
    return render(request, 'index.html')

class DeviceListView(ListView):
    model = Device
    context_object_name = 'devices'
    template_name = 'iot/device_list.html'

class DeviceDetailView(DetailView):
    model = Device
    context_object_name = 'device'
    template_name = 'iot/device_detail.html'

class DeviceCreateView(CreateView):
    model = Device
    fields = ['id', 'device_type', 'state', 'mqtt_topic']
    template_name = 'iot/device_form.html'
    success_url = reverse_lazy('iot:device_list')

class DeviceUpdateView(UpdateView):
    model = Device
    fields = ['id', 'device_type', 'state', 'mqtt_topic']
    template_name = 'iot/device_form.html'
    success_url = reverse_lazy('iot:device_list')

class DeviceDeleteView(DeleteView):
    model = Device
    context_object_name = 'device'
    template_name = 'iot/device_confirm_delete.html'
    success_url = reverse_lazy('iot:device_list')
    
class RuleListView(ListView):
    model = Rule
    context_object_name = 'rules'
    template_name = 'iot/rule_list.html'

class RuleCreateView(CreateView):
    model = Rule
    template_name = 'iot/rule_form.html'
    fields = ['description', 'subject', 'operator', 'value', 'action']
    success_url = reverse_lazy('iot:rule_list')

class RuleUpdateView(UpdateView):
    model = Rule
    template_name = 'iot/rule_form.html'
    fields = ['description', 'subject', 'operator', 'value', 'action']
    success_url = reverse_lazy('iot:rule_list')

class RuleDeleteView(DeleteView):
    model = Rule
    context_object_name = 'rule'
    template_name = 'iot/rule_confirm_delete.html'
    success_url = reverse_lazy('iot:rule_list')