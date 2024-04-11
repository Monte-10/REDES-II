import paho.mqtt.client as mqtt
import time
import argparse

def main(host, port, device_id, min_value, max_value, increment, interval):
    client = mqtt.Client()
    client.connect(host, port, 60)
    client.loop_start()

    current_value = min_value
    direction = increment

    try:
        while True:
            client.publish(f"iot/devices/{device_id}/state", str(current_value))
            print(f"Published {current_value} to iot/devices/{device_id}/state")
            current_value += direction
            if current_value > max_value or current_value < min_value:
                direction *= -1  # Change direction
            time.sleep(interval)
    except KeyboardInterrupt:
        print("Disconnecting...")
        client.disconnect()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Dummy Sensor Simulator')
    parser.add_argument('--host', default='redes2.ii.uam.es', help='MQTT broker host')
    parser.add_argument('-p', '--port', default=1883, type=int, help='MQTT broker port')
    parser.add_argument('-i', '--interval', default=1, type=int, help='Interval in seconds between messages')
    parser.add_argument('-m', '--min', default=20, type=int, help='Minimum sensor value')
    parser.add_argument('-M', '--max', default=30, type=int, help='Maximum sensor value')
    parser.add_argument('--increment', default=1, type=int, help='Value increment between messages')
    parser.add_argument('id', help='Device ID')
    
    args = parser.parse_args()

    main(args.host, args.port, args.id, args.min, args.max, args.increment, args.interval)
