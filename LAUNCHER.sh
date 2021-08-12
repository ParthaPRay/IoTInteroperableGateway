#!/bin/bash

#............ STARTING UP NRF MODULE ............#
sleep 2
pushd ~/Desktop/RPI_GATEWAY/NRF24L01/
lxterminal -e python NRF_MQTT.py
sleep 1
#................................................#


#.......... STARTING UP TEST MODULE 1 ...........#
pushd ../TEST
lxterminal -e python TEST_PUB_1.py
sleep 1
#................................................#


#.......... STARTING UP TEST MODULE 2 ...........#
lxterminal -e python TEST_PUB_2.py
sleep 1
#................................................#


#......... STARTING UP BLUETOOTH MODULE .........#
sleep 1
pushd ../BLUETOOTH
lxterminal -e python BTH_MQTT.py
sleep 1
#................................................#


#........ STARTING UP TOPIC DISTRIBUTER .........#
pushd ../TOPIC_DISTRIBUTER
lxterminal -e python TOPIC_DISTRIBUTER.py
sleep 1
#................................................#


#......... STARTING UP PACKET ROUTER ............#
sleep 1
pushd ../PACKET_ROUTER
lxterminal -e python PACKET_ROUTER.py
sleep 1
#................................................#


#...... STARTING UP IoT CLOUD DATA HANDLER ......#
sleep 1
pushd ../IoT
lxterminal -e python IoT_DATA_HANDLER.py
sleep 1
#................................................#