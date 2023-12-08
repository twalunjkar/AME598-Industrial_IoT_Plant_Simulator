#define LILYGO_WATCH_2019_WITH_TOUCH
#include <LilyGoWatch.h>
TTGOClass *ttgo;

#include "secrets.h"
#include <WiFiClientSecure.h>
#include <PubSubClient.h>
#include <ArduinoJson.h>
#include <SimpleDHT.h>
#include <WiFi.h>
#include <TimeLib.h>
#include <ESP32Time.h>

//ESP32Time rtc;
ESP32Time rtc(3600);
 
// #include "DHT.h"

// #define DHTPIN 14     // Digital pin connected to the DHT sensor
// #define DHTTYPE DHT11   // DHT 11
// DHT dht(DHTPIN, DHTTYPE);

int pinDHT11 = 25;
SimpleDHT11 dht11(pinDHT11);
 
#define AWS_IOT_PUBLISH_TOPIC   "TTGO/pub"
#define AWS_IOT_SUBSCRIBE_TOPIC "TTGO/sub"


// read without samples.
byte temperature = 0;
byte humidity = 0;

long int t;
int h ;
int tmp;
 
 
WiFiClientSecure net = WiFiClientSecure();
PubSubClient client(net);
 
void connectAWS()
{
  WiFi.mode(WIFI_STA);
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
 
  Serial.println("Connecting to Wi-Fi");
 
  while (WiFi.status() != WL_CONNECTED)
  {
    delay(500);
    Serial.print(".");
  }
 
  // Configure WiFiClientSecure to use the AWS IoT device credentials
  net.setCACert(AWS_CERT_CA);
  net.setCertificate(AWS_CERT_CRT);
  net.setPrivateKey(AWS_CERT_PRIVATE);
 
  // Connect to the MQTT broker on the AWS endpoint we defined earlier
  client.setServer(AWS_IOT_ENDPOINT, 8883);
 
  // Create a message handler
  client.setCallback(messageHandler);
 
  Serial.println("Connecting to AWS IOT");
 
  while (!client.connect(THINGNAME))
  {
    Serial.print(".");
    delay(100);
  }
 
  if (!client.connected())
  {
    Serial.println("AWS IoT Timeout!");
    return;
  }
 
  // Subscribe to a topic
  client.subscribe(AWS_IOT_SUBSCRIBE_TOPIC);
 
  Serial.println("AWS IoT Connected!");
}
 
void publishMessage()
{
  StaticJsonDocument<200> doc;
  doc["Timestamp"] = t;
  doc["humidity"] = h;
  doc["temperature"] = tmp;
  char jsonBuffer[512];
  serializeJson(doc, jsonBuffer);   // print to client
 
  client.publish(AWS_IOT_PUBLISH_TOPIC, jsonBuffer);
}
 
void messageHandler(char* topic, byte* payload, unsigned int length)
{
  Serial.print("incoming: ");
  Serial.println(topic);

  if ( strstr(topic, "TTGO/sub") ) 
  {
    StaticJsonDocument<200> doc;
    deserializeJson(doc, payload);
    String Relay1 = doc["status"];
    int r1 = Relay1.toInt();
    if(r1==1)
    {
      // digitalWrite(lamp1, LOW);
      // Serial.print("Lamp1 is ON");
      ttgo->tft->setTextSize(1);
      ttgo->tft->fillScreen(0);
      ttgo->tft->print("recieved");
    }
    else if(r1==0)
    {
      // digitalWrite(lamp1, HIGH);
      // Serial.print("Lamp1 is OFF");
      ttgo->tft->setTextSize(1);
      ttgo->tft->fillScreen(0);
      ttgo->tft->print("Not Intrested");
    }
  }
 
  // StaticJsonDocument<200> doc;
  // deserializeJson(doc, payload);
  // const char* message = doc["message"];
  // Serial.println(message);
}
 
void setup()
{
  Serial.begin(115200);
    ttgo = TTGOClass::getWatch();
    rtc.setTime(1700961773); 

    ttgo->begin();
    ttgo->openBL();
    
    ttgo->tft->fillScreen(TFT_BLACK);
    ttgo->tft->setTextColor(TFT_WHITE, TFT_BLACK);
    ttgo->tft->setTextFont(4);
  connectAWS();
  // dht.begin();
}
 
void loop()
{
  // start working...
  Serial.println("=================================");
  Serial.println("Sample DHT11...");
  

  int err = SimpleDHTErrSuccess;
  if ((err = dht11.read(&temperature, &humidity, NULL)) != SimpleDHTErrSuccess) {
    Serial.print("Read DHT11 failed, err="); Serial.println(err); delay(1000);
    return;
  }

  Serial.print("Sample OK: ");
  Serial.print(String((float)temperature) + "* C, ");
  Serial.println(String((float)humidity) + "% H");

      // ttgo->tft->drawString(String((int)temperature*1.8 + 32) + " *F",  5, 10);
      // ttgo->tft->drawString(String(humidity) + " % H",  5, 40);
      t = rtc.getEpoch();
      tmp = (int)temperature;
      h = (int)humidity;

  // h = dht.readHumidity();
  // tmp = dht.readTemperature();
 
  if (isnan(h) || isnan(tmp) )  // Check if any reads failed and exit early (to try again).
  {
    Serial.println(F("Failed to read from DHT sensor!"));
    return;
  }

  Serial.print(F("UTC Time: "));
  Serial.print(t);
  Serial.print(F("Humidity: "));
  Serial.print(h);
  Serial.print(F("%  Temperature: "));
  Serial.print(tmp);
  Serial.println(F("°C "));
 
  publishMessage();
  client.loop();
  delay(1000);
}