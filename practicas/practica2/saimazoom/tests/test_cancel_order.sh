#!/bin/bash

echo "Iniciando prueba de cancelación de pedido..."

# Asumiendo que el controlador ya está corriendo en background

# Intentar cancelar un pedido
python3 clients/launch_client.py --cancel "clientePrueba" "pedido001"

echo "Prueba de cancelación de pedido completada."
