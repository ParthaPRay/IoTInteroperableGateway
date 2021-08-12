import bluetooth
import time
import random
import threading

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
RX_MSG_END_INDEX = 19
data_end = 1

sock = bluetooth.BluetoothSocket (bluetooth.RFCOMM)

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

def transmit():
    global tx_data, STATUS
    rnd_no = random.randint(0, 9)
    tx_data = str(rnd_no)
    try:
        sock.send(tx_data)
    except:
        print ("Transmission Unsuccessful")
    
    STATUS = STATUS_RX
        
def receive():
    global tx_data, rx_data, STATUS, rec
    rx_data = sock.recv(4096)
    if data_end != -1:
        rec = str(rx_data)
        rec = rec[RX_MSG_START_INDEX:RX_MSG_END_INDEX]
        STATUS = STATUS_TX
        print("TX:  {}" .format(tx_data) + "\tRX:  {}" .format(rec))
       
        #print("TX:  {}" .format(tx_data) + "\tRX:  {}" .format(rec))
        
while 1:
    tx_thread = threading.Thread(target=transmit)
    rx_thread = threading.Thread(target=receive)

    if STATUS == STATUS_TX:
        tx_thread.start()
        tx_thread.join()
	#STATUS = STATUS_RX
            #time.sleep(0.1)
            
    elif STATUS == STATUS_RX:
        rx_thread.start()
        rx_thread.join()
        #STATUS = STATUS_TX
#	try:
    
    tx_data = ""
    rx_data = ""
    rec = ""
    rx_data = ""
    time.sleep(0.1)
#        except KeyboardInterrupt:
#	    break
#	buffer = sock.recv(4096)
#	print buffer
sock.close()
