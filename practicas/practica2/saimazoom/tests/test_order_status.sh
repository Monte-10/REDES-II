#!/bin/bash

echo "Iniciando prueba de consulta de estado de pedido..."

# Asumiendo que el controlador ya está corriendo en background

# Consultar estado de un pedido existente
python3 clients/launch_client.py --status "clientePrueba" "pedido001"

echo "Prueba de consulta de estado de pedido completada."
