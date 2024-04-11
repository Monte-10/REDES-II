from django.core.management.base import BaseCommand
from iot.services.mqtt_controller import MQTTController

class Command(BaseCommand):
    help = 'Starts the MQTT client'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting MQTT client...'))
        controller = MQTTController()
        controller.start()
