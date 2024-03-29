#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BNO055.h>
#include <utility/imumaths.h>

/* Set the delay between fresh samples default 100 */
#define BNO055_SAMPLERATE_DELAY_MS (100)

// Check I2C device address and correct line below (by default address is 0x29 or 0x28)
//                                   id, address

Adafruit_BNO055 bno = Adafruit_BNO055(-1, 0x28);

uint8_t accel = 0;

uint8_t calibrateSensor()
{
  uint8_t system, gyro, accel, mg = 0;
  bno.getCalibration(&system, &gyro, &accel, &mg);
  Serial.print("CALIBRATION: Sys=");
  Serial.print(system, DEC);
  Serial.print(" Gyro=");
  Serial.print(gyro, DEC);
  Serial.print(" Accel=");
  Serial.print(accel, DEC);
  Serial.print(" Mag=");
  Serial.println(mg, DEC);
  return accel;
}

void setup(void)
{
  Serial.begin(115200);

  /* Initialise the sensor */
  if (!bno.begin())
  {
    Serial.print("No BNO055 detected");
    while (1)
      ;
  }

  delay(1000);

  /* Display the current temperature */
  // int8_t temp = bno.getTemp();
  // Serial.print("Current Temperature: ");
  // Serial.print(temp);
  // Serial.println(" C");
  // Serial.println("");

  bno.setExtCrystalUse(true);

  //Calibrate sensor by moving around
  Serial.println("Calibration status values: 0=uncalibrated, 3=fully calibrated");
  Serial.println("Press any key and move sensor until calibration complete.");
  int keyPress = Serial.parseInt();
  while (Serial.available() == 0)
  {
    ; //wait for user to read instructions
  }
  while (accel < 3)
  {
    accel = calibrateSensor();
  }
}

void loop(void)
{
  // Possible vector values can be:
  // - VECTOR_ACCELEROMETER - m/s^2
  // - VECTOR_MAGNETOMETER  - uT
  // - VECTOR_GYROSCOPE     - rad/s
  // - VECTOR_EULER         - degrees
  // - VECTOR_LINEARACCEL   - m/s^2
  // - VECTOR_GRAVITY       - m/s^2
  imu::Vector<3> acc = bno.getVector(Adafruit_BNO055::VECTOR_ACCELEROMETER);
  imu::Vector<3> gyr = bno.getVector(Adafruit_BNO055::VECTOR_GYROSCOPE);
  imu::Vector<3> mag = bno.getVector(Adafruit_BNO055::VECTOR_MAGNETOMETER);
  imu::Quaternion quat = bno.getQuat();

  /* Display the floating point data */
  Serial.print(acc.x(), 4);
  Serial.print(", ");
  Serial.print(acc.y(), 4);
  Serial.print(", ");
  Serial.print(acc.z(), 4);
  Serial.print(", ");
  Serial.print(gyr.x(), 4);
  Serial.print(", ");
  Serial.print(gyr.y(), 4);
  Serial.print(", ");
  Serial.print(gyr.z(), 4);
  Serial.print(", ");
  Serial.print(mag.x(), 4);
  Serial.print(", ");
  Serial.print(mag.y(), 4);
  Serial.print(", ");
  Serial.print(mag.z(), 4);
  Serial.print(", ");
  Serial.print(quat.w(), 4);
  Serial.print(", ");
  Serial.print(quat.x(), 4);
  Serial.print(", ");
  Serial.print(quat.y(), 4);
  Serial.print(", ");
  Serial.print(quat.z(), 4);
  Serial.println("");

  delay(BNO055_SAMPLERATE_DELAY_MS);
}