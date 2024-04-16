# launch_controller.py
import pika
import json
from utils.config import (RABBITMQ_HOST, RABBITMQ_PORT, RABBITMQ_USERNAME,
                          RABBITMQ_PASSWORD, ORDER_QUEUE, ROBOT_WORK_QUEUE,
                          DELIVERY_QUEUE, CLIENT_REGISTRATION_QUEUE,
                          CLIENT_STATUS_QUEUE, CLIENT_CANCEL_QUEUE, ROBOT_STATUS_QUEUE, DELIVERY_STATUS_QUEUE, CANCEL_NOTIFICATION_QUEUE)
"""
    Clase que representa el controlador del sistema.
    
    Attributes:
        connection: Conexión con RabbitMQ.
        channel: Canal de comunicación con RabbitMQ.
        clients: Registro de clientes.
        orders: Registro de pedidos.
"""

class Controller:
    """
        Se encarga de inicializar el controlador del sistema.
    """
    def __init__(self):
        self.connection = self.create_connection()
        self.channel = self.connection.channel()
        self.setup_queues()
        self.clients = {}  # Registro de clientes
        self.orders = {}  # Registro de pedidos

    """
        Se encarga de crear una conexión a RabbitMQ.
        
        Returns:
            Una conexión a RabbitMQ.
    """
    def create_connection(self):
        """Establece la conexión con RabbitMQ."""
        credentials = pika.PlainCredentials(RABBITMQ_USERNAME, RABBITMQ_PASSWORD)
        return pika.BlockingConnection(
            pika.ConnectionParameters(host=RABBITMQ_HOST, port=RABBITMQ_PORT, credentials=credentials)
        )

    """
        Se encarga de configurar las colas necesarias en RabbitMQ.
        
        Returns:
            None
    """
    def setup_queues(self):
        """Declara las colas necesarias en RabbitMQ."""
        queues = [ORDER_QUEUE, ROBOT_WORK_QUEUE, DELIVERY_QUEUE,
                CLIENT_REGISTRATION_QUEUE, CLIENT_STATUS_QUEUE, CLIENT_CANCEL_QUEUE, ROBOT_STATUS_QUEUE, DELIVERY_STATUS_QUEUE, CANCEL_NOTIFICATION_QUEUE]
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
        self.channel.basic_consume(queue=CANCEL_NOTIFICATION_QUEUE,
                                 on_message_callback=self.on_cancel_notification,
                                    auto_ack=True)
    
    """
        Se encarga de manejar el registro de nuevos clientes.
        
        Args:
            ch: Canal de comunicación con RabbitMQ.
            method: Método de comunicación con RabbitMQ.
            properties: Propiedades del mensaje.
            body: Cuerpo del mensaje.
            
        Returns:
            None
    """
    def on_client_registration(self, ch, method, properties, body):
        """Manejador para el registro de nuevos clientes."""
        data = json.loads(body)
        client_id = data['client_id']
        self.clients[client_id] = data
        print(f"Cliente registrado: {client_id}")

    """
        Se encarga de manejar los pedidos recibidos.
        
        Args:
            ch: Canal de comunicación con RabbitMQ.
            method: Método de comunicación con RabbitMQ.
            properties: Propiedades del mensaje.
            body: Cuerpo del mensaje.
            
        Returns:
            None
    """
    def on_order_received(self, ch, method, properties, body):
        """Manejador para pedidos recibidos."""
        order_data = json.loads(body)
        order_data['status'] = 'Pendiente'
        self.orders[order_data['order_id']] = order_data
        print(f"Pedido recibido: {order_data}")
        # Asignar tarea al robot para procesar el pedido solo una vez
        self.assign_task_to_robot(order_data['order_id'])

    """
        Se encarga de manejar las solicitudes de estado de pedidos.
        
        Args:
            ch: Canal de comunicación con RabbitMQ.
            method: Método de comunicación con RabbitMQ.
            properties: Propiedades del mensaje.
            body: Cuerpo del mensaje.
            
        Returns:
            None
    """
    def on_status_request(self, ch, method, properties, body):
        """Manejador para solicitudes de estado de pedidos."""
        request = json.loads(body)
        order_id = request['order_id']
        if order_id in self.orders:
            status = self.orders[order_id].get('status', 'Desconocido')
            print(f"Estado del pedido {order_id}: {status}")
        else:
            print(f"Pedido {order_id} no encontrado.")

    """
        Se encarga de manejar las solicitudes de cancelación de pedidos.
        
        Args:
            ch: Canal de comunicación con RabbitMQ.
            method: Método de comunicación con RabbitMQ.
            properties: Propiedades del mensaje.
            body: Cuerpo del mensaje.
            
        Returns:
            None
    """
    def on_cancel_request(self, ch, method, properties, body):
        request = json.loads(body)
        order_id = request['order_id']
        if order_id in self.orders and self.orders[order_id].get('status') not in ['Entregado', 'Cancelado']:
            self.orders[order_id]['status'] = 'Cancelado'
            print(f"Pedido {order_id} cancelado.")
            # Aquí es donde publicamos la notificación de cancelación
            cancel_message = json.dumps({'order_id': order_id})
            self.channel.basic_publish(exchange='',
                                    routing_key=CANCEL_NOTIFICATION_QUEUE,
                                    body=cancel_message)
            print(f"Notificación de cancelación enviada para el pedido: {order_id}")
        else:
            print(f"No se puede cancelar el pedido {order_id}.")
    
    """
        Se encarga de manejar las notificaciones de cancelación de pedidos.
        
        Args:
            ch: Canal de comunicación con RabbitMQ.
            method: Método de comunicación con RabbitMQ.
            properties: Propiedades del mensaje.
            body: Cuerpo del mensaje.
            
        Returns:
            None
    """
    def on_cancel_notification(self, ch, method, properties, body):
        notification = json.loads(body)
        order_id = notification['order_id']
        
        # Marcar el pedido como cancelado si existe y aún no ha sido entregado
        if order_id in self.orders:
            # Solo actuar si el pedido no ha sido ya marcado como entregado o cancelado
            if self.orders[order_id]['status'] not in ['Entregado', 'Cancelado']:
                self.orders[order_id]['status'] = 'Cancelado'
                print(f"Pedido {order_id} marcado como cancelado.")
            else:
                print(f"Pedido {order_id} ya estaba marcado como {self.orders[order_id]['status']}.")
        else:
            print(f"Notificación de cancelación recibida para pedido desconocido: {order_id}.")

    """
        Se encarga de manejar las actualizaciones de estado de los robots.
        
        Args:
            ch: Canal de comunicación con RabbitMQ.
            method: Método de comunicación con RabbitMQ.
            properties: Propiedades del mensaje.
            body: Cuerpo del mensaje.
            
        Returns:
            None
    """
    def on_robot_status_update(self, ch, method, properties, body):
        update = json.loads(body)
        order_id = update['order_id']
        status = update['status']

        if order_id in self.orders:
            if status == 'completed':
                self.orders[order_id]['status'] = 'Recogido'
                print(f"Actualización del estado del pedido {order_id} a Recogido")
                # Publicar tarea de entrega
                self.assign_task_to_delivery(order_id)
            else:
                self.orders[order_id]['status'] = 'Fallo en recogida'
                print(f"Actualización del estado del pedido {order_id} a Fallo en recogida")
        else:
            print(f"Actualización recibida para pedido desconocido {order_id}.")
    
    """
        Se encarga de manejar las actualizaciones de estado de las entregas.
        
        Args:
            ch: Canal de comunicación con RabbitMQ.
            method: Método de comunicación con RabbitMQ.
            properties: Propiedades del mensaje.
            body: Cuerpo del mensaje.
            
        Returns:
            None
    """
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
        
    """
        Se encarga de asignar una tarea al robot.
        
        Args:
            order_id: Identificador del pedido.
            
        Returns:
            None
    """
    def assign_task_to_robot(self, order_id):
        """Asigna una tarea al robot, solo si el pedido no ha sido cancelado."""
        if self.orders[order_id].get('status') == 'Cancelado':
            print(f"Pedido {order_id} ha sido cancelado, no se asignará tarea al robot.")
            return
        task = {'order_id': order_id}
        self.channel.basic_publish(exchange='',
                                   routing_key=ROBOT_WORK_QUEUE,
                                   body=json.dumps(task))
        print(f"Tarea asignada al robot para el pedido: {order_id}")
    
    """
        Se encarga de asignar una tarea de entrega al repartidor.
        
        Args:
            order_id: Identificador del pedido.
            
        Returns:
            None
    """
    def assign_task_to_delivery(self, order_id):
        """Asigna una tarea de entrega al repartidor, solo si el pedido no ha sido cancelado y ha sido recogido."""
        if self.orders[order_id]['status'] in ['Cancelado', 'Fallo en recogida']:
            print(f"Pedido {order_id} ha sido cancelado o falló en recogida, no se asignará tarea de entrega.")
            return
        task = {'order_id': order_id}
        self.channel.basic_publish(exchange='',
                                   routing_key=DELIVERY_QUEUE,
                                   body=json.dumps(task))
        print(f"Tarea de entrega asignada al repartidor para el pedido: {order_id}")
    
    """
        Se encarga de iniciar el procesamiento de mensajes.
        
        Returns:
            None
    """
    def start(self):
        """Inicia el procesamiento de mensajes."""
        print("Controlador iniciado. Esperando mensajes...")
        self.channel.start_consuming()

if __name__ == '__main__':
    controller = Controller()
    controller.start()
