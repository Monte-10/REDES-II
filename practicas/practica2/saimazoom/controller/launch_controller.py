# launch_controller.py
import pika
import json
from utils.config import (RABBITMQ_HOST, RABBITMQ_PORT, RABBITMQ_USERNAME,
                          RABBITMQ_PASSWORD, ORDER_QUEUE, ROBOT_WORK_QUEUE,
                          DELIVERY_QUEUE, CLIENT_REGISTRATION_QUEUE,
                          CLIENT_STATUS_QUEUE, CLIENT_CANCEL_QUEUE, ROBOT_STATUS_QUEUE, DELIVERY_STATUS_QUEUE)

class Controller:
    def __init__(self):
        self.connection = self.create_connection()
        self.channel = self.connection.channel()
        self.setup_queues()
        self.clients = {}  # Registro de clientes
        self.orders = {}  # Registro de pedidos

    def create_connection(self):
        """Establece la conexión con RabbitMQ."""
        credentials = pika.PlainCredentials(RABBITMQ_USERNAME, RABBITMQ_PASSWORD)
        return pika.BlockingConnection(
            pika.ConnectionParameters(host=RABBITMQ_HOST, port=RABBITMQ_PORT, credentials=credentials)
        )

    def setup_queues(self):
        """Declara las colas necesarias en RabbitMQ."""
        queues = [ORDER_QUEUE, ROBOT_WORK_QUEUE, DELIVERY_QUEUE,
                CLIENT_REGISTRATION_QUEUE, CLIENT_STATUS_QUEUE, CLIENT_CANCEL_QUEUE, ROBOT_STATUS_QUEUE, DELIVERY_STATUS_QUEUE]
        for queue in queues:
            self.channel.queue_declare(queue=queue, durable=False, auto_delete=True)

        # Configurar consumidores
        self.channel.basic_consume(queue=CLIENT_REGISTRATION_QUEUE,
                                   on_message_callback=self.on_client_registration,
                                   auto_ack=True)
        self.channel.basic_consume(queue=ORDER_QUEUE,
                                   on_message_callback=self.on_order_received,
                                   auto_ack=True)
        self.channel.basic_consume(queue=CLIENT_STATUS_QUEUE,
                                   on_message_callback=self.on_status_request,
                                   auto_ack=True)
        self.channel.basic_consume(queue=CLIENT_CANCEL_QUEUE,
                                   on_message_callback=self.on_cancel_request,
                                   auto_ack=True)
        self.channel.basic_consume(queue=ROBOT_STATUS_QUEUE,
                               on_message_callback=self.on_robot_status_update,
                               auto_ack=True)
        self.channel.basic_consume(queue=DELIVERY_STATUS_QUEUE,
                               on_message_callback=self.on_delivery_status_update,
                               auto_ack=True)

    def on_client_registration(self, ch, method, properties, body):
        """Manejador para el registro de nuevos clientes."""
        data = json.loads(body)
        client_id = data['client_id']
        self.clients[client_id] = data
        print(f"Cliente registrado: {client_id}")

    def on_order_received(self, ch, method, properties, body):
        """Manejador para pedidos recibidos."""
        order_data = json.loads(body)
        self.orders[order_data['order_id']] = order_data
        print(f"Pedido recibido: {order_data}")
        # Lógica para procesar el pedido, como asignarlo a un robot

    def on_status_request(self, ch, method, properties, body):
        """Manejador para solicitudes de estado de pedidos."""
        request = json.loads(body)
        order_id = request['order_id']
        if order_id in self.orders:
            status = self.orders[order_id].get('status', 'Desconocido')
            print(f"Estado del pedido {order_id}: {status}")
        else:
            print(f"Pedido {order_id} no encontrado.")

    def on_cancel_request(self, ch, method, properties, body):
        """Manejador para solicitudes de cancelación de pedidos."""
        request = json.loads(body)
        order_id = request['order_id']
        if order_id in self.orders and self.orders[order_id].get('status') != 'Entregado':
            self.orders[order_id]['status'] = 'Cancelado'
            print(f"Pedido {order_id} cancelado.")
        else:
            print(f"No se puede cancelar el pedido {order_id}.")
            
    def on_robot_status_update(self, ch, method, properties, body):
        """Manejador para actualizaciones de estado de los robots."""
        update = json.loads(body)
        order_id = update['order_id']
        status = update['status']

        # Actualiza el estado del pedido basado en la actualización del robot
        if order_id in self.orders:
            self.orders[order_id]['status'] = 'Recogido' if status == 'completed' else 'Fallo en recogida'
            print(f"Actualización del estado del pedido {order_id} a {self.orders[order_id]['status']}")
        else:
            print(f"Actualización recibida para pedido desconocido {order_id}.")
    
    def on_delivery_status_update(self, ch, method, properties, body):
        """Manejador para actualizaciones de estado de las entregas."""
        update = json.loads(body)
        order_id = update['order_id']
        status = update['status']

        # Actualiza el estado del pedido basado en la actualización de entrega
        if order_id in self.orders:
            new_status = 'Entregado' if status == 'Delivered' else 'Fallo en entrega'
            self.orders[order_id]['status'] = new_status
            print(f"Actualización del estado del pedido {order_id} a {new_status}")
        else:
            print(f"Actualización recibida para pedido desconocido {order_id}.")
        
    def start(self):
        """Inicia el procesamiento de mensajes."""
        print("Controlador iniciado. Esperando mensajes...")
        self.channel.start_consuming()

if __name__ == '__main__':
    controller = Controller()
    controller.start()
