#  import adafruit_motor.servo
from adafruit_servokit import ServoKit
import time


class Motors:
    def __init__(self):
        self.kit = ServoKit(channels=16, reference_clock_speed=26541466)
        # set the correct pulse range (1100 microseconds to 1900 microseconds)
        for servo in self.kit.servo:
            servo.set_pulse_width_range(1100, 1900)
        self.motor_velocities = [0, 0, 0, 0, 0, 0]
        self.stop_all()

    def drive_motor(self, motor_num: int, velocity: float):
        # maps the velocity from -1..1 where -1 is full throttle reverse and
        # 1 is full throttle forward to an angle where 0 degrees is full
        # throttle reverse and 180 degrees is full throttle forward
        angle = int(velocity * 90) + 90
        self.kit.servo[motor_num].angle = angle

    # move the ROV left or right
    def x_velocity(self, velocity: float):
        # positive velocity - ROV moves right
        # negative velocity - ROV moves left
        self.motor_velocities[0] -= velocity
        self.motor_velocities[1] += velocity
        self.motor_velocities[2] -= velocity
        self.motor_velocities[3] += velocity

    # move the ROV forward or backward
    def y_velocity(self, velocity: float):
        # positive velocity - ROV moves forward
        # negative velocity - ROV moves backward
        self.motor_velocities[0] -= velocity
        self.motor_velocities[1] -= velocity
        self.motor_velocities[2] += velocity
        self.motor_velocities[3] += velocity

    # move the ROV up or down
    def z_velocity(self, velocity: float):
        # positive velocity - ROV moves up
        # negative velocity - ROV moves down
        self.motor_velocities[4] += velocity
        self.motor_velocities[5] += velocity

    # turn the ROV left or right
    def yaw_velocity(self, velocity: float):
        # positive velocity - ROV turns right
        # negative velocity - ROV turns left
        self.motor_velocities[0] -= velocity
        self.motor_velocities[1] += velocity
        self.motor_velocities[2] += velocity
        self.motor_velocities[3] -= velocity

    # make the ROV do a barrel roll
    def roll_velocity(self, velocity: float):
        # positive velocity - ROV rolls to the right, maybe
        # negative velocity - ROV rolls to the left, maybe
        self.motor_velocities[4] -= velocity
        self.motor_velocities[5] += velocity

    def stop_all(self):
        for motor_num in range(6):
            self.drive_motor(motor_num, 0)

    def drive_motors(self):
        for motor_num, velocity in enumerate(self.motor_velocities):
            self.drive_motor(motor_num, velocity)

    def test_motors(self):
        for motor_num in range(6):
            self.drive_motor(motor_num, 0.15)
            time.sleep(0.5)
            self.drive_motor(motor_num, 0)


def main():
    motors = Motors()
    motors.test_motors()
    motors.x_velocity(0.15)
    time.sleep(3)
    motors.x_velocity(0)


if __name__ == "__main__":
    main()

