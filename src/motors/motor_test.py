#  import adafruit_motor.servo
from adafruit_servokit import ServoKit

kit = ServoKit(channels=16, reference_clock_speed=26541466)

for servo_num in range(6):
    kit.servo[servo_num].set_pulse_width_range(1100, 1900)
    kit.servo[servo_num].actuation_range = 180


kit.servo[0].set_pulse_width_range(1100, 1900)
kit.servo[0].angle = 90
kit.servo[1].angle = 90
kit.servo[2].angle = 90
