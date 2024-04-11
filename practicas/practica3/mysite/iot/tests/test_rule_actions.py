from django.test import TestCase
from unittest.mock import patch, MagicMock
from iot.models import Device, Rule
from iot.services.mqtt_controller import MQTTController
from iot.services.rule_engine import RuleEngine

class TestRuleActions(TestCase):
    def setUp(self):
        # Configura los objetos necesarios para el test
        self.device = Device.objects.create(id=1, device_type='sensor', state='off')
        self.rule = Rule.objects.create(
            description="Encender cuando la temperatura es alta",
            subject="temperature",
            operator=">",
            value="25",
            action="turn_on"
        )

    @patch('iot.services.rule_engine.RuleEngine.perform_action')
    @patch('iot.services.rule_engine.RuleEngine.evaluate')
    def test_action_triggered_by_rule(self, mock_evaluate, mock_perform_action):
        # Configurar el mock para simular que la regla se cumple
        mock_evaluate.side_effect = lambda: RuleEngine.perform_action(self.device.id, 'turn_on')

        # Crear un controlador MQTT y simular la recepción de un mensaje que cumple la regla
        controller = MQTTController()
        controller.on_message(None, None, self.mock_mqtt_message('iot/devices/1/temperature', '26'))

        # Asegurarse de que la acción se llama correctamente
        mock_perform_action.assert_called_once_with(self.device.id, 'turn_on')

    def mock_mqtt_message(self, topic, payload):
        class MQTTMessage:
            def __init__(self, topic, payload):
                self.topic = topic
                self.payload = payload.encode()
        return MQTTMessage(topic, payload)
