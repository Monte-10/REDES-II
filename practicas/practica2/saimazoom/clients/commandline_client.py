import argparse
import pika
import json
from utils.config import (RABBITMQ_HOST, RABBITMQ_PORT, RABBITMQ_USERNAME,
                          RABBITMQ_PASSWORD, CLIENT_REGISTRATION_QUEUE, ORDER_QUEUE,
                          CLIENT_STATUS_QUEUE, CLIENT_CANCEL_QUEUE)

"""
    Cliente de línea de comandos para interactuar con el sistema de pedidos de Saimazoom.
    
    El cliente permite realizar las siguientes acciones:
    - Registrar un nuevo cliente
    - Realizar un nuevo pedido
    - Consultar el estado de un pedido
    - Cancelar un pedido
    
    Ejemplos de uso:
    - Registrar un nuevo cliente:
        python commandline_client.py --register CLIENT_ID
    - Realizar un nuevo pedido:
        python commandline_client.py --order CLIENT_ID ORDER_ID PRODUCT_IDS
    - Consultar el estado de un pedido:
        python commandline_client.py --status CLIENT_ID ORDER_ID
    - Cancelar un pedido:
        python commandline_client.py --cancel CLIENT_ID ORDER_ID
        
    Los argumentos CLIENT_ID, ORDER_ID y PRODUCT_IDS son cadenas de texto.
    PRODUCT_IDS es una lista de identificadores de productos separados por comas.
    
    El cliente se conecta a RabbitMQ y envía mensajes a las colas correspondientes.
"""
class CommandLineClient:

    """
        Se encarga de inicializar el cliente de línea de comandos.
    """
    def __init__(self):
        self.connection = self.create_connection()
        self.channel = self.connection.channel()

    """
        Se encarga de crear una conexión a RabbitMQ.
        
        Returns:
            Una conexión a RabbitMQ.    
    """
    def create_connection(self):
        credentials = pika.PlainCredentials(RABBITMQ_USERNAME, RABBITMQ_PASSWORD)
        return pika.BlockingConnection(
            pika.ConnectionParameters(host=RABBITMQ_HOST, port=RABBITMQ_PORT, credentials=credentials)
        )

    """
        Se encarga de registrar un nuevo cliente.
        
        Args:
            client_id: Identificador del cliente.
            
        Returns:
            None
    """
    def register_client(self, client_id):
        message = json.dumps({"client_id": client_id})
        self.channel.basic_publish(exchange='',
                                   routing_key=CLIENT_REGISTRATION_QUEUE,
                                   body=message)
        print(f"Cliente {client_id} registrado.")

    """
        Se encarga de realizar un nuevo pedido.
        
        Args:
            client_id: Identificador del cliente.
            order_id: Identificador del pedido.
            product_ids: Lista de identificadores de productos.
            
        Returns:
            None
    """
    def make_order(self, client_id, order_id, product_ids):
        message = json.dumps({"client_id": client_id, "order_id": order_id, "product_ids": product_ids})
        self.channel.basic_publish(exchange='',
                                   routing_key=ORDER_QUEUE,
                                   body=message)
        print(f"Pedido {order_id} realizado.")

    """
        Se encarga de consultar el estado de un pedido.
        
        Args:
            client_id: Identificador del cliente.
            order_id: Identificador del pedido.
            
        Returns:
            None
    """
    def check_order_status(self, client_id, order_id):
        """Consulta el estado de un pedido."""
        message = json.dumps({"client_id": client_id, "order_id": order_id})
        self.channel.basic_publish(exchange='',
                                   routing_key=CLIENT_STATUS_QUEUE,
                                   body=message)
        print(f"Consultando estado del pedido {order_id}.")

    """
        Se encarga de cancelar un pedido.
        
        Args:
            client_id: Identificador del cliente.
            order_id: Identificador del pedido.
            
        Returns:
            None
    """
    def cancel_order(self, client_id, order_id):
        """Cancela un pedido."""
        message = json.dumps({"client_id": client_id, "order_id": order_id})
        self.channel.basic_publish(exchange='',
                                   routing_key=CLIENT_CANCEL_QUEUE,
                                   body=message)
        print(f"Cancelando pedido {order_id}.")

    """
        Se encarga de ejecutar el cliente de línea de comandos.
        
        Returns:
            None
    """
    def run(self):
        parser = argparse.ArgumentParser(description="Cliente de línea de comandos para Saimazoom")
        parser.add_argument("--register", help="Registra un nuevo cliente", metavar="CLIENT_ID")
        parser.add_argument("--order", help="Realiza un nuevo pedido", nargs=3, metavar=("CLIENT_ID", "ORDER_ID", "PRODUCT_IDS"))
        parser.add_argument("--status", help="Consulta el estado de un pedido", nargs=2, metavar=("CLIENT_ID", "ORDER_ID"))
        parser.add_argument("--cancel", help="Cancela un pedido", nargs=2, metavar=("CLIENT_ID", "ORDER_ID"))
        args = parser.parse_args()

        if args.register:
            self.register_client(args.register)
        elif args.order:
            client_id, order_id, product_ids = args.order
            product_ids = [int(pid) for pid in product_ids.split(',')]
            self.make_order(client_id, order_id, product_ids)
        elif args.status:
            client_id, order_id = args.status
            self.check_order_status(client_id, order_id)
        elif args.cancel:
            client_id, order_id = args.cancel
            self.cancel_order(client_id, order_id)

if __name__ == "__main__":
    client = CommandLineClient()
    client.run()
