from commandline_client import CommandLineClient
import time

"""
    Se encarga de simular el comportamiento de un cliente de línea de comandos.
    
    Returns:
        None
"""
def main():
    client = CommandLineClient()

    # Simular acciones del cliente
    client_id = "cliente_demo"
    order_id = "pedido_demo"
    product_ids = "1,2,3"

    print(f"Registrando al cliente '{client_id}'...")
    client.register_client(client_id)
    time.sleep(1)  # Esperar para asegurar que el registro se complete

    print(f"Realizando un pedido '{order_id}' con productos {product_ids}...")
    client.make_order(client_id, order_id, product_ids)
    time.sleep(1)  # Esperar para asegurar que el pedido se procese

    print(f"Consultando el estado del pedido '{order_id}'...")
    client.check_order_status(client_id, order_id)
    time.sleep(1)  # Esperar para simular tiempo de procesamiento y respuesta

    print(f"Cancelando el pedido '{order_id}'...")
    client.cancel_order(client_id, order_id)
    time.sleep(1)  # Esperar para asegurar que la cancelación se procese

if __name__ == "__main__":
    main()
