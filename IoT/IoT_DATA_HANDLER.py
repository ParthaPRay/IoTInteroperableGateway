#!/usr/bin/env python
import paho.mqtt.client as mqttClient
import time
import httplib, urllib

NRF_ADDR = 1
ESP_ADDR = 2
TS1_ADDR = 3
TS2_ADDR = 4
BTH_ADDR = 5

NRF_STR = "NRF"
ESP_STR = "ESP"
TS1_STR = "TS1"
TS2_STR = "TS2"
BTH_STR = "BTH"

SRC_ADDR_INDEX = 0
DEST_ADDR_INDEX = 19

MSG_BEGIN_INDEX = 2
MSG_END_INDEX = 18

SRC_ADDR_STR = ""
DEST_ADDR_STR = ""

pkt_no = 0

SRC_ADDR = 0
DEST_ADDR = 0

packet = ""
QoS = 2

master_topic_name = "rpi_gateway/mastertopic"

key = "2FBKOKZML6DIWAIW"  # Thingspeak channel to update

headers = {"Content-typZZe": "application/x-www-form-urlencoded","Accept": "text/plain"}
conn = httplib.HTTPConnection("api.thingspeak.com:80")

#Report Raspberry Pi internal temperature to Thingspeak Channel
def Upload_IoT_Data(SRC_ADDR, USR_MSG, DEST_ADDR):
    global headers, conn
    params = urllib.urlencode({"field1": USR_MSG, "status": USR_MSG, "key": key })
    #headers = {"Content-typZZe": "application/x-www-form-urlencoded","Accept": "text/plain"}
    #conn = httplib.HTTPConnection("api.thingspeak.com:80")
    
    try:
        conn.request("POST", "/update", params, headers)
        response = conn.getresponse()
        print "{}" .format(USR_MSG) + "\t[DATA UPLOAD TO IoT CLOUD SUCCESSFUL]: " + "{}". format(response.status)
        data = response.read()
        #conn.close()
        
    except:
        print "connection failed"

def on_connect(client, userdata, flags, rc):
    
    if rc == 0:
        print("\t... INITIALIZATION COMPLETE. BEGINNING IoT DATA UPLOAD ...\n\n")
 
        global Connected                #Use global variable
        Connected = True                #Signal connection
 
    else:
        print("\t\t.... INITIALIZATION FAILED ....\n\n")


def on_message(client, userdata, message):
    
    global pkt_no
    pkt_no = pkt_no + 1
    received = message.payload
    
    if len(received) < 2:
        print("\t\t.....NETWORK IDLE.....\n")
    
    else:
        try:
            SRC_ADDR_STR = received[SRC_ADDR_INDEX]
            DEST_ADDR_STR = received[DEST_ADDR_INDEX]
            SRC_ADDR = int(SRC_ADDR_STR)
            DEST_ADDR = int(DEST_ADDR_STR)
            USR_MSG = received[MSG_BEGIN_INDEX: MSG_END_INDEX]
            Upload_IoT_Data(SRC_ADDR, USR_MSG, DEST_ADDR)
    
        except:
            print("\n\t\t!! PACKET STRUCTURE INVALID !!")
            
    
Connected = False   #global variable for the state of the connection

QoS = 2
BROKER_ADDRESS= "localhost"  #Broker address
PORT_NUMBER = 1883           #Broker port

print("\t\t.... INITIALIZING IoT DATA HANDLER ....\n")
 
client = mqttClient.Client("IoT_DATA_HANDLER")               #create new instance

client.on_connect= on_connect                      #attach function to callback
client.on_message= on_message                      #attach function to callback
 
client.connect(BROKER_ADDRESS, PORT_NUMBER)          #connect to broker
 
client.loop_start()        #start the loop
 
while Connected != True:    #Wait for connection
    time.sleep(0.1)
 
client.subscribe(master_topic_name, QoS)
time.sleep(1)

try:
    while True:
        time.sleep(1)
 
except KeyboardInterrupt:
    print ("exiting")
    client.disconnect()
    client.loop_stop()
