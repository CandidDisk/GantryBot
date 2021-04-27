// Select the baud rate to match the target device.
#define baudRateSerialPort 115200
#define baudRateInputPort  115200

// When using COM ports, is the device TTL or RS232?
#define isTtlInputPort  false

// Container for the byte to be read-in
int input;

boolean waitReply = true;

void setup() {
    // Put your setup code here, it will run once:

    // Set up serial communication to print out the serial input.
    Serial.begin(baudRateSerialPort);
    while (!Serial) {
        continue;
    }

    // Set up serial communication to send serial input over.
    Serial0.begin(baudRateInputPort);
    Serial0.ttl(isTtlInputPort);
    while (!Serial0) {
        continue;
    }
}

void loop() {
    // Put your main code here, it will run repeatedly:
    if (waitReply = true){
        input = Serial0.read();

        // If there was a valid byte read-in, print it.
        if (input != -1) {
            // Display the input character received.
            Serial.print("Received: ");
            Serial.println((char)input);
        }
        else {
            Serial.println("No data received...");
        }
        delay(1000);
    }
    // Read the input.


    // Wait a second then repeat...

}