import paho.mqtt.client as mqtt
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
django.setup()

from app.models import Dispositivo

# MQTT Settings
MQTT_BROKER_URL = "mqtt.eclipse.org"
MQTT_BROKER_PORT = 1883

# Define on_connect
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("redes2/+/+/+")

# Define on_message
def on_message(client, userdata, msg):
    print(f"Message received: {msg.topic} {str(msg.payload)}")
    # Process message
    # Here you would parse the topic to get the DEVICE_ID and check the payload
    # to decide what action to take. For example:
    topic_parts = msg.topic.split('/')
    if len(topic_parts) == 4:
        grupo, pareja, device_id = topic_parts[1:]
        try:
            dispositivo = Dispositivo.objects.get(pk=device_id)
            # Process message for dispositivo
            # For example, change state, log event, etc.
        except Dispositivo.DoesNotExist:
            print("Dispositivo no registrado")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(MQTT_BROKER_URL, MQTT_BROKER_PORT, 60)

# Blocking call that processes network traffic, dispatches callbacks, and
# handles reconnecting.
client.loop_forever()
