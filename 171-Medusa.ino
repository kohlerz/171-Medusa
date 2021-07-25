#include <ESP8266WiFi.h>
#include <Servo.h>

#define port 6969 
#define left_pin 3
#define right_pin 4
#define cmd_size 12

bool enabled = false;

char cmd[cmd_size];
char keepalive[] = {'k','e','e','p','a','l','i','v','e',' ',' ',NULL};

Servo leftMotor;  // Motor controllers use same signal as servos
Servo rightMotor;

long last_time = 0;
long current_time = 0;

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
  if (client) {
    while (client.connected())
    {
      if (client.available())
      {
        client.readBytesUntil('\n', cmd, cmd_size);
//        for(int i=0; i<cmd_size; i++) {
//          Serial.print(cmd[i], DEC);
//        }
//        Serial.println();

        if (array_cmp(cmd, keepalive)) {
          client.println("OK");
        }
        
        Serial.println(cmd);
        delay(100);
      }
    }
  }

  Serial.printf("Stations connected to soft-AP = %d\n", WiFi.softAPgetStationNum());
  delay(1000);
}

boolean array_cmp(char *a, char *b){
      int n;

      // test each element to be the same. if not, return false
      for (n=0;n<cmd_size;n++) if (a[n]!=b[n]) return false;

      //ok, if we have not returned yet, they are equal :)
      return true;
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
