#!/bin/bash

echo "Iniciando prueba de registro de cliente y realización de pedido..."

# Iniciar el controlador en background
python3 controller/launch_controller.py &
CONTROLLER_PID=$!
echo "Controlador iniciado con PID $CONTROLLER_PID"

sleep 2  # Esperar a que el controlador esté listo

# Registrar un nuevo cliente
echo "Registrando cliente: clientePrueba..."
python3 clients/commandline_client.py --register "clientePrueba"
sleep 1  # Espera corta para asegurar el registro

# Realizar un nuevo pedido
echo "Realizando pedido: pedido001 por clientePrueba..."
python3 clients/commandline_client.py --order "clientePrueba" "pedido001" "1,2,3"

sleep 30  # Dar tiempo para que el pedido se procese

# Finalizar el controlador
kill $CONTROLLER_PID
echo "Prueba de registro y pedido completada."
