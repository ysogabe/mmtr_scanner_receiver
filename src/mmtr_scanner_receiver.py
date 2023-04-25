import serial
import configparser
import signal
import socket
import json
import os
import sys
import asyncio
from datetime import datetime
from azure.eventhub.aio import EventHubProducerClient
from azure.eventhub import EventData

config = configparser.ConfigParser()
config.read("src/config.ini")

CONNECTION_STR = os.environ.get(
    "AZURE_CONNECTION_STR", config.get("azure_eventhubs", "connection_str")
)
EVENTHUB_NAME = os.environ.get(
    "AZURE_EVENTHUB_NAME", config.get("azure_eventhubs", "eventhub_name")
)

def valid_items(items_to_check):
    for item in items_to_check:
        if item.startswith("00") or len(item) != len("7c:df:a1:a3:b5:34"):
            return False
    return True

async def send_to_eventhubs(beacon_addr, rssi, host_name):
    try:
        producer = EventHubProducerClient.from_connection_string(conn_str=CONNECTION_STR, eventhub_name=EVENTHUB_NAME)

        timestamp = datetime.utcnow().isoformat()

        data = {
            "MAMORIO": beacon_addr,
            "RSSI": int(rssi),
            "Time": timestamp,
            "Hostname": host_name
        }

        event_data = EventData(json.dumps(data))

        async with producer:
            await producer.send_batch([event_data])

    except Exception as e:
        print(f"Error occurred during sending to Event Hubs: {e}")

async def read_serial(port):
    while True:
        try:
            line = port.readline().decode('utf-8').strip()

            if line.startswith("RECV::"):
                line = line.replace("RECV::", "")
                items = line.split(",")

                if len(items) < 3 or not valid_items(items[0:2]):
                    print(f'ignore data: {line}')
                    continue

                await send_to_eventhubs(items[1], items[2], items[0])
        except Exception as e:
            print(f"Error read_serial: {e}")

def signal_handler(sig, frame):
    print("終了処理中...")
    ser.close()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

if __name__ == "__main__":
    ser_port = "/dev/ttyACM0"
    ser = serial.Serial(ser_port, 115200, timeout=1)

    asyncio.run(read_serial(ser))
