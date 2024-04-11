#!/bin/bash
echo "Starting MQTT Controller..."
python3 manage.py startmqtt &  # Asegúrate de que esto corre en el fondo
MQTT_PID=$!
echo "Controller running with PID $MQTT_PID"

echo "Simulating devices..."
python3 simulators/dummy-switch.py --host localhost --port 1883 --probability 0.3 1 &
SWITCH_PID=$!
python3 simulators/dummy-sensor.py --host localhost --port 1883 --min 20 --max 30 --increment 1 --interval 1 2 &
SENSOR_PID=$!
python3 simulators/dummy-clock.py --host localhost --port 1883 --time "09:00:00" --increment 60 --rate 1 1 &
CLOCK_PID=$!
echo "Devices running: Switch PID=$SWITCH_PID, Sensor PID=$SENSOR_PID, Clock PID=$CLOCK_PID"

echo "Running simulation for 30 seconds..."
sleep 30

echo "Killing all processes..."
kill $MQTT_PID $SWITCH_PID $SENSOR_PID $CLOCK_PID
echo "Simulation complete."
