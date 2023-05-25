import time
import board
import adafruit_bno055

imu = adafruit_bno055.BNO055_I2C(board.I2C())

time.sleep(1)

#  imu.mode = adafruit_bno055.COMPASS_MODE

while True:
    print(imu.calibration_status)
    #  print(f"Gyro Calibration: {imu.offsets_gyroscope}")
    #  print(f"Mag Calibration: {imu.offsets_magnetometer}")

    #  print(f"X Acceleration: {imu.acceleration[0]} m/s^2")
    #  print(f"Yaw Angle: {imu.euler[0]}°")
    print(f"Roll Angle: {imu.euler[1]}°")
    #  print(f"Pitch Angle: {imu.euler[2]}°")
    #  print(f"Magnetometer: {imu.magnetic}μT")
    time.sleep(0.1)

