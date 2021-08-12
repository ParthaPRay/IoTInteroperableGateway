import paho.mqtt.client as mqtt
import time
import random

topic_name = "rpi_gateway/"
in_topic = "rpi_gateway/ts1_outgoing"

CLIENT_NAME = "TEST_PUBLISHER_1"
BROKER_ADDRESS = "localhost"
PORT_NUMBER = 1883
TIMEOUT_DURATION = 60
CONNECTED_FLAG = False

DEV_ADDR = 3
DEST_ADDR = 0

pkt_no = 0

in_msg_ts1 = ""

QoS = 2

message = " MESSAGE FROM TS1 "
final_msg = ""

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        CONNECTED_FLAG = True
        print("Connection Successful! Result Code: "+str(rc))
    else:
        print("Connection Unsuccessfull! Result Code: "+str(rc))
        client.loop_stop()
        
def on_message(client, userdata, message):
    global in_msg_ts1
#    received = message.payload
    in_msg_ts1 = message.payload
#    print ("Message received: "  + in_msg)
    #client.publish(topic_name, received, 2)

client = mqtt.Client(CLIENT_NAME)
client.on_connect = on_connect
client.on_message= on_message                      #attach function to callback
client.connect(BROKER_ADDRESS, PORT_NUMBER)

time.sleep(2)

while True:
    
    try:
        rnd = 0
        global pkt_no
        topic_name = topic_name + "ts1"
	DEST_ADDR = random.randint(1, 5)
	
	if DEST_ADDR == DEV_ADDR:
            rnd = random.randint(0, 1)
            if rnd == 0:
                DEST_ADDR = DEST_ADDR + 1
            elif rnd == 1:
                DEST_ADDR = DEST_ADDR - 1
                
        final_msg = str(DEV_ADDR) + message + str(DEST_ADDR)
        pkt_no = pkt_no + 1
#        print("TS1 TX (rpi_gateway/test_topic_1): " + final_msg)
        print("TS1 ---> PKT-NO: {}  ||  ".format(pkt_no) + "TX: {}".format(final_msg) + "  ||  RX: {}".format(in_msg_ts1) + "\n")
        client.publish(topic_name, final_msg, QoS)
        client.subscribe(in_topic, QoS)
        client.loop(2, 10)
        final_msg = ""
        topic_name = "rpi_gateway/";
        time.sleep(1)
        
    except:
            print("INVALID PACKET!")
            try:
                while True:
                    time.sleep(1)
 
            except KeyboardInterrupt:
                quit()
                print ("exiting")
                client.disconnect()
                client.loop_stop()
                
