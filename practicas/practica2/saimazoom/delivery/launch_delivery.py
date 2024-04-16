import pika
import json
import argparse
import time
import random
from utils.config import (RABBITMQ_HOST, RABBITMQ_PORT, RABBITMQ_USERNAME,
                          RABBITMQ_PASSWORD, DELIVERY_QUEUE, DELIVERY_STATUS_QUEUE, CANCEL_NOTIFICATION_QUEUE)

"""
    Se encarga de simular el comportamiento de un repartidor.
    
    Returns:
        None
"""
class DeliveryPerson:
    """
        Inicializa un nuevo repartidor con una tasa de éxito específica.
        
        Args:
            success_rate: Tasa de éxito de las entregas (entre 0 y 1).
    """
    def __init__(self, success_rate=0.8):
        self.success_rate = success_rate
        self.connection = self.create_connection()
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=DELIVERY_QUEUE, durable=False, auto_delete=True)
        self.channel.basic_consume(queue=DELIVERY_QUEUE, on_message_callback=self.on_delivery_task_received, auto_ack=True)
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
    def on_delivery_task_received(self, ch, method, properties, body):
        task = json.loads(body)
        order_id = task['order_id']
        if order_id in self.cancelled_orders:
            print(f"El pedido {order_id} ha sido cancelado. Abortando entrega.")
            return  # Sale tempranamente si el pedido está cancelado
        print(f"Repartidor recibió tarea de entrega: {task}")
        success_rate = 0.8
        attempts = 0
        delivered = False

        while attempts < 3 and not delivered:
            time_to_deliver = random.randint(10, 20)
            time.sleep(time_to_deliver)
            attempts += 1

            if random.random() < self.success_rate:
                print(f"Entrega realizada exitosamente para el pedido: {task}")
                delivered = True
                # Notificar al controlador sobre la entrega exitosa
                self.notify_controller(task['order_id'], 'Delivered')
            else:
                print(f"Intento de entrega {attempts} fallido para el pedido: {task}")

        if not delivered:
            print(f"No se pudo entregar el pedido después de {attempts} intentos: {task}")
            # Notificar al controlador el fallo final
            self.notify_controller(task['order_id'], 'Failed')

    """
        Se encarga de enviar una notificación al controlador con el estado de la entrega.
        
        Args:
            order_id: Identificador del pedido.
            status: Estado de la entrega.
            
        Returns:
            None
    """
    def notify_controller(self, order_id, status):
        """Envía una notificación al controlador con el estado de la entrega."""
        message = json.dumps({'order_id': order_id, 'status': status})
        self.channel.basic_publish(exchange='',
                                   routing_key=DELIVERY_STATUS_QUEUE,
                                   body=message)
        
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
        Inicia el repartidor y espera tareas de entrega.
        
        Returns:
            None
    """
    def start(self):
        print("Repartidor iniciado y esperando tareas de entrega...")
        self.channel.start_consuming()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Inicia el proceso del repartidor con una tasa de éxito específica.')
    parser.add_argument('--success-rate', type=float, default=0.8, help='Tasa de éxito de las entregas (entre 0 y 1)')
    args = parser.parse_args()

    delivery_person = DeliveryPerson(success_rate=args.success_rate)
    delivery_person.start()