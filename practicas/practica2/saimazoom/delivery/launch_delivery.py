import pika
import json
import time
import random
from utils.config import (RABBITMQ_HOST, RABBITMQ_PORT, RABBITMQ_USERNAME,
                          RABBITMQ_PASSWORD, DELIVERY_QUEUE, DELIVERY_STATUS_QUEUE)

class DeliveryPerson:
    def __init__(self):
        self.connection = self.create_connection()
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=DELIVERY_QUEUE, durable=False, auto_delete=True)
        self.channel.basic_consume(queue=DELIVERY_QUEUE, on_message_callback=self.on_delivery_task_received, auto_ack=True)

    def create_connection(self):
        credentials = pika.PlainCredentials(RABBITMQ_USERNAME, RABBITMQ_PASSWORD)
        return pika.BlockingConnection(
            pika.ConnectionParameters(host=RABBITMQ_HOST, port=RABBITMQ_PORT, credentials=credentials)
        )

    def on_delivery_task_received(self, ch, method, properties, body):
        task = json.loads(body)
        print(f"Repartidor recibió tarea de entrega: {task}")
        success_rate = 0.8
        attempts = 0
        delivered = False

        while attempts < 3 and not delivered:
            time_to_deliver = random.randint(10, 20)
            time.sleep(time_to_deliver)
            attempts += 1

            if random.random() < success_rate:
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

    def notify_controller(self, order_id, status):
        """Envía una notificación al controlador con el estado de la entrega."""
        message = json.dumps({'order_id': order_id, 'status': status})
        self.channel.basic_publish(exchange='',
                                   routing_key=DELIVERY_STATUS_QUEUE,
                                   body=message)

    def start(self):
        print("Repartidor iniciado y esperando tareas de entrega...")
        self.channel.start_consuming()

if __name__ == '__main__':
    delivery_person = DeliveryPerson()
    delivery_person.start()
