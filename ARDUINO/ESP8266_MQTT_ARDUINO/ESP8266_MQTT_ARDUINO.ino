#include <ESP8266WiFi.h>
#include <PubSubClient.h>

#define DEV_ADDR 2

const char* ssid = "COLDSPOT";
const char* password =  "1234567890";
const char* mqttServer = "192.168.43.135";
const int mqttPort = 1883;
const int QoS_LEVEL = 2;

//const char* mqttUser = "YourMqttUser";
//const char* mqttPassword = "YourMqttUserPassword";

int DEST_ADDR;

String final_msg;
const char* pub_topic_name = "rpi_gateway/esp";
const char* sub_topic_name = "rpi_gateway/esp_outgoing";

char* rx_msg = "";
 
WiFiClient espClient;
PubSubClient client(espClient);
 
void setup()
{
  Serial.begin(115200);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED)
  {
    delay(500);
    Serial.println("Connecting to WiFi..");
  }
  Serial.println("Connected to the WiFi network");
  client.setServer(mqttServer, mqttPort);
  client.setCallback(callback);
 
  while (!client.connected())
  {
    Serial.println("Connecting to MQTT...");
    if (client.connect("ESP8266Client"))
    {
      Serial.println("connected");  
    }
    else
    {
      Serial.print("failed with state ");
      Serial.print(client.state());
      delay(2000);
    }
  }
}
 
void callback(char* topic_msg, byte* payload, unsigned int length)
{
  for (int i = 0; i < length; i++)
  {
    rx_msg[i] = (char)payload[i];
  }
}
 
void loop()
{
  int rnd = 0;
  String str;
  str = (String)rx_msg;
  //str.trim();
  str = str.substring(0, 16);
  DEST_ADDR = random(1, 5);
  if(DEST_ADDR == DEV_ADDR)
  {
    rnd = random(0, 1);
    if(rnd == 0)
    {
      DEST_ADDR = DEST_ADDR - 1;
    }
    else if(rnd == 1)
    {
      DEST_ADDR == DEST_ADDR + 1;
    }
  }

  /*************************Framing the final packet ************************************/
  final_msg = String(DEV_ADDR) + " MESSAGE FROM ESP " + String(DEST_ADDR);
  /**************************************************************************************/
  
  client.publish(pub_topic_name, (char*)final_msg.c_str() , QoS_LEVEL);
  Serial.print("TX: ");
  Serial.print(final_msg);
  Serial.print("\tRX: ");
  client.subscribe(sub_topic_name);
  Serial.print(str);
  delay(100);
  Serial.print("\n");
  client.loop();
}

