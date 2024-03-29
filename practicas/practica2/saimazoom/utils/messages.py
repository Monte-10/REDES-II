# utils/messages.py

def create_register_message(client_id):
    return f"REGISTER {client_id}"

def create_order_message(client_id, order_id, product_ids):
    product_ids_str = ','.join(map(str, product_ids))
    return f"ORDER {client_id} {order_id} {product_ids_str}"

def create_move_message(order_id):
    return f"MOVE {order_id}"

def create_delivery_message(order_id):
    return f"DELIVER {order_id}"

def parse_message(message):
    """Descompone el mensaje en sus componentes y los devuelve."""
    components = message.split()
    # Ejemplo: 'REGISTER 123' -> ('REGISTER', ['123'])
    message_type = components[0]
    message_data = components[1:]
    return message_type, message_data
