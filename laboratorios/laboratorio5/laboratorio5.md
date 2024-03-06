# Confirmaciones de entrega (acknowledgments)
## ¿Se vuelven a encolar los mensajes al terminar el consumidor?, ¿qué crees que pasa en RabbitMQ con la memoria de los mensajes sin ack?
Al arrancar el servidor de nuevo aparecen los mensajes que se enviaron en las sesiones anteriores. La memoria se llena porque no se eliminan los mensajes
## Repite las pruebas añadiendo como parámetro auto_ack=True
Sólo se muestran los mensajes enviados en esa sesión
