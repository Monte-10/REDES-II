from django.db import models

from django.db import models

from django.db import models

class Device(models.Model):
    DEVICE_TYPES = (
        ('switch', 'Interruptor'),
        ('sensor', 'Sensor'),
        ('clock', 'Reloj'),
    )
    device_type = models.CharField(max_length=10, choices=DEVICE_TYPES)
    state = models.CharField(max_length=50)
    mqtt_topic = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.id} ({self.device_type})"

class Rule(models.Model):
    # Información básica de la regla
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    # Componentes de la condición de la regla
    subject = models.CharField(max_length=100, help_text="The subject to check, e.g., 'temperature'", default='temperature')
    operator = models.CharField(max_length=2, choices=[('==', 'equals'), ('>', 'greater than'), ('<', 'less than')], help_text="Comparison operator", default='==')
    value = models.CharField(max_length=50, help_text="Value to compare the subject against, e.g., '25'", default='25')

    # Acción a realizar cuando se cumple la condición
    action = models.CharField(max_length=255, help_text="Action to perform, e.g., 'turn_on: heater'")

    def __str__(self):
        return f"{self.description}: If {self.subject} {self.operator} {self.value}, then {self.action}"