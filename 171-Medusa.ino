#include <ESP8266WiFi.h>
#include <Servo.h>

#define port 6969 
#define left_pin 3
#define right_pin 4
#define cmd_size 16

bool enabled = false;

char cmd[] = "E 100 90";

Servo leftMotor;  // Motor controllers use same signal as servos
Servo rightMotor;

WiFiServer server(port);

void setup()
{
  Serial.begin(9600);
  Serial.println();

  Serial.println("Starting Wifi Server");
  WiFi.softAP("171-Medusa") ? Serial.println("Ready") : Serial.println("Failed!");
  server.begin();

  Serial.println(WiFi.softAPIP());

  leftMotor.attach(left_pin);
  rightMotor.attach(right_pin);

//  handleIncomingData();
}

void loop()
{
  WiFiClient client = server.available();

  while (client.connected())
  {
    if (client.available())
    {
      client.readBytes(cmd, cmd_size);
      Serial.println(cmd);
    }
  }
}

void handleIncomingData() {
  char* command = strtok(cmd, " ");
  char* enabled = command;
  command = strtok(cmd, " ");
  int left_data = atoi(command);
  command = strtok(0, " ");
  int right_data = atoi(command);

  Serial.println(left_data);
  Serial.println(right_data);
}

void driveMotors(int left_stick, int right_stick) {
  int left_drive  = map(left_drive, -100, 100, 0, 180);
  int right_drive = map(right_drive, -100, 100, 0, 180);

  leftMotor.write(left_drive);
  rightMotor.write(right_drive);
}
