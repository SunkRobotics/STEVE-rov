#  import adafruit_motor.servo
from adafruit_servokit import ServoKit
import adafruit_pca9685
import board
import busio
import time

i2c = busio.I2C(board.SCL, board.SDA)
pca = adafruit_pca9685.PCA9685(i2c)

kit = ServoKit(channels=16)

for servo_num in range(6):
    kit.servo[servo_num].set_pulse_width_range(1100, 1900)
    kit.servo[servo_num].actuation_range = 180


kit.servo[0].set_pulse_width_range(1100, 1900)
kit.servo[0].angle = 115
kit.servo[1].angle = 115
