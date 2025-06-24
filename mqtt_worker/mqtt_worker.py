import os
import json
import ssl
import paho.mqtt.client as mqtt
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

MQTT_BROKER = os.getenv("MQTT_BROKER")
MQTT_PORT = int(os.getenv("MQTT_PORT", 8883))
MQTT_USERNAME = os.getenv("MQTT_USERNAME")
MQTT_PASSWORD = os.getenv("MQTT_PASSWORD")
MQTT_TOPIC = os.getenv("MQTT_TOPIC")

COSMOS_URI = os.getenv("COSMOS_URI")
mongo_client = MongoClient(COSMOS_URI)
collection = mongo_client["iot"]["data"]

def on_connect(client, userdata, flags, rc):
    print("✅ Connected to HiveMQ")
    client.subscribe(MQTT_TOPIC)

def on_message(client, userdata, msg):
    try:
        payload = json.loads(msg.payload.decode())
        print(f"[{msg.topic}] {payload}")
        collection.insert_one({"topic": msg.topic, "payload": payload})
    except Exception as e:
        print("Error:", e)

client = mqtt.Client()
client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
client.tls_set(cert_reqs=ssl.CERT_REQUIRED)
client.on_connect = on_connect
client.on_message = on_message
client.connect(MQTT_BROKER, MQTT_PORT, 60)
client.loop_forever()