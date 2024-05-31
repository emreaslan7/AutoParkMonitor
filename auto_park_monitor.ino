#include <LiquidCrystal.h>
#include <Servo.h>

// Declare a servo motor object and specify the pin for an LED
Servo smotor;
const int ledPin = 13;

// Variables to store the current and previous count of vehicles
int count = 0;
int newCount = 0;

// Initialize the LiquidCrystal library with the pins connected to the LCD
LiquidCrystal lcd(8, 7, 6, 5, 4, 3);

void setup() {
  // Begin serial communication at 9600 baud rate
  Serial.begin(9600);

  // Set the LED pin as an output
  pinMode(ledPin, OUTPUT);

  // Attach the servo motor to pin 9
  smotor.attach(9);

  // Initialize the LCD with 16 columns and 2 rows
  lcd.begin(16,2);

  // Print a title on the first line of the LCD
  lcd.print("CAR PARK");

  // Move the cursor to the second line and print the initial vehicle count
  lcd.setCursor(0, 1);
  lcd.print("Vehicle Count: 0");
}

void loop() {
  // Check if there is incoming data available on the serial port
  if(Serial.available() > 0){
    // Read the incoming data until a newline character is encountered
    String data = Serial.readStringUntil('\n');
    
    // Convert the read string to an integer
    count = data.toInt();

    // Check if the new count is different from the previous count
    if(newCount != count){
      // Update the previous count with the new count
      newCount = count;

      // Turn on the LED to indicate activity
      digitalWrite(ledPin, HIGH);

      // Clear the LCD screen
      lcd.clear();

      // Print the title on the first line of the LCD
      lcd.setCursor(0, 0);
      lcd.print("CAR PARK");

      // Move the cursor to the second line and print the updated vehicle count
      lcd.setCursor(0, 1);
      lcd.print("Vehicle Count:");
      lcd.print(count);

      // Rotate the servo motor to simulate an action
      smotor.write(0);
      delay(4000);
      smotor.write(90);

      // Turn off the LED
      digitalWrite(ledPin, LOW);
    }
  }
}
