import serial

import time

import paho.mqtt.client as paho

import time

# XBee setting

serdev = '/dev/ttyUSB0'

s = serial.Serial(serdev, 9600)

# https://os.mbed.com/teams/mqtt/wiki/Using-MQTT#python-client


# MQTT broker hosted on local machine

mqttc = paho.Client()

host = "192.168.1.113"

topic = "velocity"

def on_connect(self, mosq, obj, rc):

      print("Connected rc: " + str(rc))


def on_message(mosq, obj, msg):

      print("[Received] Topic: " + msg.topic + ", Message: " + str(msg.payload) + "\n");


def on_subscribe(mosq, obj, mid, granted_qos):

      print("Subscribed OK")


def on_unsubscribe(mosq, obj, mid, granted_qos):

      print("Unsubscribed OK")

mqttc.on_connect = on_connect

print("Connecting to " + host + "/" + topic)

mqttc.connect(host, port=1883, keepalive=60)

s.write("+++".encode())

char = s.read(2)

print("Enter AT mode.")

print(char.decode())


s.write("ATMY 0x140\r\n".encode())

char = s.read(3)

print("Set MY <BASE_MY>.")

print(char.decode())


s.write("ATDL 0x240\r\n".encode())

char = s.read(3)

print("Set DL <BASE_DL>.")

print(char.decode())


s.write("ATID 0x1\r\n".encode())

char = s.read(3)

print("Set PAN ID <PAN_ID>.")

print(char.decode())


s.write("ATWR\r\n".encode())

char = s.read(3)

print("Write config.")

print(char.decode())


s.write("ATMY\r\n".encode())

char = s.read(4)

print("MY :")

print(char.decode())


s.write("ATDL\r\n".encode())

char = s.read(4)

print("DL : ")

print(char.decode())


s.write("ATCN\r\n".encode())

char = s.read(3)

print("Exit AT mode.")

print(char.decode())


print("start sending RPC")

while True:

    # send RPC to remote
    s.write(bytes("/getAcc/run\r", 'UTF-8'))

    line=s.readline() # Read an echo string from K66F terminated with '\n' (pc.putc())

    #print(line)
    ret = mqttc.publish(topic, "%s\n", line, qos=0)

    if (ret[0] != 0):

        print("Publish failed")

    mqttc.loop()

    time.sleep(0.5)


s.close()