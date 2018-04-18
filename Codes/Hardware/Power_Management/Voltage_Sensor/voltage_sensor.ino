// number of analog samples to take per reading
#define NUM_SAMPLES 10

int sum = 0;                    // sum of samples taken
unsigned char sample_count = 0; // current sample number
float voltage = 0.0;            // calculated voltage

void setup()
{
    Serial.begin(9600);
}

void loop()
{
    while (sample_count < NUM_SAMPLES) {
        sum += analogRead(A15);
        sample_count++;
        delay(10);
    }
    voltage = ((float)sum / (float)NUM_SAMPLES * 5.0) / 1023.0;
    Serial.print(voltage * 2);
    Serial.println (" V");
    sample_count = 0;
    sum = 0;
}
