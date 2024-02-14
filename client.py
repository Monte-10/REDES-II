import socket

# Crear un objeto socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Conectar el socket a una dirección específica
s.connect(('localhost', 8001))

# Aquí puedes enviar y recibir datos usando s.send() y s.recv()
s.send("pito")
# Asegúrate de cerrar la conexión una vez completada la comunicación
s.close()
