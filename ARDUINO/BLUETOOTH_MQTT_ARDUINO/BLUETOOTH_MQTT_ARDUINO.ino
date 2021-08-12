#include <SoftwareSerial.h>

#define DEV_ADDR 5
#define BTH_TX_PIN 5
#define BTH_RX_PIN 6
#define STATUS_TX 0
#define STATUS_RX 1

int STATUS = 0;
int DEST_ADDR;
int final_msg_length;
String final_message;
int rx_int;
String rx_str;

SoftwareSerial bth(BTH_TX_PIN, BTH_RX_PIN);

void setup()
{
  Serial.begin( 9600 );
  bth.begin(9600);
}

void loop()
{
  DEST_ADDR = random(1, 4);
  final_message = String(DEV_ADDR) + " MESSAGE FROM BTH " + String(DEST_ADDR);
  final_msg_length = final_message.length();
  if(STATUS == STATUS_TX)
  {
    bth.print(final_message);
    STATUS = STATUS_RX;
    //delay(500);
  }

  else if(STATUS == STATUS_RX)
  {
    //while(bth.available())
    if(bth.available() > 0)
    {
//      rx_data = String(bth.read());
        //rx_int = bth.parseInt();
        rx_str = bth.readString();
        //delay(1);
     }
     //rx_str = String(rx_int);
     //delay(500);
     STATUS = STATUS_TX;
  }
  Serial.print("TX:  ");
  Serial.print(final_message);
  Serial.print("\tRX:  ");
  Serial.print(rx_str);
  Serial.print("\n");
  rx_int = 0;
  delay(1000);
}

