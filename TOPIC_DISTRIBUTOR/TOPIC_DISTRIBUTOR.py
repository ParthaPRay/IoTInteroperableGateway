import paho.mqtt.client as mqttClient
import time

received = ""
topic_name = "rpi_gateway/mastertopic"

master_topic_msg = ""
rx_topic = ""
 
def on_connect(client, userdata, flags, rc):
 
    if rc == 0:
 
        print("Connected to broker")
 
        global Connected                #Use global variable
        Connected = True                #Signal connection 
 
    else:
 
        print("Connection failed")
 
def on_message(client, userdata, message):
    global master_topic_msg
    global rx_topic
    rx_topic = message.topic
    #received = message.payload
    master_topic_msg = message.payload
    print ("TOPIC DISTRIBUTION:  {}  ||  ".format(rx_topic) + "DATA:  {}".format(master_topic_msg) + "\n")
    client.publish(topic_name, master_topic_msg, 2)
    

Connected = False   #global variable for the state of the connection

QoS = 2
BROKER_ADDRESS= "localhost"  #Broker address
PORT_NUMBER = 1883                         #Broker port
 
client = mqttClient.Client("TOPIC_DISTRIBUTER")               #create new instance

client.on_connect= on_connect                      #attach function to callback
client.on_message= on_message                      #attach function to callback
 
client.connect(BROKER_ADDRESS, PORT_NUMBER)          #connect to broker
 
client.loop_start()        #start the loop
 
while Connected != True:    #Wait for connection
    time.sleep(0.1)
 
client.subscribe([("rpi_gateway/nrf", QoS), ("rpi_gateway/esp", QoS), ("rpi_gateway/ts1", QoS), ("rpi_gateway/ts2", QoS), ("rpi_gateway/bth", QoS)])
time.sleep(1)

try:
    while True:
        time.sleep(1)
 
except KeyboardInterrupt:
    print ("exiting")
    client.disconnect()
    client.loop_stop()
