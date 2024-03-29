# tests/test_multiple_orders.sh
echo "Iniciando prueba de múltiples pedidos simultáneos..."

# Iniciar controlador, robot y repartidor
python3 controller/launch_controller.py &
CONTROLLER_PID=$!
python3 robots/launch_robot.py &
ROBOT_PID=$!
python3 delivery/launch_delivery.py &
DELIVERY_PID=$!

sleep 2  # Esperar a que estén listos

# Registrar cliente
python3 clients/commandline_client.py --register multi_order_client

# Realizar múltiples pedidos
python3 clients/commandline_client.py --order multi_order_client multi1 "1,2"
python3 clients/commandline_client.py --order multi_order_client multi2 "3,4"
python3 clients/commandline_client.py --order multi_order_client multi3 "5,6"

sleep 10  # Dar tiempo para procesar

# Limpiar
kill $CONTROLLER_PID $ROBOT_PID $DELIVERY_PID
echo "Prueba de múltiples pedidos simultáneos completada."
