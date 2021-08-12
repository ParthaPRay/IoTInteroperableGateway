import paho.mqtt.client as mqttClient
import time

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
nrf_out_topic = "rpi_gateway/nrf_outgoing"
ts1_out_topic = "rpi_gateway/ts1_outgoing"
ts2_out_topic = "rpi_gateway/ts2_outgoing"
esp_out_topic = "rpi_gateway/esp_outgoing"
bth_out_topic = "rpi_gateway/bth_outgoing"

#USR_MSG = "HELLO"


def route_packet(SRC_ADDR, USR_MSG, DEST_ADDR):
    
    SRC_STR = ""
    
    if SRC_ADDR == NRF_ADDR:
        SRC_STR = NRF_STR
        
    elif SRC_ADDR == ESP_ADDR:
        SRC_STR = ESP_STR
        
    elif SRC_ADDR == TS1_ADDR:
        SRC_STR = TS1_STR
        
    elif SRC_ADDR == TS2_ADDR:
        SRC_STR = TS2_STR
        
    elif SRC_ADDR == BTH_ADDR:
        SRC_STR = BTH_STR

    if DEST_ADDR == NRF_ADDR: # ROUTING PACKET TO NRF24L01 #
        print("PKT-NO: {} || ".format(pkt_no) + "SOURCE: {}".format(SRC_STR) + " ({}) || ".format(SRC_ADDR) + "DATA: {} || ".format(USR_MSG) + "DESTINATION: NRF ({})\n".format(NRF_ADDR))
        client.publish(nrf_out_topic, USR_MSG, 2)
    
    elif DEST_ADDR == ESP_ADDR:
        print("PKT-NO: {} || ".format(pkt_no) + "SOURCE: {}".format(SRC_STR) + " ({}) || ".format(SRC_ADDR) + "DATA: {} || ".format(USR_MSG) + "DESTINATION: ESP ({})\n".format(ESP_ADDR))
        client.publish(esp_out_topic, USR_MSG, 2)
    
    
    elif DEST_ADDR == TS1_ADDR:   
        print("PKT-NO: {} || ".format(pkt_no) + "SOURCE: {}".format(SRC_STR) + " ({}) || ".format(SRC_ADDR) + "DATA: {} || ".format(USR_MSG) + "DESTINATION: TS1 ({})\n".format(TS1_ADDR))
        client.publish(ts1_out_topic, USR_MSG, 2)
    
    elif DEST_ADDR == TS2_ADDR:
        print("PKT-NO: {} || ".format(pkt_no) + "SOURCE: {}".format(SRC_STR) + " ({}) || ".format(SRC_ADDR) + "DATA: {} || ".format(USR_MSG) + "DESTINATION: TS2 ({})\n".format(TS2_ADDR))
        client.publish(ts2_out_topic, USR_MSG, 2)
        
    elif DEST_ADDR == BTH_ADDR:
        print("PKT-NO: {} || ".format(pkt_no) + "SOURCE: {}".format(SRC_STR) + " ({}) || ".format(SRC_ADDR) + "DATA: {} || ".format(USR_MSG) + "DESTINATION: BTH ({})\n".format(BTH_ADDR))
        client.publish(bth_out_topic, USR_MSG, 2)

 
def on_connect(client, userdata, flags, rc):
    
    if rc == 0:
        print("\t... INITIALIZATION COMPLETE. BEGINNING ROUTING ...\n\n")
 
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
            route_packet(SRC_ADDR, USR_MSG, DEST_ADDR)
    
        except:
            print("\n\t\t!! PACKET STRUCTURE INVALID !!")
            
    
Connected = False   #global variable for the state of the connection

QoS = 2
BROKER_ADDRESS= "localhost"  #Broker address
PORT_NUMBER = 1883                         #Broker port

print("\t\t.... INITIALIZING PACKET ROUTER ....\n")
 
client = mqttClient.Client("PACKET_ROUTER")               #create new instance

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
