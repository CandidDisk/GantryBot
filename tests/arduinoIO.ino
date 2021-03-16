
const byte numChars = 64;
char receivedChars[numChars];

boolean newData = false;



void setup() {
    Serial.begin(115200);

    pinMode(LED_BUILTIN, OUTPUT);
    digitalWrite(LED_BUILTIN, HIGH);
    delay(200);
    digitalWrite(LED_BUILTIN, LOW);
    delay(200);
    digitalWrite(LED_BUILTIN, HIGH);

    Serial.println("<Arduino is ready>");
}

void loop() {
    recvWithStartEndMarkers();
    replyToPython();
}



void recvWithStartEndMarkers() {
    static boolean recvInProgress = false;
    static byte ndx = 0;
    char startMarker = '<';
    char endMarker = '>';
    char rc;

    while (Serial.available() > 0 && newData == false) {
        rc = Serial.read();

        if (recvInProgress == true) {
            if (rc != endMarker) {
                receivedChars[ndx] = rc;
                ndx++;
                if (ndx >= numChars) {
                    ndx = numChars - 1;
                }
            }
            else {
                receivedChars[ndx] = '\0'; 
                recvInProgress = false;
                ndx = 0;
                newData = true;
            }
        }

        else if (rc == startMarker) {
            recvInProgress = true;
        }
    }
}



void replyToPython() {
    if (newData == true) {
        Serial.print("<Message start ... ");
        Serial.print(receivedChars);
        Serial.print("   ");
        Serial.print(millis());
        Serial.print('>');
        digitalWrite(LED_BUILTIN, ! digitalRead(LED_BUILTIN));
        newData = false;
    }
}