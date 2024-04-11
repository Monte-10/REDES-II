import paho.mqtt.client as mqtt
from django.http import HttpResponseRedirect
from .mqtt_client import publish_message
from .app.models import Dispositivo
from django.shortcuts import render, get_object_or_404
TOPIC = "redes2/2311/04/#"

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(TOPIC)

def on_message(client, userdata, msg):
    print(f"{msg.topic} {str(msg.payload)}")
    
def publish_message(topic, message):
    client.publish(topic, message)

def cambiar_estado_dispositivo(request, pk):
    dispositivo = get_object_or_404(Dispositivo, pk=pk)
    nuevo_estado = "ON" if dispositivo.estado == "OFF" else "OFF"
    publish_message(f"dispositivos/{dispositivo.nombre}/set", nuevo_estado)
    dispositivo.estado = nuevo_estado
    dispositivo.save()
    return HttpResponseRedirect('/')

import threading

def start_mqtt_client():
    client.loop_start()

threading.Thread(target=start_mqtt_client).start()

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("mqtt.eclipse.org", 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()