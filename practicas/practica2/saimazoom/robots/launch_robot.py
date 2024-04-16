import pika
import json
import time
import random
from utils.config import (RABBITMQ_HOST, RABBITMQ_PORT, RABBITMQ_USERNAME,
                          RABBITMQ_PASSWORD, ROBOT_WORK_QUEUE, ROBOT_STATUS_QUEUE, CANCEL_NOTIFICATION_QUEUE)

"""
    Se encarga de simular el comportamiento de un robot.
    
    Returns:
        None
"""
class Robot:
    """
        Inicializa un nuevo robot.
    """
    def __init__(self):
        self.connection = self.create_connection()
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=ROBOT_WORK_QUEUE, durable=False, auto_delete=True)
        self.channel.queue_declare(queue=ROBOT_STATUS_QUEUE, durable=False, auto_delete=True)  # Asegurar que la cola de estado exista
        self.channel.basic_consume(queue=ROBOT_WORK_QUEUE, on_message_callback=self.on_task_received, auto_ack=True)
        self.channel.queue_declare(queue=CANCEL_NOTIFICATION_QUEUE, durable=False, auto_delete=True)
        self.channel.basic_consume(queue=CANCEL_NOTIFICATION_QUEUE,
                                on_message_callback=self.on_cancel_notification_received,
                                auto_ack=True)
        self.cancelled_orders = set()

    """
        Se encarga de crear una conexión a RabbitMQ.
        
        Returns:
            Una conexión a RabbitMQ.
    """
    def create_connection(self):
        credentials = pika.PlainCredentials(RABBITMQ_USERNAME, RABBITMQ_PASSWORD)
        return pika.BlockingConnection(
            pika.ConnectionParameters(host=RABBITMQ_HOST, port=RABBITMQ_PORT, credentials=credentials)
        )

    """
        Se encarga de procesar una tarea de entrega.
        
        Args:
            ch: Canal de comunicación.
            method: Método de entrega.
            properties: Propiedades del mensaje.
            body: Cuerpo del mensaje.
            
        Returns:
            None
    """
    def on_task_received(self, ch, method, properties, body):
        task = json.loads(body)
        order_id = task['order_id']
        if order_id in self.cancelled_orders:
            print(f"El pedido {order_id} ha sido cancelado. Abortando tarea.")
            return  # Sale tempranamente si el pedido está cancelado
        print(f"Robot recibió tarea: {task}")
        time_to_complete = random.randint(5, 10)
        time.sleep(time_to_complete)

        message = {
            'order_id': task['order_id'],
            'status': 'completed' if random.random() < 0.9 else 'failed'
        }

        print(f"Robot {'completó' if message['status'] == 'completed' else 'no pudo completar'} la tarea: {task}")
        # Enviar actualización de estado al controlador
        self.channel.basic_publish(exchange='',
                                   routing_key=ROBOT_STATUS_QUEUE,
                                   body=json.dumps(message))
    
    """
        Se encarga de procesar una notificación de cancelación.
        
        Args:
            ch: Canal de comunicación.
            method: Método de entrega.
            properties: Propiedades del mensaje.
            body: Cuerpo del mensaje.
            
        Returns:
            None
    """
    def on_cancel_notification_received(self, ch, method, properties, body):
        notification = json.loads(body)
        order_id = notification['order_id']
        self.cancelled_orders.add(order_id)  # Añade el pedido cancelado al conjunto
        print(f"Recibida notificación de cancelación para el pedido: {order_id}")

    """
        Inicia el robot y espera tareas.
        
        Returns:
            None
    """
    def start(self):
        print("Robot iniciado y esperando tareas...")
        self.channel.start_consuming()

if __name__ == '__main__':
    robot = Robot()
    robot.start()
