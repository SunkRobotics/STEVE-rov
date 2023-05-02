#!/usr/bin/python
import ms5837
#  import time

# sensor = ms5837.MS5837_30BA()  # Default I2C bus is 1 (Raspberry Pi 3)
# sensor = ms5837.MS5837_30BA(0) # Specify I2C bus
sensor = ms5837.MS5837_02BA(1)
# sensor = ms5837.MS5837_02BA(0)

# We must initialize the sensor before reading it
if not sensor.init():
    print("Sensor could not be initialized")
    exit(1)

# We have to read values from sensor to update pressure and temperature
if not sensor.read():
    print("Sensor read failed!")
    exit(1)

sensor.setFluidDensity(ms5837.DENSITY_FRESHWATER)

# Spew readings
while True:
    if sensor.read():
        print(f"Pressure: {sensor.pressure()} mbar")
        print(f"Temperature: {sensor.temperature()} C")
        print(f"Altitude: {sensor.altitude():.10f} m")
        print(f"Depth: {(sensor.depth() * 100):.10f} cm")
        #  sensor.pressure(), # Default is mbar (no arguments)
        #  sensor.pressure(ms5837.UNITS_psi), # Request psi
        #  sensor.temperature(), # Default is degrees C (no arguments)
        #  sensor.temperature(ms5837.UNITS_Farenheit) # Request Farenheit
    else:
        print("Sensor read failed!")
        exit(1)
