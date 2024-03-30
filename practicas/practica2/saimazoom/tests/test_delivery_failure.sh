#!/bin/bash

echo "Iniciando prueba de falla en la entrega por repartidor..."

# Iniciar controlador, robot y repartidor en background
python3 controller/launch_controller.py &
CONTROLLER_PID=$!
echo "Controlador iniciado con PID $CONTROLLER_PID"

python3 robots/launch_robot.py &
ROBOT_PID=$!
echo "Robot iniciado con PID $ROBOT_PID"

python3 delivery/launch_delivery.py &
DELIVERY_PID=$!
echo "Repartidor iniciado con PID $DELIVERY_PID"

sleep 2  # Esperar a que estén listos

# Registrar cliente y realizar un pedido
python3 clients/commandline_client.py --register "clienteFalloEntrega"
sleep 1  # Esperar a que se complete el registro
python3 clients/commandline_client.py --order "clienteFalloEntrega" "pedidoFallo" "1,2,3"

sleep 30  # Dar tiempo para el proceso de entrega

# Finalizar procesos
kill $CONTROLLER_PID $ROBOT_PID $DELIVERY_PID
echo "Prueba de falla en entrega completada."
