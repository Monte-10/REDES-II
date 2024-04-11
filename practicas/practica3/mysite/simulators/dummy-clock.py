import paho.mqtt.client as mqtt
import time
import argparse
from datetime import datetime, timedelta

def main(host, port, device_id, start_time, increment, rate):
    client = mqtt.Client()
    client.connect(host, port, 60)
    client.loop_start()

    current_time = start_time or datetime.now()
    try:
        while True:
            client.publish(f"iot/devices/{device_id}/state", current_time.strftime('%H:%M:%S'))
            print(f"Published {current_time.strftime('%H:%M:%S')} to iot/devices/{device_id}/state")
            current_time += timedelta(seconds=increment)
            time.sleep(rate)
    except KeyboardInterrupt:
        print("Disconnecting...")
        client.disconnect()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Dummy Clock Simulator')
    parser.add_argument('--host', default='redes2.ii.uam.es', help='MQTT broker host')
    parser.add_argument('-p', '--port', default=1883, type=int, help='MQTT broker port')
    parser.add_argument('--time', help='Start time in HH:MM:SS format')
    parser.add_argument('--increment', default=1, type=int, help='Time increment in seconds')
    parser.add_argument('--rate', default=1, type=int, help='Rate of message sending in seconds')
    parser.add_argument('id', help='Device ID')
    
    args = parser.parse_args()
    start_time = datetime.strptime(args.time, '%H:%M:%S') if args.time else None

    main(args.host, args.port, args.id, start_time, args.increment, args.rate)
