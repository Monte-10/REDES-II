#!/bin/bash

echo "Iniciando prueba con múltiples robots y repartidores..."

# Iniciar controlador, múltiples robots y repartidores en background
python3 controller/launch_controller.py &
CONTROLLER_PID=$!
echo "Controlador iniciado con PID $CONTROLLER_PID"

# Iniciar múltiples instancias de robots y repartidores
for i in {1..3}; do
    python3 robots/launch_robot.py &
    python3 delivery/launch_delivery.py &
done

sleep 2  # Esperar a que estén listos

# Registrar un cliente
echo "Registrando cliente: clienteMulti..."
python3 clients/commandline_client.py --register "clienteMulti"
sleep 1  # Dar tiempo para asegurar el registro

# Realizar múltiples pedidos
for i in {1..5}; do
    order_id="multiOrder$i"
    echo "Realizando pedido: $order_id..."
    python3 clients/commandline_client.py --order "clienteMulti" "$order_id" "1,2,3"
    sleep 2  # Pequeña pausa entre pedidos para permitir el procesamiento
done

sleep 60  # Dar tiempo para procesar los pedidos

# Finalizar todos los procesos
kill $CONTROLLER_PID
pkill -f launch_robot.py
pkill -f launch_delivery.py
echo "Prueba con múltiples robots y repartidores completada."
