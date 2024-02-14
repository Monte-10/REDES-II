# 1. Estableciendo conexiones
## 1. ¿Cuántos interfaces tiene la máquina?
La máquina tiene cinco interfaces de red, que son:
enp1s0
lo (interfaz de loopback)
virbr0
vmnet1
vmnet8
## 2. Las direcciones IP asignadas a cada interfaz, ¿son públicas o privadas? ¿Cómo puedes identificar cada una?
enp1s0 tiene asignada la dirección IP 10.250.1.21, que es una dirección privada.
Las direcciones IP privadas suelen encontrarse en los rangos 10.0.0.0 - 10.255.255.255, 172.16.0.0 - 172.31.255.255, y 192.168.0.0 - 192.168.255.255.
lo tiene asignada la dirección IP 127.0.0.1, que es una dirección de loopback, usada para que el sistema se comunique consigo mismo. 
No es ni pública ni privada en el sentido tradicional, sino que se reserva para loopback.
virbr0 tiene asignada la dirección IP 192.168.122.1, que es una dirección privada, dentro del rango 192.168.0.0 - 192.168.255.255.
vmnet1 tiene asignada la dirección IP 172.16.49.1, que es una dirección privada, dentro del rango 172.16.0.0 - 172.31.255.255.
vmnet8 tiene asignada la dirección IP 172.16.140.1, que también es una dirección privada, dentro del mismo rango de 172.16.0.0 - 172.31.255.255.
Para determinar si una dirección IP es pública o privada, se puede comparar con los rangos de direcciones IP reservados para uso privado según lo definido por la RFC 1918. Todas las direcciones IP listadas en esta salida son privadas, ya que caen dentro de los rangos reservados para redes privadas. Las direcciones públicas son aquellas que no están reservadas para uso privado y pueden ser accedidas directamente a través de Internet.

# 2. Monitorizando conexiones
## Ejecuta ahora el servidor y cliente anteriores y localiza la conexión entre ambos. ¿Cómo la has identificado? ¿Cuál es el estado?
Se ha identificado haciendo lsof -n -i | grep 8001
Desde el lado del cliente:
nc  6720  e420674  3u  IPv4  52771  0t0  TCP 10.250.1.21:52508->10.250.1.22:8001 (ESTABLISHED)
Desde el lado del servidor; si se conecta un cliente aparece también la línea de arriba
nc  8963  e423652  3u  IPv4  195858  0t0  TCP *:8001 (LISTEN)
## Cierra la conexión ahora desde el cliente, pero NO pares el servidor. ¿Se ha cerrado la conexión? ¿Qué ha pasado con el socket del servidor?
Se ha cerrado la conexión y el socket vuelve a estar libre.

# 3. Escaneando puertos
