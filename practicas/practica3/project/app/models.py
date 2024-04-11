from django.db import models

class Dispositivo(models.Model):
    # Aquí defines los campos de tu modelo
    nombre = models.CharField(max_length=100)
    tipo = models.CharField(max_length=50)
    estado = models.CharField(max_length=50)
    # Más campos según sea necesario

class Regla(models.Model):
    # Define el modelo para las reglas
    descripcion = models.TextField()
    # Más campos que definen la regla
