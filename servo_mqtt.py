# send to mqtt message servo1=1;servo2=12
import paho.mqtt.client as mqttClient
import time
import ssl
from time import sleep
import RPi.GPIO as GPIO
import sys

servo1_pin = 2
servo2_pin = 14

GPIO.setmode(GPIO.BCM)
GPIO.setup(servo1_pin, GPIO.OUT)
GPIO.setup(servo2_pin, GPIO.OUT)

p1 = GPIO.PWM(servo1_pin, 50)
p2 = GPIO.PWM(servo2_pin, 50)

p1.start(0)
p2.start(0)

host = "host"
port = "port"
user = "user"
password = "password"
ca = "ca"
sub_topic = "subscribe topic"

def on_message(client, userdata, message):
    rotate = message.payload.decode()
    res = {x[0]:x[1] for x in [y.split("=") for y in rotate.split(";") if len(y)]}
    p1.ChangeDutyCycle(float(res["servo1"]))
    p2.ChangeDutyCycle(float(res["servo2"]))
    sleep(1)
    p1.ChangeDutyCycle(0)
    p2.ChangeDutyCycle(0)


client = mqttClient.Client("Python")
client.username_pw_set(user, password=password)
client.tls_set(ca_certs=ca)
client.tls_insecure_set(True)
client.connect(host, port, 60)
client.loop_start()
client.subscribe(sub_topic)

try:
    while True:
        client.on_message=on_message

except KeyboardInterrupt:

    client.disconnect()
    client.loop_stop()
    p1.stop()
    p2.stop()
    GPIO.cleanup()
