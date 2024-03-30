#!/bin/bash

echo "Iniciando prueba de cancelación de pedido..."

# Asumiendo que el controlador ya está corriendo en background

# Registrar un nuevo cliente
echo "Registrando nuevo cliente: clientePrueba..."
python3 clients/commandline_client.py --register "clientePrueba"

sleep 2 # Espera breve para asegurar que el registro se procesa

# Crear un nuevo pedido
echo "Creando nuevo pedido: pedido001 para clientePrueba..."
python3 clients/commandline_client.py --order "clientePrueba" "pedido001" "1,2,3"

sleep 2 # Espera para dar tiempo al sistema a procesar el pedido

# Intentar cancelar el pedido creado
echo "Intentando cancelar el pedido: pedido001..."
python3 clients/commandline_client.py --cancel "clientePrueba" "pedido001"

echo "Prueba de cancelación de pedido completada."
