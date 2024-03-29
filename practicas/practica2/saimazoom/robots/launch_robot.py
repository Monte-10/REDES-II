import pika
import json
import time
import random
from utils.config import (RABBITMQ_HOST, RABBITMQ_PORT, RABBITMQ_USERNAME,
                          RABBITMQ_PASSWORD, ROBOT_WORK_QUEUE, ROBOT_STATUS_QUEUE)

class Robot:
    def __init__(self):
        self.connection = self.create_connection()
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=ROBOT_WORK_QUEUE, durable=False, auto_delete=True)
        self.channel.queue_declare(queue=ROBOT_STATUS_QUEUE, durable=False, auto_delete=True)  # Asegurar que la cola de estado exista
        self.channel.basic_consume(queue=ROBOT_WORK_QUEUE, on_message_callback=self.on_task_received, auto_ack=True)

    def create_connection(self):
        credentials = pika.PlainCredentials(RABBITMQ_USERNAME, RABBITMQ_PASSWORD)
        return pika.BlockingConnection(
            pika.ConnectionParameters(host=RABBITMQ_HOST, port=RABBITMQ_PORT, credentials=credentials)
        )

    def on_task_received(self, ch, method, properties, body):
        task = json.loads(body)
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

    def start(self):
        print("Robot iniciado y esperando tareas...")
        self.channel.start_consuming()

if __name__ == '__main__':
    robot = Robot()
    robot.start()
