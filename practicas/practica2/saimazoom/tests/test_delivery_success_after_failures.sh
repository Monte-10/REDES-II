#!/bin/bash

echo "Iniciando prueba de entrega exitosa tras intentos fallidos..."

# Asumiendo que el controlador, robot y repartidor ya están corriendo
# El repartidor necesita estar configurado para simular fallos y éxitos en entregas

# Registrar cliente y realizar un pedido que inicialmente falla, pero eventualmente tiene éxito
python3 clients/launch_client.py --register "clienteExitoDespuesFallo"
sleep 1
python3 clients/launch_client.py --order "clienteExitoDespuesFallo" "pedidoExitoFallo" "4,5"

sleep 10  # Dar tiempo para el proceso de entrega

echo "Prueba de entrega exitosa tras intentos fallidos completada."
