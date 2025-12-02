#ifndef SENSORS_H
#define SENSORS_H

// Convert ADC reading to voltage
double analogToVoltage(int aValue) {
  float sensor_volt = aValue * (3.3 / 4095.0);
  return sensor_volt;
}

#endif
