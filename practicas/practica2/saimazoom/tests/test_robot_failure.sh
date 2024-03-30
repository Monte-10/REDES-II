#!/bin/bash

echo "Iniciando prueba de fallo en la recogida por robot..."

# Iniciar controlador y robot en background
python3 controller/launch_controller.py &
CONTROLLER_PID=$!
echo "Controlador iniciado con PID $CONTROLLER_PID"

python3 robots/launch_robot.py &
ROBOT_PID=$!
echo "Robot iniciado con PID $ROBOT_PID"

sleep 2  # Esperar a que estén listos

# Registrar cliente y hacer pedido
echo "Registrando cliente: test_failure..."
python3 clients/commandline_client.py --register "test_failure"
sleep 1  # Espera corta para asegurar el registro

echo "Realizando pedido: failure_order para test_failure..."
python3 clients/commandline_client.py --order "test_failure" "failure_order" "4,5"

sleep 20  # Dar tiempo para procesar el pedido y simular el fallo

# Limpiar al finalizar la prueba
kill $CONTROLLER_PID $ROBOT_PID
echo "Prueba de fallo en robot completada."
