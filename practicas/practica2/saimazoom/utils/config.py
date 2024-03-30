# utils/config.py

# Configuración de RabbitMQ
RABBITMQ_HOST = 'localhost'  # Cambiar a 'redes2.ii.uam.es' para producción
RABBITMQ_PORT = 5672
RABBITMQ_USERNAME = 'guest'  # Ajustar según sea necesario
RABBITMQ_PASSWORD = 'guest'  # Ajustar según sea necesario

# Prefijos de nombres de colas para evitar conflictos
QUEUE_PREFIX = '2311-04_'

# Colas específicas
ORDER_QUEUE = f'{QUEUE_PREFIX}orders'
ROBOT_WORK_QUEUE = f'{QUEUE_PREFIX}robot_work'
DELIVERY_QUEUE = f'{QUEUE_PREFIX}delivery'
CLIENT_REGISTRATION_QUEUE = f'{QUEUE_PREFIX}client_registration'
CLIENT_STATUS_QUEUE = f'{QUEUE_PREFIX}client_status'
CLIENT_CANCEL_QUEUE = f'{QUEUE_PREFIX}client_cancel'
ROBOT_STATUS_QUEUE = f'{QUEUE_PREFIX}robot_status'
DELIVERY_STATUS_QUEUE = f'{QUEUE_PREFIX}delivery_status'
CANCEL_NOTIFICATION_QUEUE = f'{QUEUE_PREFIX}cancel_notifications'