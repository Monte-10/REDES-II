import socket

# Crear un objeto socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Vincular el socket a una dirección y un puerto
s.bind(('localhost', 8001))

# Poner el socket en modo de escucha
s.listen()

print("Esperando conexión...")
# Aceptar una conexión entrante
conn, addr = s.accept()

with conn:
    print('Conectado por', addr)
    while True:
        # Recibir datos del cliente
        data = conn.recv(1024)
        print(data)
        if not data:
            break  # Si no hay datos, salir del bucle

        # Enviar los mismos datos recibidos de vuelta al cliente
        conn.sendall(data)

# Cerrar el socket
s.close()
