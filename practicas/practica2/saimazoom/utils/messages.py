"""
Este módulo contiene funciones para crear y parsear mensajes.
"""

"""
Crea un mensaje de registro para un cliente.

Args:
    client_id: Identificador del cliente.
    
Returns:
    str: Mensaje de registro.
"""
def create_register_message(client_id):
    return f"REGISTER {client_id}"

"""
Crea un mensaje de pedido para un cliente.

Args:
    client_id: Identificador del cliente.
    order_id: Identificador del pedido.
    product_ids: Lista de identificadores de productos.
    
Returns:
    str: Mensaje de pedido.
"""
def create_order_message(client_id, order_id, product_ids):
    product_ids_str = ','.join(map(str, product_ids))
    return f"ORDER {client_id} {order_id} {product_ids_str}"

"""
Crea un mensaje de consulta de estado para un cliente.

Args:
    client_id: Identificador del cliente.
    order_id: Identificador del pedido.
    
Returns:
    str: Mensaje de consulta de estado.
"""
def create_move_message(order_id):
    return f"MOVE {order_id}"

"""
Crea un mensaje de entrega para un pedido.

Args:
    order_id: Identificador del pedido.
    
Returns:
    str: Mensaje de entrega.
"""
def create_delivery_message(order_id):
    return f"DELIVER {order_id}"

"""
Crea un mensaje de cancelación para un pedido.

Args:
    order_id: Identificador del pedido.
    
Returns:
    str: Mensaje de cancelación.
"""
def parse_message(message):
    """Descompone el mensaje en sus componentes y los devuelve."""
    components = message.split()
    # Ejemplo: 'REGISTER 123' -> ('REGISTER', ['123'])
    message_type = components[0]
    message_data = components[1:]
    return message_type, message_data
