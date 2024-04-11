from iot.models import Rule, Device
import paho.mqtt.publish as publish

class RuleEngine:
    @staticmethod
    def evaluate():
        """ Evaluar todas las reglas activas y realizar las acciones necesarias. """
        for rule in Rule.objects.all():
            try:
                device = Device.objects.get(id=rule.subject)
                if RuleEngine.check_condition(device.state, rule.operator, rule.value):
                    print(f"Rule {rule.id} triggered.")
                    RuleEngine.perform_action(rule.action)
            except Device.DoesNotExist:
                print(f"Device with ID {rule.subject} not found.")

    @staticmethod
    def check_condition(current_value, operator, condition_value):
        """ Comprueba si la condición de la regla se cumple. """
        if operator == '==':
            return current_value == condition_value
        elif operator == '>':
            return float(current_value) > float(condition_value)
        elif operator == '<':
            return float(current_value) < float(condition_value)
        return False

    @staticmethod
    def perform_action(action):
        """ Realizar la acción especificada en la regla. """
        action_parts = action.split(':')
        if len(action_parts) == 2:
            command, device_id = action_parts
            if command == 'turn_on':
                RuleEngine.send_command(device_id, 'on')
            elif command == 'turn_off':
                RuleEngine.send_command(device_id, 'off')
        else:
            print("Invalid action format.")

    @staticmethod
    def send_command(device_id, state):
        """ Enviar un comando MQTT al dispositivo. """
        topic = f"iot/devices/{device_id}/command"
        message = state
        publish.single(topic, payload=message, hostname='localhost')
        print(f"Sent {message} to {topic}")

# Asegúrate de adaptar las funciones y lógica según las especificaciones de tu proyecto y estructura de datos.
