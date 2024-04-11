# iot/tests/test_controller.py

from django.test import TestCase
from unittest.mock import patch, MagicMock
from iot.models import Device, Rule
from iot.services.mqtt_controller import MQTTController
from iot.services.rule_engine import RuleEngine

class ControllerTests(TestCase):
    def setUp(self):
        self.device = Device.objects.create(id='123', device_type='switch', state='off')
        self.rule = Rule.objects.create(
            description="Turn on if off",
            subject="state",
            operator="==",
            value="'off'",
            action="turn_on: 123"
        )

    @patch('iot.services.rule_engine.RuleEngine.evaluate')
    @patch('paho.mqtt.client.Client')
    def test_controller_receives_mqtt_message_and_evaluates_rule(self, mock_mqtt, mock_evaluate):
        controller = MQTTController()
        mock_client = mock_mqtt.return_value
        controller.client.on_connect(mock_client, None, None, 0)
        controller.client.subscribe.assert_called_with('iot/devices/#')
        controller.on_message(mock_client, None, self.mock_mqtt_message('iot/devices/123', 'on'))
        mock_evaluate.assert_called_once()

    @patch('iot.services.rule_engine.RuleEngine.perform_action')
    def test_rule_action_is_performed(self, mock_perform_action):
        RuleEngine.perform_action('123', 'turn_on')
        mock_perform_action.assert_called_once_with('123', 'turn_on')

    def mock_mqtt_message(self, topic, payload):
        class MQTTMessage:
            def __init__(self, topic, payload):
                self.topic = topic
                self.payload = payload.encode()
        return MQTTMessage(topic, payload)
