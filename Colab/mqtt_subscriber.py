import csv
import random
import pytz
from datetime import datetime
from paho.mqtt import client as mqtt_client
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# MQTT Settings
broker = 'broker.emqx.io'
port = 1883
client_id = f'subscribe-{random.randint(0, 100)}'
username = 'emqx'
password = 'public'

# CSV File Path
filename = "dataset.csv"

# Create CSV file with headers (if not exists)
try:
    with open(filename, "x", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Timestamp", "MQ2", "MQ4", "MQ135",
                         "DHT-temp", "DHT-Humidity"])
except FileExistsError:
    pass


# Store latest sensor values temporarily
latest_values = {
    "MQ2": None,
    "MQ4": None,
    "MQ135": None,
    "DHT-temp": None,
    "DHT-Humidity": None
}


# ------------------------
# Email Notification System
# ------------------------
def send_email(topic, value):
    sender_email = "crce.9866.ecs@gmail.com"
    password = "mohtbcvngtxyycmo"

    receiver_email = "crce.9843.ecs@gmail.com"
    subject = "⚠ Air Quality Alert"

    if topic == "DHT-temp":
        message = "⚠ Temperature has reached extreme levels. Stay hydrated."
    else:
        message = f"⚠ Warning: Dangerous gas levels detected.\n{topic} : {value}"

    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg["Subject"] = subject
    msg.attach(MIMEText(message, "plain"))

    context = ssl.create_default_context()

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
        print("Email sent successfully!")
    except Exception as e:
        print(f"Email error: {e}")


# ------------------------
# MQTT Subscribe Callback
# ------------------------
def subscribe(client: mqtt_client.Client):
    def on_message(client, userdata, msg):
        topic = msg.topic
        value = msg.payload.decode()

        # Store received value
        if topic in latest_values:
            latest_values[topic] = float(value)

        # Threshold alerts
        if topic == "MQ2" and float(value) > 0.9:
            send_email(topic, value)

        if topic == "MQ4" and float(value) > 0.7:
            send_email(topic, value)

        if topic == "MQ135" and float(value) > 2:
            send_email(topic, value)

        if topic == "DHT-temp" and float(value) > 40:
            send_email(topic, value)

        if topic == "DHT-Humidity" and float(value) > 50:
            send_email(topic, value)

        # Log to CSV only when all values received once
        if all(v is not None for v in latest_values.values()):
            india_tz = pytz.timezone('Asia/Kolkata')
            data_row = [
                datetime.now(india_tz).isoformat(),
                latest_values["MQ2"],
                latest_values["MQ4"],
                latest_values["MQ135"],
                latest_values["DHT-temp"],
                latest_values["DHT-Humidity"]
            ]

            with open(filename, "a", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(data_row)

            print("Logged to CSV:", data_row)

            # Reset values
            for key in latest_values:
                latest_values[key] = None

    # Subscribe to required topics
    client.subscribe("MQ2")
    client.subscribe("MQ4")
    client.subscribe("MQ135")
    client.subscribe("DHT-temp")
    client.subscribe("DHT-Humidity")

    client.on_message = on_message


# ------------------------
# MQTT Connection
# ------------------------
def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to broker!")
        else:
            print("Connection failed:", rc)

    client = mqtt_client.Client(
        client_id=client_id,
        callback_api_version=mqtt_client.CallbackAPIVersion.VERSION1
    )
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)

    return client


# ------------------------
# RUN Script
# ------------------------
def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()


if __name__ == "__main__":
    run()
