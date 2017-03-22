/*
* Simple program that sends dat afrom a soil moisture sensor
* This device is indiated by the letter A
*/

#include <SPI.h>
#include "nRF24L01.h"
#include "RF24.h"

// Debugging nrf24
int serial_putc( char c, FILE *)
{
  Serial.write( c );
  return c;
}

// Debugging nrf24
void printf_begin(void)
{
  Serial.println("printf_begin begins");
  fdevopen( &serial_putc, 0);
  Serial.println("printf_begin ends");
}

// Pin configuration for nRF24
// nRF24 set the pin 9 to CE and 10 to CSN/SS
// Cables are:
//   SS    -> 10
//   MOSI  -> 11
//   MISO  -> 12
//   SCK   -> 13

RF24 radio(9, 10);

// 
const uint64_t pipes[2] = { 0xF0F0F0F0E1LL, 0xF0F0F0F0D2LL };

// Set a maximum on 30 char
char SendPayload[31] = "";

// Humidity sensor
const int sensPinHumidity = A5;
const char* sensHumidityCode = "99AAAAAA";
const char* sensHumidityType = "05"; // Type is connected to pin number

const int sensOnPin = 8; // Digital pin 8 controls switk on of sensor

// Device code (a 8 hexs code not starting with 99)
char* deviceName = "AAAAAA01";
char* deviceType = "00"; // Arduino nano

void setup() {
  // put your setup code here, to run once  
  Serial.begin(9600); // To debug
  printf_begin();
  
  // nRF24 config
  radio.begin();
  radio.setChannel(0x4c);
  radio.setAutoAck(1);
  radio.setRetries(15, 15);
  radio.setDataRate(RF24_2MBPS);
  radio.setPayloadSize(32);
  radio.openReadingPipe(1, pipes[0]);
  radio.openWritingPipe(pipes[1]);
  radio.startListening();
  radio.printDetails();
  
}

void loop() {
  
  SendPayload[0] = '\0';
  strcat(SendPayload, deviceName);
  strcat(SendPayload, "|");
  strcat(SendPayload, deviceType);
  strcat(SendPayload, "|");
  
  // READ SOIL MISTURE SENSOR
  //     We will keep the sensor not powered on until we need it
  //     To power it on we will use digital pin 8 // NO, facciamo con un transistor
  delay(200);
  int sensValueHumidity = analogRead(sensPinHumidity);  
  Serial.println(sensValueHumidity);

  char buf[4];  
  strcat(SendPayload, sensHumidityCode);
  strcat(SendPayload, "|");
  strcat(SendPayload, sensHumidityType);
  strcat(SendPayload, "|");
  
  strcat(SendPayload, itoa(sensValueHumidity, buf, 10));
  
  // Send an heart beat
  radio.stopListening();
  bool ok = radio.write(&SendPayload, strlen(SendPayload));
  if( !ok ) {
    Serial.println("Radio.write not worked");
  }
  Serial.println("Sent payload");
  Serial.println(SendPayload);
  radio.startListening();
  
  delay(1000);
}

