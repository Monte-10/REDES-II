# tests/test_robot_failure.sh
echo "Iniciando prueba de fallo en la recogida por robot..."

# Iniciar controlador y robot
python3 controller/launch_controller.py &
CONTROLLER_PID=$!

python3 robots/launch_robot.py --failure-rate 1.0 &  # Asumiendo que agregas soporte para una tasa de fallo
ROBOT_PID=$!

sleep 2  # Esperar a que estén listos

# Registrar cliente y hacer pedido
python3 clients/commandline_client.py --register test_failure
sleep 1
python3 clients/commandline_client.py --order test_failure failure_order "4,5"

sleep 5  # Dar tiempo para procesar

# Limpiar
kill $CONTROLLER_PID $ROBOT_PID
echo "Prueba de fallo en robot completada."
