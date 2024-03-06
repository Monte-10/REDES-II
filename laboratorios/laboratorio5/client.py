#!/usr/bin/env python
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(host='redes2.ii.uam.es'))
channel = connection.channel()

channel.queue_declare(queue='2311-04hello')

channel.basic_publish(exchange='', routing_key='2311-04hello', body='Hello World!')
print(" [x] Sent 'Hello World!'")
connection.close()
