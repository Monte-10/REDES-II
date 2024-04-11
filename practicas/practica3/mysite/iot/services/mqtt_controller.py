# iot/services/mqtt_controller.py
import paho.mqtt.client as mqtt
from django.conf import settings
from iot.models import Device
from iot.services.rule_engine import RuleEngine

class MQTTController:
    def __init__(self):
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code " + str(rc))
        client.subscribe("iot/devices/#")

    def on_message(self, client, userdata, msg):
        print(f"Message received on {msg.topic} with payload {msg.payload}")
        topic_parts = msg.topic.split('/')
        if len(topic_parts) > 2:
            device_id = topic_parts[2]
            state = msg.payload.decode('utf-8')
            try:
                device = Device.objects.get(id=device_id)
                device.state = state
                device.save()
                print(f"Device {device_id} updated to {state}")
                RuleEngine.evaluate()  # Evaluate rules upon message reception
            except Device.DoesNotExist:
                print(f"Device {device_id} not found")
            except ValueError:
                print(f"Invalid device ID {device_id}")
        else:
            print("Invalid topic format")

    def start(self):
        self.client.connect(settings.MQTT_HOST, settings.MQTT_PORT, 60)
        self.client.loop_forever()
