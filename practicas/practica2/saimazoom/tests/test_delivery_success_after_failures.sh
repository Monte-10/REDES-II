#!/bin/bash

echo "Iniciando prueba de entrega exitosa tras intentos fallidos..."

# Asumiendo que el controlador, robot y repartidor ya están corriendo en el entorno

# Registrar un nuevo cliente
echo "Registrando cliente: clienteExitoDespuesFallo..."
python3 clients/commandline_client.py --register "clienteExitoDespuesFallo"
sleep 1  # Dar tiempo para asegurar el registro

# Realizar un nuevo pedido
echo "Realizando pedido: pedidoExitoFallo para clienteExitoDespuesFallo..."
python3 clients/commandline_client.py --order "clienteExitoDespuesFallo" "pedidoExitoFallo" "4,5"

# Este sleep es para dar tiempo suficiente al sistema para procesar el pedido,
# incluyendo los intentos fallidos de entrega y el intento exitoso.
sleep 30  

# Verificar el estado del pedido
# Este paso es opcional
echo "Verificando el estado del pedido: pedidoExitoFallo..."
python3 clients/commandline_client.py --status "clienteExitoDespuesFallo" "pedidoExitoFallo"

echo "Prueba de entrega exitosa tras intentos fallidos completada."
