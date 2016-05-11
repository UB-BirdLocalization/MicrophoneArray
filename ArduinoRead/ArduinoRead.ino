int mic1;
int mic2;
int mic3; 
unsigned long timer1 = 0;
unsigned long samples = 0;
int runTime = 0;
char buffer [20];      

// Define various ADC prescaler
const unsigned char PS_16 = (1 << ADPS2);
const unsigned char PS_32 = (1 << ADPS2) | (1 << ADPS0);
const unsigned char PS_64 = (1 << ADPS2) | (1 << ADPS1);
const unsigned char PS_128 = (1 << ADPS2) | (1 << ADPS1) | (1 << ADPS0);

void setup() {
  Serial.begin(250000);
   // set up the ADC
  ADCSRA &= ~PS_128;  // remove bits set by Arduino library

  // you can choose a prescaler from above.
  // PS_16, PS_32, PS_64 or PS_128
  //Document says that ADC clock should be between 50kHz and 200kHz, 64 = 250kHz
  ADCSRA |= PS_64;    // set our own prescaler to 64
}

void loop() {
  while(runTime == 0){
    String tempRunTime = Serial.readStringUntil('\n');
    runTime = tempRunTime.toInt();
  }
  if(!timer1){
    timer1 = micros();
  }
  // read the analog in value:
  mic1 = analogRead(A0);
  mic2 = analogRead(A1);
  mic3 = analogRead(A2);

 sprintf(buffer,"%d,%d,%d\n",mic1,mic2,mic3);

  samples ++;
  Serial.print(buffer);
  if(micros()-timer1 > runTime*1000000){
    //Serial.println();
    Serial.print("Samples: ");
    Serial.print(samples);
    Serial.println(" Sampling rate per second ~");
    Serial.println(samples/runTime);
    runTime = 0;
    timer1 = 0;
    samples = 0;
  }
}
