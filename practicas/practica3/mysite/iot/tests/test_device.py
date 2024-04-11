from django.test import TestCase
from unittest.mock import patch, MagicMock
from iot.models import Device
from iot.services.mqtt_controller import MQTTController
from django.conf import settings

class DeviceTests(TestCase):
    @patch('paho.mqtt.client.Client')
    def test_mqtt_connection(self, mock_mqtt):
        """ Test that the device connects correctly to the MQTT broker. """
        mock_client = mock_mqtt.return_value
        controller = MQTTController(client=mock_client)
        controller.start()
        mock_client.connect.assert_called_with(settings.MQTT_HOST, settings.MQTT_PORT, 60)

    @patch('paho.mqtt.client.Client')
    def test_switch_state_change(self, mock_mqtt):
        """ Test that a switch changes its state upon receiving a command. """
        # Setup
        device = Device.objects.create(id='123', device_type='switch', state='off')
        
        # Simulate incoming MQTT message
        mock_client = mock_mqtt.return_value
        mock_client.on_message = MQTTController().on_message
        mock_client.on_message(mock_client, None, self.mock_mqtt_message('iot/devices/123', 'on'))
        
        # Test state change
        device.refresh_from_db()
        self.assertEqual(device.state, 'on')

    @patch('paho.mqtt.client.Client')
    def test_sensor_state_change(self, mock_mqtt):
        """ Test that a sensor updates its state based on interval readings. """
        # Setup
        device = Device.objects.create(id='124', device_type='sensor', state='25')

        # Simulate incoming MQTT message
        mock_client = mock_mqtt.return_value
        mock_client.on_message = MQTTController().on_message
        mock_client.on_message(mock_client, None, self.mock_mqtt_message('iot/devices/124', '26'))
        
        # Test state change
        device.refresh_from_db()
        self.assertEqual(device.state, '26')

    def mock_mqtt_message(self, topic, payload):
        """Utility function to create a MQTT message object with given topic and payload."""
        class MQTTMessage:
            def __init__(self, topic, payload):
                self.topic = topic
                self.payload = payload.encode()

        return MQTTMessage(topic, payload)

