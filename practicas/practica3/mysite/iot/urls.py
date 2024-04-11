from django.urls import path
from .views import *

app_name = 'iot'
urlpatterns = [
    path('', index, name='index'),
    path('devices/', DeviceListView.as_view(), name='device_list'),
    path('devices/new/', DeviceCreateView.as_view(), name='device_new'),
    path('devices/<pk>/', DeviceDetailView.as_view(), name='device_detail'),
    path('devices/<pk>/edit/', DeviceUpdateView.as_view(), name='device_edit'),
    path('device/<pk>/remove/', DeviceDeleteView.as_view(), name='device_remove'),
    path('rules/', RuleListView.as_view(), name='rule_list'),
    path('rules/new/', RuleCreateView.as_view(), name='rule_new'),
    path('rules/<int:pk>/edit/', RuleUpdateView.as_view(), name='rule_edit'),
    path('rules/<int:pk>/delete/', RuleDeleteView.as_view(), name='rule_delete'),
]