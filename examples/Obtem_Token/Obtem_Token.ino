#include <MFRC522Extended.h>
#include <require_cpp11.h>
#include <MFRC522.h>
#include <deprecated.h>
#include <ESP8266WiFi.h>
#include <PubSubClient.h>
/*
   Curso de Arduino e AVR WR Kits Channel
   
   Aula 88 - RFID - Introdução
   
    
   Autor: Eng. Wagner Rambo  Data: Outubro de 2016
   
   www.wrkits.com.br | facebook.com/wrkits | youtube.com/user/canalwrkits
   
*/

// --- Bibliotecas Auxiliares ---
#include <SPI.h>
#include <MFRC522.h>

// --- mqtt_esp8266
// Update these with values suitable for your network.

const char* ssid = "";
const char* password = "";
const char* mqtt_server = "";

WiFiClient espClient;
PubSubClient client(espClient);
long lastMsg = 0;
char msg[50];
int value = 0;



// --- Mapeamento de Hardware ---
//#define SS_PIN 10 //Arduino
//#define RST_PIN 9 //Arduino


#define SS_PIN 4 //ESP32
#define RST_PIN 5 //ESP32

MFRC522 mfrc522(SS_PIN, RST_PIN);   // Cria instância com MFRC522
 

// --- Variáveis Globais --- 
char st[20];


// --- Configurações Iniciais ---
void setup() 
{
  Serial.begin(9600);   // Inicia comunicação Serial em 9600 baud rate
  SPI.begin();          // Inicia comunicação SPI bus
  mfrc522.PCD_Init();   // Inicia MFRC522
  
  Serial.println("Aproxime o seu cartao do leitor...");
  Serial.println();

  // --- mqtt_esp8266
  pinMode(BUILTIN_LED, OUTPUT);     // Initialize the BUILTIN_LED pin as an output
  //Serial.begin(115200);
  setup_wifi();
  client.setServer(mqtt_server, 1883);
  client.setCallback(callback);
   
  
} //end setup

//Funcoes do MQTT_ESP8266
void setup_wifi() {

  delay(10);
  // We start by connecting to a WiFi network
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
}

void callback(char* topic, byte* payload, unsigned int length) {
  Serial.print("Message arrived [");
  Serial.print(topic);
  Serial.print("] ");
  for (int i = 0; i < length; i++) {
    Serial.print((char)payload[i]);
  }
  Serial.println();

  // Switch on the LED if an 1 was received as first character
  if ((char)payload[0] == '1') {
    digitalWrite(BUILTIN_LED, LOW);   // Turn the LED on (Note that LOW is the voltage level
    // but actually the LED is on; this is because
    // it is acive low on the ESP-01)
  } else {
    digitalWrite(BUILTIN_LED, HIGH);  // Turn the LED off by making the voltage HIGH
  }

}

void reconnect() {
  // Loop until we're reconnected
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    // Attempt to connect
    if (client.connect("ESP8266Client")) {
      Serial.println("connected");
      // Once connected, publish an announcement...
      client.publish("outTopic", "hello world");
      // ... and resubscribe
      client.subscribe("inTopic");
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      // Wait 5 seconds before retrying
      delay(5000);
    }
  }
}

//Fim funcoes do MQTT_ESP8266







// --- Loop Infinito ---
void loop() 
{
  //Funcao mqtt_esp8266
  if (!client.connected()) {
    reconnect();
  }
  client.loop();


  
  // Verifica novos cartões
  if ( ! mfrc522.PICC_IsNewCardPresent()) 
  {
    return;
  }
  // Seleciona um dos cartões
  if ( ! mfrc522.PICC_ReadCardSerial()) 
  {
    return;
  }
  
  // Mostra UID na serial
  Serial.print("UID da tag :");
  String conteudo= "";
  byte letra;
  for (byte i = 0; i < mfrc522.uid.size; i++) 
  {
     
     conteudo.concat(String(mfrc522.uid.uidByte[i] < 0x10 ? " 0" : " "));
     conteudo.concat(String(mfrc522.uid.uidByte[i], HEX));
  }
  conteudo.toUpperCase();
  // Envia o token para o broker
  String token = conteudo.substring(1);
  for(int i =0;i<token.length();i++){
    msg[i] = token[i];
  }
  client.publish("test",msg);

  
  Serial.println(conteudo.substring(1)); // Conteudo.substring(1) contem o Token que deve ser enviado
  delay(1000);
  
} //end loop
 
 
