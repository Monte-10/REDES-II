#!/bin/bash

echo "Iniciando prueba de múltiples pedidos simultáneos..."

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

# Registrar cliente
echo "Registrando cliente: multi_order_client..."
python3 clients/commandline_client.py --register "multi_order_client"
sleep 1  # Dar tiempo para asegurar el registro

# Realizar múltiples pedidos
echo "Realizando pedido multi1..."
python3 clients/commandline_client.py --order "multi_order_client" "multi1" "1,2"
sleep 3
echo "Realizando pedido multi2..."
python3 clients/commandline_client.py --order "multi_order_client" "multi2" "3,4"
sleep 3
echo "Realizando pedido multi3..."
python3 clients/commandline_client.py --order "multi_order_client" "multi3" "5,6"

sleep 30  # Dar tiempo para procesar los pedidos

# Opcional: Verificar el estado de los pedidos
echo "Verificando el estado de multi1..."
python3 clients/commandline_client.py --status "multi_order_client" "multi1"
echo "Verificando el estado de multi2..."
python3 clients/commandline_client.py --status "multi_order_client" "multi2"
echo "Verificando el estado de multi3..."
python3 clients/commandline_client.py --status "multi_order_client" "multi3"

# Limpiar procesos al finalizar la prueba
kill $CONTROLLER_PID $ROBOT_PID $DELIVERY_PID
echo "Prueba de múltiples pedidos simultáneos completada."
