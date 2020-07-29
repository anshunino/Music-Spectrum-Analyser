/*
 MOSI: pin 11
 SCK: pin 13
 Latch: pin 10
 */

#include <SPI.h>
#define latch_pin 10

uint8_t fft_frame[8] = {0};
uint8_t temp = 0;
uint8_t index = 0;
void setup() {
 // Serial.begin(9600);
 DDRD |= 0b01111100; // setting pin 2,3,4,5,6 on arduino to output
  SPI.begin();
  pinMode(latch_pin, OUTPUT);
  Serial.begin(19200);
}

void loop() {
  if(Serial.available() > 0)
  {
    temp = Serial.read();
    if(temp == 0x55)
      index = 0;
      else
      {
        fft_frame[index] = temp;
        index++;
      } 
  }

    
    for(uint8_t j = 0; j <8; j++)
      {
        SPI.transfer(1<<j);
        PORTD = fft_frame[j]<<2;
        PORTB  |= 1<<PB2; //digitalWrite(latch_pin,HIGH);
        PORTB &= ~(1<<PB2);
        //digitalWrite(latch_pin,LOW);
      }
 
}
