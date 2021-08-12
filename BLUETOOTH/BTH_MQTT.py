import bluetooth
import time
import random
import paho.mqtt.client as mqtt

topic_name = "rpi_gateway/bth"
in_topic = "rpi_gateway/bth_outgoing"

CLIENT_NAME = "BTH_PUBLISHER"
BROKER_ADDRESS = "localhost"
PORT_NUMBER = 1883
TIMEOUT_DURATION = 60
CONNECTED_FLAG = False

DEV_ADDR = 5
DEST_ADDR = 0

pkt_no = 0

in_msg_bth = ""

QoS = 2

message = " MESSAGE FROM BTH "

final_msg = ""

BTH_NODE_MAC_ADDR = "98:D3:35:00:CC:28"
PORT = 1

tx_data = ""
rx_data = ""
rx_data_end = 2
rec = ""

STATUS = 0
STATUS_TX = 0
STATUS_RX = 1
RX_MSG_START_INDEX = 0
RX_MSG_END_INDEX = 20
data_end = 1

sock = bluetooth.BluetoothSocket (bluetooth.RFCOMM)

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        CONNECTED_FLAG = True
        print("\n\tConnection to MQTT Successful! Result Code: "+str(rc) + "\n")
    else:
        print("\n\tConnection to MQTT Unsuccessfull! Result Code: "+str(rc) + "\n")
        client.loop_stop()
        
def on_message(client, userdata, message): 
    global in_msg_bth
#    received = message.payload
    in_msg_bth = message.payload
#    print ("Message received: "  + in_msg)
    #client.publish(topic_name, received, 2)
    try:
        sock.send(in_msg_bth)
        time.sleep(0.2)
    except:
        print ("Transmission Unsuccessful")

client = mqtt.Client(CLIENT_NAME)
client.on_connect = on_connect
client.on_message= on_message                      #attach function to callback
client.connect(BROKER_ADDRESS, PORT_NUMBER)

time.sleep(2)

def connect_bth():
    global sock
    print("\n\t\t..... Connecting to BTH (BLUETOOTH) Node .....\n")
    try:
        sock.connect((BTH_NODE_MAC_ADDR, PORT))
        print("\t..... Successfully Connected to BTH (BLUETOOTH) Node .....\n")
    except:
        print("\t..... Unable to Connect to BTH (BLUETOOTH) Node, EXITING ! .....\n")
        exit(1)
        
connect_bth()

while 1:
        global in_msg_bth, rx_data
        #topic_name = topic_name + "bth"
#        rx_data = ""
#        rec = ""
        #global tx_data, rx_data, rec
#        rnd = random.randint(0, 9)
 #       tx_data = str(rnd)
#        if STATUS == STATUS_TX:
#            try:
#                sock.send(tx_data)
#                time.sleep(0.2)
#	    except:
#                print ("Transmission Unsuccessful")
		
#	    STATUS = STATUS_RX
            
#        elif STATUS == STATUS_RX:
            #global rx_data
#	try:
        time.sleep(0.1)
        rx_data += sock.recv(1024)
        time.sleep(0.1)
            #rec = str(sock.recv(512))
        rec = rx_data[RX_MSG_START_INDEX:RX_MSG_END_INDEX]
#            time.sleep(0.2)
            #data_end = rx_data.find('\n')
#        if data_end != -1:
                #rec = rx_data[:data_end - 1]
                #rec = str(rx_data)
                #rec = rx_data[RX_MSG_START_INDEX:RX_MSG_END_INDEX]
                #rec = rec[RX_MSG_START_INDEX:RX_MSG_END_INDEX]
                #time.sleep(0.3)
                #print ("RX:\t{}\n" .format(rec))
                #rx_data = rx_data[data_end + 1]
                #time.sleep(0.5)
#                STATUS = STATUS_TX
                #time.sleep(0.1)
                #print("TX:  {}" .format(tx_data) + "\tRX:  {}" .format(rec))
        client.publish(topic_name, rec, QoS)
        print("TX:  {}" .format(in_msg_bth) + "\tRX:  {}" .format(rec))
        tx_data = ""
        rx_data = ""
        rec = ""
        #del tx_data
        #del rx_data
        #del rec
        client.loop(2, 10)
        #print("TX:  {}" .format(tx_data) + "\tRX:  {}" .format(rec))
        
        time.sleep(0.2)
#        except KeyboardInterrupt:
#	    break
#	buffer = sock.recv(4096)
#	print buffer
sock.close()
